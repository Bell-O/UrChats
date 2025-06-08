#!/usr/bin/env python3
"""
Chat Manager
Handles sending and receiving encrypted messages
"""

import os
import sys
import json
import base64
import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box
from nacl.encoding import Base64Encoder
from utils import get_timestamp

class ChatManager:
    """Manages chat operations"""
    
    def __init__(self, user_data, db_manager):
        """
        Initialize the chat manager
        
        Args:
            user_data: User data dictionary
            db_manager: Database manager instance
        """
        self.user_data = user_data
        self.db_manager = db_manager
        self.username = user_data['username']
        
        # Get identity keys
        self.identity_private_key = PrivateKey(Base64Encoder.decode(user_data['identity_private_key']))
        self.identity_public_key = PublicKey(Base64Encoder.decode(user_data['identity_public_key']))
        
        # Initialize or get chat keypair for current DB
        self._initialize_chat_keypair()
    
    def _initialize_chat_keypair(self):
        """Initialize or get chat keypair for current DB"""
        try:
            # Get Supabase URL
            supabase_url = os.getenv("SUPABASE_URL")
            
            # Check if we have a keypair for this DB
            if supabase_url in self.user_data['db_profiles']:
                db_profile = self.user_data['db_profiles'][supabase_url]
                
                if not db_profile['current_keypair']:
                    # Generate new keypair
                    private_key = PrivateKey.generate()
                    public_key = private_key.public_key
                    
                    # Store keypair
                    db_profile['current_keypair'] = {
                        "private_key": Base64Encoder.encode(bytes(private_key)).decode('utf-8'),
                        "public_key": Base64Encoder.encode(bytes(public_key)).decode('utf-8'),
                        "created_at": get_timestamp()
                    }
            else:
                # Create new DB profile
                private_key = PrivateKey.generate()
                public_key = private_key.public_key
                
                self.user_data['db_profiles'][supabase_url] = {
                    "current_keypair": {
                        "private_key": Base64Encoder.encode(bytes(private_key)).decode('utf-8'),
                        "public_key": Base64Encoder.encode(bytes(public_key)).decode('utf-8'),
                        "created_at": get_timestamp()
                    },
                    "old_keys": []
                }
        except Exception as e:
            print(f"Error initializing chat keypair: {e}")
    
    def send_message(self, recipient_username, recipient_public_key_str, message):
        """
        Send an encrypted message to a recipient
        
        Args:
            recipient_username: Username of the recipient
            recipient_public_key_str: Recipient's public key as string
            message: Message to send
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert recipient's public key from string to PublicKey object
            recipient_public_key = PublicKey(Base64Encoder.decode(recipient_public_key_str))
            
            # Create encryption box
            box = Box(self.identity_private_key, recipient_public_key)
            
            # Encrypt message
            nonce = nacl.utils.random(Box.NONCE_SIZE)
            encrypted = box.encrypt(message.encode('utf-8'), nonce)
            ciphertext = Base64Encoder.encode(encrypted).decode('utf-8')
            
            # Send message to database
            success = self.db_manager.send_message(self.username, recipient_username, ciphertext)
            
            return success
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
    
    def receive_messages(self):
        """
        Receive and decrypt messages
        
        Returns:
            List of decrypted messages if successful, empty list otherwise
        """
        try:
            # Get messages from database
            encrypted_messages = self.db_manager.get_messages(self.username)
            
            decrypted_messages = []
            
            for msg in encrypted_messages:
                try:
                    # Get sender's public key
                    sender_public_key_str = self.db_manager.get_user_public_key(msg['sender_username'])
                    
                    if not sender_public_key_str:
                        print(f"Could not find public key for {msg['sender_username']}")
                        continue
                    
                    # Convert sender's public key from string to PublicKey object
                    sender_public_key = PublicKey(Base64Encoder.decode(sender_public_key_str))
                    
                    # Create decryption box
                    box = Box(self.identity_private_key, sender_public_key)
                    
                    # Decrypt message
                    encrypted = Base64Encoder.decode(msg['ciphertext'])
                    decrypted = box.decrypt(encrypted).decode('utf-8')
                    
                    # Add decrypted message to list
                    decrypted_messages.append({
                        "sender_username": msg['sender_username'],
                        "timestamp": msg['timestamp'],
                        "decrypted_content": decrypted
                    })
                except Exception as e:
                    print(f"Error decrypting message from {msg['sender_username']}: {e}")
                    
                    # Try with old keys
                    decrypted = self._try_decrypt_with_old_keys(msg['ciphertext'], sender_public_key_str)
                    
                    if decrypted:
                        decrypted_messages.append({
                            "sender_username": msg['sender_username'],
                            "timestamp": msg['timestamp'],
                            "decrypted_content": decrypted
                        })
            
            return decrypted_messages
        except Exception as e:
            print(f"Error receiving messages: {e}")
            return []
    
    def _try_decrypt_with_old_keys(self, ciphertext, sender_public_key_str):
        """
        Try to decrypt a message with old keys
        
        Args:
            ciphertext: Encrypted message
            sender_public_key_str: Sender's public key as string
            
        Returns:
            Decrypted message if successful, None otherwise
        """
        try:
            # Get Supabase URL
            supabase_url = os.getenv("SUPABASE_URL")
            
            # Check if we have old keys for this DB
            if supabase_url in self.user_data['db_profiles']:
                db_profile = self.user_data['db_profiles'][supabase_url]
                
                # Convert sender's public key from string to PublicKey object
                sender_public_key = PublicKey(Base64Encoder.decode(sender_public_key_str))
                
                # Try each old key
                for key_data in db_profile.get('old_keys', []):
                    try:
                        # Get private key
                        private_key = PrivateKey(Base64Encoder.decode(key_data['private_key']))
                        
                        # Create decryption box
                        box = Box(private_key, sender_public_key)
                        
                        # Decrypt message
                        encrypted = Base64Encoder.decode(ciphertext)
                        decrypted = box.decrypt(encrypted).decode('utf-8')
                        
                        return decrypted
                    except Exception:
                        # Try next key
                        continue
            
            return None
        except Exception as e:
            print(f"Error trying old keys: {e}")
            return None

    def get_chat_history(self, partner_username, limit=50):
        """
        Get chat history with a specific user
        
        Args:
            partner_username: Username of the chat partner
            limit: Maximum number of messages to retrieve
        
        Returns:
            List of messages sorted by timestamp
        """
        try:
            # Get all messages between current user and partner
            sent_messages = self.db_manager.get_messages_between_users(
                self.username, partner_username
            )
            received_messages = self.db_manager.get_messages_between_users(
                partner_username, self.username
            )
        
            # Decrypt received messages
            decrypted_received = []
            for msg in received_messages:
                try:
                    # Get sender's public key
                    sender_public_key_str = self.db_manager.get_user_public_key(msg['sender_username'])
                
                    if sender_public_key_str:
                        # Convert sender's public key from string to PublicKey object
                        sender_public_key = PublicKey(Base64Encoder.decode(sender_public_key_str))
                    
                        # Create decryption box
                        box = Box(self.identity_private_key, sender_public_key)
                    
                        # Decrypt message
                        encrypted = Base64Encoder.decode(msg['ciphertext'])
                        decrypted = box.decrypt(encrypted).decode('utf-8')
                    
                        decrypted_received.append({
                            "sender_username": msg['sender_username'],
                            "recipient_username": msg['recipient_username'],
                            "content": decrypted,
                            "timestamp": msg['timestamp'],
                            "message_type": "received"
                        })
                except Exception as e:
                    print(f"Error decrypting message: {e}")
        
            # Add sent messages (no decryption needed)
            all_messages = []
        
            # Add received messages
            for msg in decrypted_received:
                all_messages.append(msg)
        
            # Add sent messages (we need to get these from database too)
            # For now, we'll just return received messages
            # You can extend this to also fetch and include sent messages
        
            # Sort by timestamp
            all_messages.sort(key=lambda x: x['timestamp'])
        
            # Return last 'limit' messages
            return all_messages[-limit:] if len(all_messages) > limit else all_messages
        
        except Exception as e:
            print(f"Error getting chat history: {e}")
            return []
