#!/usr/bin/env python3
"""
Login Manager
Handles user login, registration, and profile management
"""

import os
import sys
import json
import getpass
import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box
from nacl.encoding import Base64Encoder
import flightcodev2CLI as flightcode
from utils import get_timestamp, save_json, load_json

class LoginManager:
    """Manages user login and registration"""
    
    def __init__(self):
        """Initialize the login manager"""
        self.profile_path = "user_profile.json.he"
    
    def register_user(self, username, password):
        """
        Register a new user
        
        Args:
            username: Username for the new user
            password: Password for encryption
            
        Returns:
            User data dictionary if successful, None otherwise
        """
        try:
            # Generate identity keypair
            identity_private_key = PrivateKey.generate()
            identity_public_key = identity_private_key.public_key
            
            # Create user profile
            user_data = {
                "username": username,
                "identity_public_key": Base64Encoder.encode(bytes(identity_public_key)).decode('utf-8'),
                "identity_private_key": Base64Encoder.encode(bytes(identity_private_key)).decode('utf-8'),
                "db_profiles": {}
            }
            
            # Save user profile
            self._save_user_profile(user_data, password)
            
            return user_data
        except Exception as e:
            print(f"Error during registration: {e}")
            return None
    
    def login_user(self, password):
        """
        Login an existing user
        
        Args:
            password: Password for decryption
            
        Returns:
            User data dictionary if successful, None otherwise
        """
        try:
            # Check if profile exists
            if not os.path.exists(self.profile_path):
                print("No user profile found.")
                return None
            
            # Decrypt and load user profile
            encrypted_data = open(self.profile_path, 'rb').read()
            
            try:
                decrypted_data = flightcode.CryptoService.decrypt_data(encrypted_data, password)
                user_data = json.loads(decrypted_data.decode('utf-8'))
                return user_data
            except Exception as e:
                print(f"Decryption error: {e}")
                return None
        except Exception as e:
            print(f"Error during login: {e}")
            return None
    
    def get_user_data(self):
        """
        Get the current user data
        
        Returns:
            User data dictionary if available, None otherwise
        """
        try:
            if not os.path.exists(self.profile_path):
                return None
            
            # Ask for password
            password = getpass.getpass("Enter password to access user data: ")
            
            # Decrypt and load user profile
            encrypted_data = open(self.profile_path, 'rb').read()
            
            try:
                decrypted_data = flightcode.CryptoService.decrypt_data(encrypted_data, password)
                user_data = json.loads(decrypted_data.decode('utf-8'))
                return user_data
            except Exception as e:
                print(f"Decryption error: {e}")
                return None
        except Exception as e:
            print(f"Error getting user data: {e}")
            return None
    
    def update_user_data(self, user_data, password=None):
        """
        Update the user profile
        
        Args:
            user_data: Updated user data dictionary
            password: Password for encryption (will prompt if None)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if password is None:
                password = getpass.getpass("Enter password to update user data: ")
            
            # Save user profile
            self._save_user_profile(user_data, password)
            
            return True
        except Exception as e:
            print(f"Error updating user data: {e}")
            return False
    
    def _save_user_profile(self, user_data, password):
        """
        Save and encrypt user profile
        
        Args:
            user_data: User data dictionary
            password: Password for encryption
        """
        # Convert user data to JSON
        json_data = json.dumps(user_data, indent=2).encode('utf-8')
        
        # Encrypt user data
        encrypted_data = flightcode.CryptoService.encrypt_data(json_data, password)
        
        # Save encrypted data
        with open(self.profile_path, 'wb') as f:
            f.write(encrypted_data)
