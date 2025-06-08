#!/usr/bin/env python3
"""
Database Manager
Handles connections to Supabase and database operations
"""

import os
import sys
import json
import time
from dotenv import load_dotenv
from supabase import create_client, Client
from nacl.encoding import Base64Encoder
from utils import get_timestamp

class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, user_data):
        """
        Initialize the database manager
        
        Args:
            user_data: User data dictionary
        """
        self.user_data = user_data
        self.username = user_data['username']
        self.supabase = self._connect_to_supabase()
        
        # Initialize database if needed
        if self.supabase:
            self._initialize_database()
            self._register_user_key()
    
    def _connect_to_supabase(self):
        """
        Connect to Supabase
        
        Returns:
            Supabase client if successful, None otherwise
        """
        try:
            # Load environment variables
            load_dotenv()
        
            # Get Supabase credentials
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_KEY")
        
            if not supabase_url or not supabase_key:
                print("Supabase credentials not found in .env file.")
                print("Please make sure your .env file contains:")
                print("SUPABASE_URL=your_supabase_url")
                print("SUPABASE_KEY=your_supabase_key")
                return None
        
            # Create Supabase client
            supabase = create_client(supabase_url, supabase_key)
        
            # Test connection with a simple query
            try:
                # Try to query the auth users (this should always work)
                response = supabase.auth.get_session()
                print("Successfully connected to Supabase!")
            except Exception as test_error:
                print(f"Connection test failed: {test_error}")
                print("Please check your Supabase URL and key.")
                return None
        
            # Store Supabase URL in user_data if not already there
            if supabase_url not in self.user_data.get('db_profiles', {}):
                self.user_data['db_profiles'][supabase_url] = {
                    "current_keypair": None,
                    "old_keys": []
                }
        
            return supabase
        except Exception as e:
            print(f"Error connecting to Supabase: {e}")
            print("Please check your internet connection and Supabase credentials.")
            return None
    
    def _initialize_database(self):
        """Initialize database tables if they don't exist"""
        try:
            # First, try to query existing tables
            try:
                self.supabase.table("users_public_keys").select("*").limit(1).execute()
                self.supabase.table("message_log").select("*").limit(1).execute()
                print("Database tables already exist.")
                return
            except Exception:
                print("Tables don't exist. Creating them...")
        
            # Create users_public_keys table
            create_users_table_sql = """
            CREATE TABLE IF NOT EXISTS users_public_keys (
                username TEXT PRIMARY KEY,
                public_key TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT NOW()
            );
            """
        
            # Create message_log table
            create_messages_table_sql = """
            CREATE TABLE IF NOT EXISTS message_log (
                message_id SERIAL PRIMARY KEY,
                sender_username TEXT NOT NULL,
                recipient_username TEXT NOT NULL,
                ciphertext TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT NOW()
            );
            """
        
            # Execute SQL commands
            try:
                # Use RPC to execute raw SQL
                self.supabase.rpc('create_tables', {
                    'users_sql': create_users_table_sql,
                    'messages_sql': create_messages_table_sql
                }).execute()
                print("Database tables created successfully using RPC.")
            except Exception as rpc_error:
                print(f"RPC method failed: {rpc_error}")
                print("Trying alternative table creation method...")
            
                # Alternative: Try to create tables by inserting dummy data
                try:
                    # Try to create users table by inserting and then deleting
                    self.supabase.table("users_public_keys").insert({
                        "username": "dummy_user_delete_me",
                        "public_key": "dummy_key",
                        "updated_at": get_timestamp()
                    }).execute()
                
                    # Delete the dummy record
                    self.supabase.table("users_public_keys").delete().eq("username", "dummy_user_delete_me").execute()
                
                    # Try to create messages table
                    self.supabase.table("message_log").insert({
                        "sender_username": "dummy_sender",
                        "recipient_username": "dummy_recipient", 
                        "ciphertext": "dummy_message",
                        "timestamp": get_timestamp()
                    }).execute()
                
                    # Delete the dummy record
                    self.supabase.table("message_log").delete().eq("sender_username", "dummy_sender").execute()
                
                    print("Database tables created successfully using insert method.")
                
                except Exception as insert_error:
                    print(f"Insert method also failed: {insert_error}")
                    print("Please create the tables manually in your Supabase dashboard:")
                    print("\n1. users_public_keys table:")
                    print("   - username (text, primary key)")
                    print("   - public_key (text)")
                    print("   - updated_at (timestamp)")
                    print("\n2. message_log table:")
                    print("   - message_id (int8, primary key, auto-increment)")
                    print("   - sender_username (text)")
                    print("   - recipient_username (text)")
                    print("   - ciphertext (text)")
                    print("   - timestamp (timestamp)")
                
        except Exception as e:
            print(f"Error initializing database: {e}")
    
    def _register_user_key(self):
        """Register or update user's public key in the database"""
        try:
            # Check if user exists
            response = self.supabase.table("users_public_keys").select("*").eq("username", self.username).execute()
            
            # Get public key
            public_key = self.user_data['identity_public_key']
            
            if response.data:
                # User exists, update public key
                self.supabase.table("users_public_keys").update({
                    "public_key": public_key,
                    "updated_at": get_timestamp()
                }).eq("username", self.username).execute()
            else:
                # User doesn't exist, insert new record
                self.supabase.table("users_public_keys").insert({
                    "username": self.username,
                    "public_key": public_key,
                    "updated_at": get_timestamp()
                }).execute()
        except Exception as e:
            print(f"Error registering user key: {e}")
    
    def get_users(self):
        """
        Get list of users from the database
        
        Returns:
            List of users if successful, empty list otherwise
        """
        if not self.supabase:
            print("No database connection available.")
            return []
    
        try:
            response = self.supabase.table("users_public_keys").select("*").execute()
        
            # Filter out system user and dummy users
            users = [user for user in response.data if user['username'] not in ['system', 'dummy_user_delete_me']]
        
            return users
        except Exception as e:
            print(f"Error getting users: {e}")
            print("This might mean the tables don't exist yet.")
            return []
    
    def get_user_public_key(self, username):
        """
        Get public key for a specific user
        
        Args:
            username: Username to get public key for
            
        Returns:
            Public key if found, None otherwise
        """
        try:
            response = self.supabase.table("users_public_keys").select("public_key").eq("username", username).execute()
            
            if response.data:
                return response.data[0]['public_key']
            else:
                return None
        except Exception as e:
            print(f"Error getting user public key: {e}")
            return None
    
    def send_message(self, sender, recipient, ciphertext):
        """
        Send an encrypted message
        
        Args:
            sender: Sender username
            recipient: Recipient username
            ciphertext: Encrypted message
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.supabase.table("message_log").insert({
                "sender_username": sender,
                "recipient_username": recipient,
                "ciphertext": ciphertext,
                "timestamp": get_timestamp()
            }).execute()
            
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
    
    def get_messages(self, username):
        """
        Get messages for a specific user
        
        Args:
            username: Username to get messages for
            
        Returns:
            List of messages if successful, empty list otherwise
        """
        try:
            response = self.supabase.table("message_log").select("*").eq("recipient_username", username).execute()
            
            # Filter out system messages
            messages = [msg for msg in response.data if msg['sender_username'] != 'system']
            
            return messages
        except Exception as e:
            print(f"Error getting messages: {e}")
            return []
    
    def update_public_key(self, username, public_key):
        """
        Update public key for a user
        
        Args:
            username: Username to update public key for
            public_key: New public key
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.supabase.table("users_public_keys").update({
                "public_key": public_key,
                "updated_at": get_timestamp()
            }).eq("username", username).execute()
            
            return True
        except Exception as e:
            print(f"Error updating public key: {e}")
            return False

    def get_messages_between_users(self, sender, recipient):
        """
        Get messages between two specific users
        
        Args:
            sender: Sender username
            recipient: Recipient username
            
        Returns:
            List of messages if successful, empty list otherwise
        """
        try:
            response = self.supabase.table("message_log").select("*").eq("sender_username", sender).eq("recipient_username", recipient).order("timestamp", desc=False).execute()
            
            return response.data
        except Exception as e:
            print(f"Error getting messages between users: {e}")
            return []

    def get_recent_messages(self, username, limit=50):
        """
        Get recent messages for a user with limit
        
        Args:
            username: Username to get messages for
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of messages if successful, empty list otherwise
        """
        try:
            response = self.supabase.table("message_log").select("*").eq("recipient_username", username).order("timestamp", desc=True).limit(limit).execute()
            
            # Reverse to get chronological order
            messages = response.data[::-1]
            
            # Filter out system messages
            messages = [msg for msg in messages if msg['sender_username'] != 'system']
            
            return messages
        except Exception as e:
            print(f"Error getting recent messages: {e}")
            return []
