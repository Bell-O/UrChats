#!/usr/bin/env python3
"""
Test Supabase Connection
Simple script to test if Supabase connection works
"""

import os
from dotenv import load_dotenv
from supabase import create_client
from colorama import Fore, init

init(autoreset=True)

def test_connection():
    """Test the Supabase connection"""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get credentials
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        print(f"URL: {supabase_url}")
        print(f"Key: {supabase_key[:20]}...")
        
        if not supabase_url or not supabase_key:
            print(Fore.RED + "[!] Missing credentials")
            return False
        
        # Create client
        supabase = create_client(supabase_url, supabase_key)
        
        # Test connection
        print(Fore.YELLOW + "[*] Testing connection...")
        
        # Try to access auth (this should always work)
        session = supabase.auth.get_session()
        print(Fore.GREEN + "[+] Basic connection works!")
        
        # Try to access tables
        try:
            result = supabase.table("users_public_keys").select("*").limit(1).execute()
            print(Fore.GREEN + "[+] users_public_keys table exists!")
        except Exception as e:
            print(Fore.RED + f"[!] users_public_keys table error: {e}")
        
        try:
            result = supabase.table("message_log").select("*").limit(1).execute()
            print(Fore.GREEN + "[+] message_log table exists!")
        except Exception as e:
            print(Fore.RED + f"[!] message_log table error: {e}")
        
        return True
        
    except Exception as e:
        print(Fore.RED + f"[!] Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
