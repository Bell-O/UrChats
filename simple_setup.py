#!/usr/bin/env python3
"""
Simple Database Setup
Creates tables using direct SQL execution
"""

import os
import sys
from dotenv import load_dotenv
from supabase import create_client
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def create_tables_with_sql():
    """Create tables using raw SQL"""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get Supabase credentials
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            print(Fore.RED + "[!] Supabase credentials not found in .env file.")
            return False
        
        print(Fore.YELLOW + "[*] Connecting to Supabase...")
        
        # Create Supabase client
        supabase = create_client(supabase_url, supabase_key)
        
        print(Fore.GREEN + "[+] Connected to Supabase successfully!")
        
        # SQL to create tables
        create_users_table = """
        CREATE TABLE IF NOT EXISTS public.users_public_keys (
            username TEXT PRIMARY KEY,
            public_key TEXT NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        create_messages_table = """
        CREATE TABLE IF NOT EXISTS public.message_log (
            message_id BIGSERIAL PRIMARY KEY,
            sender_username TEXT NOT NULL,
            recipient_username TEXT NOT NULL,
            ciphertext TEXT NOT NULL,
            timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        create_indexes = """
        CREATE INDEX IF NOT EXISTS idx_message_log_recipient 
        ON public.message_log(recipient_username);
        
        CREATE INDEX IF NOT EXISTS idx_message_log_sender 
        ON public.message_log(sender_username);
        
        CREATE INDEX IF NOT EXISTS idx_message_log_timestamp 
        ON public.message_log(timestamp DESC);
        """
        
        enable_rls = """
        ALTER TABLE public.users_public_keys ENABLE ROW LEVEL SECURITY;
        ALTER TABLE public.message_log ENABLE ROW LEVEL SECURITY;
        """
        
        create_policies = """
        CREATE POLICY IF NOT EXISTS "Allow all operations on users_public_keys" 
        ON public.users_public_keys FOR ALL 
        TO authenticated, anon 
        USING (true) 
        WITH CHECK (true);
        
        CREATE POLICY IF NOT EXISTS "Allow all operations on message_log" 
        ON public.message_log FOR ALL 
        TO authenticated, anon 
        USING (true) 
        WITH CHECK (true);
        """
        
        print(Fore.YELLOW + "[*] Creating users_public_keys table...")
        try:
            result = supabase.rpc('exec_sql', {'sql': create_users_table}).execute()
            print(Fore.GREEN + "[+] users_public_keys table created!")
        except Exception as e:
            print(Fore.YELLOW + f"[*] Table creation via RPC failed: {e}")
            print(Fore.YELLOW + "[*] This is normal - tables might already exist or RPC is disabled")
        
        print(Fore.YELLOW + "[*] Creating message_log table...")
        try:
            result = supabase.rpc('exec_sql', {'sql': create_messages_table}).execute()
            print(Fore.GREEN + "[+] message_log table created!")
        except Exception as e:
            print(Fore.YELLOW + f"[*] Table creation via RPC failed: {e}")
        
        # Test if tables exist by trying to query them
        print(Fore.YELLOW + "[*] Testing table access...")
        
        try:
            # Test users table
            result = supabase.table("users_public_keys").select("*").limit(1).execute()
            print(Fore.GREEN + "[+] users_public_keys table is accessible!")
            
            # Test messages table  
            result = supabase.table("message_log").select("*").limit(1).execute()
            print(Fore.GREEN + "[+] message_log table is accessible!")
            
            print(Fore.GREEN + "\n[+] Database setup completed successfully!")
            return True
            
        except Exception as e:
            print(Fore.RED + f"[!] Tables are not accessible: {e}")
            print(Fore.YELLOW + "\n[*] Manual setup required:")
            print("1. Go to your Supabase dashboard")
            print("2. Navigate to SQL Editor")
            print("3. Copy and paste the SQL from 'manual_setup.sql'")
            print("4. Run the SQL to create the tables")
            return False
            
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")
        return False

def main():
    """Main function"""
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + "  Simple Database Setup")
    print(Fore.CYAN + "=" * 50)
    
    success = create_tables_with_sql()
    
    if not success:
        print(Fore.YELLOW + "\n" + "=" * 50)
        print(Fore.YELLOW + "MANUAL SETUP INSTRUCTIONS:")
        print(Fore.YELLOW + "=" * 50)
        print("1. Open your Supabase dashboard")
        print("2. Go to SQL Editor")
        print("3. Copy the SQL from 'manual_setup.sql'")
        print("4. Paste and run it in the SQL Editor")
        print("5. Then run this app again")

if __name__ == "__main__":
    main()
