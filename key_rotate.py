#!/usr/bin/env python3
"""
Key Rotation Manager
Handles key rotation and management
"""

import os
import sys
import json
import nacl.utils
from nacl.public import PrivateKey, PublicKey
from nacl.encoding import Base64Encoder
import getpass
from utils import get_timestamp
import flightcodev2CLI as flightcode

class KeyRotationManager:
    """Manages key rotation"""
    
    def __init__(self, user_data, db_manager):
        """
        Initialize the key rotation manager
        
        Args:
            user_data: User data dictionary
            db_manager: Database manager instance
        """
        self.user_data = user_data
        self.db_manager = db_manager
        self.username = user_data['username']
        self.profile_path = "user_profile.json.he"
    
    def rotate_key(self):
        """
        Rotate encryption keys
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get Supabase URL
            supabase_url = os.getenv("SUPABASE_URL")
            
            # Check if we have a profile for this DB
            if supabase_url not in self.user_data['db_profiles']:
                print(f"No profile found for {supabase_url}")
                return False
            
            db_profile = self.user_data['db_profiles'][supabase_url]
            
            # Store current keypair in old keys if it exists
            if db_profile.get('current_keypair'):
                if 'old_keys' not in db_profile:
                    db_profile['old_keys'] = []
                
                db_profile['old_keys'].append(db_profile['current_keypair'])
            
            # Generate new keypair
            private_key = PrivateKey.generate()
            public_key = private_key.public_key
            
            # Store new keypair
            db_profile['current_keypair'] = {
                "private_key": Base64Encoder.encode(bytes(private_key)).decode('utf-8'),
                "public_key": Base64Encoder.encode(bytes(public_key)).decode('utf-8'),
                "created_at": get_timestamp()
            }
            
            # Update identity keys as well
            identity_private_key = PrivateKey.generate()
            identity_public_key = identity_private_key.public_key
            
            self.user_data['identity_private_key'] = Base64Encoder.encode(bytes(identity_private_key)).decode('utf-8')
            self.user_data['identity_public_key'] = Base64Encoder.encode(bytes(identity_public_key)).decode('utf-8')
            
            # Update public key in database
            success = self.db_manager.update_public_key(
                self.username, 
                self.user_data['identity_public_key']
            )
            
            if not success:
                print("Failed to update public key in database.")
                return False
            
            # Save updated user data
            password = getpass.getpass("Enter password to save updated keys: ")
            
            # Convert user data to JSON
            json_data = json.dumps(self.user_data, indent=2).encode('utf-8')
            
            # Encrypt user data
            encrypted_data = flightcode.CryptoService.encrypt_data(json_data, password)
            
            # Save encrypted data
            with open(self.profile_path, 'wb') as f:
                f.write(encrypted_data)
            
            return True
        except Exception as e:
            print(f"Error rotating keys: {e}")
            return False
    
    def check_key_rotation_needed(self):
        """
        Check if key rotation is needed
        
        Returns:
            True if rotation is needed, False otherwise
        """
        try:
            # Get Supabase URL
            supabase_url = os.getenv("SUPABASE_URL")
            
            # Check if we have a profile for this DB
            if supabase_url not in self.user_data['db_profiles']:
                return False
            
            db_profile = self.user_data['db_profiles'][supabase_url]
            
            # Check if we have a current keypair
            if not db_profile.get('current_keypair'):
                return True
            
            # Check if keypair is older than 1 day
            created_at = db_profile['current_keypair']['created_at']
            current_time = get_timestamp()
            
            # Simple time comparison (not perfect but works for this example)
            # In a real app, parse timestamps and compare properly
            day_ago = current_time.split(' ')[0]  # Just compare date part
            created_date = created_at.split(' ')[0]
            
            return created_date != day_ago
        except Exception as e:
            print(f"Error checking key rotation: {e}")
            return False
