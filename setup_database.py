#!/usr/bin/env python3
"""
Database Setup Utility
Helps set up the required database tables
"""

import os
import sys
from dotenv import load_dotenv
from supabase import create_client
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def setup_database():
    """Set up the database tables"""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get Supabase credentials
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            print(Fore.RED + "[!] Supabase credentials not found in .env file.")
            print(Fore.YELLOW + "[*] Please create a .env file with:")
            print("SUPABASE_URL=your_supabase_url")
            print("SUPABASE_KEY=your_supabase_key")
            return False
        
        print(Fore.YELLOW + "[*] Connecting to Supabase...")
        
        # Create Supabase client
        supabase = create_client(supabase_url, supabase_key)
        
        print(Fore.GREEN + "[+] Connected to Supabase successfully!")
        
        # Create tables
        print(Fore.YELLOW + "[*] Creating database tables...")
        
        # Create users_public_keys table
        try:
            # Try to insert a test record to create the table
            supabase.table("users_public_keys").insert({
                "username": "setup_test_user",
                "public_key": "setup_test_key",
                "updated_at": "2024-01-01 00:00:00"
            }).execute()
            
            # Delete the test record
            supabase.table("users_public_keys").delete().eq("username", "setup_test_user").execute()
            
            print(Fore.GREEN + "[+] users_public_keys table created/verified!")
            
        except Exception as e:
            print(Fore.RED + f"[!] Error with users_public_keys table: {e}")
        
        # Create message_log table
        try:
            # Try to insert a test record to create the table
            supabase.table("message_log").insert({
                "sender_username": "setup_test_sender",
                "recipient_username": "setup_test_recipient",
                "ciphertext": "setup_test_message",
                "timestamp": "2024-01-01 00:00:00"
            }).execute()
            
            # Delete the test record
            supabase.table("message_log").delete().eq("sender_username", "setup_test_sender").execute()
            
            print(Fore.GREEN + "[+] message_log table created/verified!")
            
        except Exception as e:
            print(Fore.RED + f"[!] Error with message_log table: {e}")
        
        # Test the tables
        print(Fore.YELLOW + "[*] Testing database tables...")
        
        try:
            # Test users table
            users_response = supabase.table("users_public_keys").select("*").limit(1).execute()
            print(Fore.GREEN + "[+] users_public_keys table is working!")
            
            # Test messages table
            messages_response = supabase.table("message_log").select("*").limit(1).execute()
            print(Fore.GREEN + "[+] message_log table is working!")
            
            print(Fore.GREEN + "\n[+] Database setup completed successfully!")
            print(Fore.CYAN + "[*] You can now run the chat application with: python main.py")
            
            return True
            
        except Exception as e:
            print(Fore.RED + f"[!] Error testing tables: {e}")
            return False
            
    except Exception as e:
        print(Fore.RED + f"[!] Error setting up database: {e}")
        return False

def main():
    """Main function"""
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + "  Encrypted Chat App - Database Setup")
    print(Fore.CYAN + "=" * 50)
    
    success = setup_database()
    
    if success:
        print(Fore.GREEN + "\n[+] Setup completed successfully!")
    else:
        print(Fore.RED + "\n[!] Setup failed. Please check the errors above.")
        print(Fore.YELLOW + "\n[*] Manual setup instructions:")
        print("1. Go to your Supabase dashboard")
        print("2. Go to the SQL Editor")
        print("3. Run the SQL commands from create_tables.sql")

if __name__ == "__main__":
    main()
