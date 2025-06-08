#!/usr/bin/env python3
"""
Message Storage Manager
Handles local encrypted message storage using FlightCode V2
"""

import os
import json
import time
from datetime import datetime
import flightcodev2CLI as flightcode
from utils import get_timestamp

class MessageStorage:
    """Manages local encrypted message storage using FlightCode V2"""
    
    def __init__(self, username, password):
        """
        Initialize message storage with FlightCode V2 encryption
        
        Args:
            username: Username for the storage
            password: Password for FlightCode encryption
        """
        self.username = username
        self.password = password
        self.storage_file = f"messages_{username}.hee"
        self.messages = self._load_messages()
    
    def _load_messages(self):
        """Load messages from FlightCode encrypted storage"""
        try:
            if not os.path.exists(self.storage_file):
                return []
            
            # Read encrypted data
            with open(self.storage_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt using FlightCode V2
            try:
                decrypted_data = flightcode.CryptoService.decrypt_data(encrypted_data, self.password)
                messages = json.loads(decrypted_data.decode('utf-8'))
                return messages
            except Exception as decrypt_error:
                print(f"Failed to decrypt messages with FlightCode: {decrypt_error}")
                return []
            
        except Exception as e:
            print(f"Error loading messages: {e}")
            return []
    
    def _save_messages(self):
        """Save messages to FlightCode encrypted storage"""
        try:
            # Convert to JSON
            json_data = json.dumps(self.messages, indent=2, ensure_ascii=False).encode('utf-8')
            
            # Encrypt using FlightCode V2
            encrypted_data = flightcode.CryptoService.encrypt_data(json_data, self.password)
            
            # Save to file
            with open(self.storage_file, 'wb') as f:
                f.write(encrypted_data)
            
            return True
        except Exception as e:
            print(f"Error saving messages with FlightCode: {e}")
            return False
    
    def add_message(self, sender, recipient, content, message_type='received'):
        """
        Add a message to FlightCode encrypted storage
        
        Args:
            sender: Sender username
            recipient: Recipient username
            content: Message content
            message_type: 'sent' or 'received'
        """
        try:
            message = {
                "sender": sender,
                "recipient": recipient,
                "content": content,
                "type": message_type,
                "timestamp": get_timestamp(),
                "id": int(time.time() * 1000000),  # Unique microsecond ID
                "encrypted_with": "FlightCode_V2"  # Mark encryption method
            }
            
            self.messages.append(message)
            success = self._save_messages()
            
            if success:
                print(f"💾 Message saved with FlightCode encryption")
            
            return success
        except Exception as e:
            print(f"Error adding message: {e}")
            return False
    
    def get_chat_messages(self, partner_username, limit=50):
        """
        Get messages for a specific chat partner from FlightCode storage
        
        Args:
            partner_username: Username of chat partner
            limit: Maximum number of messages
            
        Returns:
            List of decrypted messages
        """
        try:
            # Filter messages for this chat
            chat_messages = []
            
            for msg in self.messages:
                if ((msg['sender'] == self.username and msg['recipient'] == partner_username) or
                    (msg['sender'] == partner_username and msg['recipient'] == self.username)):
                    chat_messages.append(msg)
            
            # Sort by timestamp
            chat_messages.sort(key=lambda x: x['timestamp'])
            
            # Return last 'limit' messages
            return chat_messages[-limit:] if len(chat_messages) > limit else chat_messages
        except Exception as e:
            print(f"Error getting chat messages: {e}")
            return []
    
    def get_storage_info(self):
        """Get information about the encrypted storage"""
        try:
            if not os.path.exists(self.storage_file):
                return {
                    "exists": False,
                    "size": 0,
                    "message_count": 0,
                    "encryption": "FlightCode_V2"
                }
            
            file_size = os.path.getsize(self.storage_file)
            message_count = len(self.messages)
            
            return {
                "exists": True,
                "size": file_size,
                "message_count": message_count,
                "encryption": "FlightCode_V2",
                "file_path": self.storage_file
            }
        except Exception as e:
            print(f"Error getting storage info: {e}")
            return {"error": str(e)}
    
    def clear_all_messages(self):
        """Clear all stored messages and delete FlightCode encrypted file"""
        try:
            self.messages = []
            
            # Delete the encrypted file
            if os.path.exists(self.storage_file):
                os.remove(self.storage_file)
                print(f"🗑️ Deleted FlightCode encrypted file: {self.storage_file}")
            
            return True
        except Exception as e:
            print(f"Error clearing messages: {e}")
            return False
    
    def backup_messages(self, backup_password=None):
        """Create a backup of messages with FlightCode encryption"""
        try:
            if backup_password is None:
                backup_password = self.password
            
            backup_file = f"backup_messages_{self.username}_{int(time.time())}.hee"
            
            # Create backup data
            backup_data = {
                "username": self.username,
                "backup_time": get_timestamp(),
                "encryption": "FlightCode_V2",
                "messages": self.messages
            }
            
            # Convert to JSON
            json_data = json.dumps(backup_data, indent=2, ensure_ascii=False).encode('utf-8')
            
            # Encrypt with FlightCode V2
            encrypted_backup = flightcode.CryptoService.encrypt_data(json_data, backup_password)
            
            # Save backup
            with open(backup_file, 'wb') as f:
                f.write(encrypted_backup)
            
            print(f"💾 Backup created: {backup_file}")
            return backup_file
        except Exception as e:
            print(f"Error creating backup: {e}")
            return None
    
    def restore_from_backup(self, backup_file, backup_password=None):
        """Restore messages from FlightCode encrypted backup"""
        try:
            if backup_password is None:
                backup_password = self.password
            
            if not os.path.exists(backup_file):
                print(f"Backup file not found: {backup_file}")
                return False
            
            # Read encrypted backup
            with open(backup_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt with FlightCode V2
            decrypted_data = flightcode.CryptoService.decrypt_data(encrypted_data, backup_password)
            backup_data = json.loads(decrypted_data.decode('utf-8'))
            
            # Restore messages
            if 'messages' in backup_data:
                self.messages = backup_data['messages']
                success = self._save_messages()
                
                if success:
                    print(f"✅ Messages restored from backup: {backup_file}")
                    return True
            
            return False
        except Exception as e:
            print(f"Error restoring from backup: {e}")
            return False
