#!/usr/bin/env python3
"""
UrChats.hee - Encrypted Chat Application
Your words, your keys, your world.

Made by Bell (github.com/Bell-O)
Support: https://ko-fi.com/bell_o
"""

import os
import sys
import getpass
import json
import time
import threading
from colorama import Fore, Style, init
import pyfiglet

# Import local modules
from login import LoginManager
from db_connect import DatabaseManager
from chat import ChatManager
from key_rotate import KeyRotationManager
from message_storage import MessageStorage
from utils import clear_screen, get_timestamp, save_json, load_json

# Initialize colorama
init(autoreset=True)

class Application:
    """Main application class"""
    
    def __init__(self):
        self.login_manager = LoginManager()
        self.db_manager = None
        self.chat_manager = None
        self.key_manager = None
        self.message_storage = None
        self.user_data = None
        self.user_password = None
        self.is_logged_in = False
    
    def display_banner(self):
        """Display application banner"""
        clear_screen()
        fig = pyfiglet.Figlet(font="slant")
        print(Fore.CYAN + fig.renderText("UrChats.hee"))
        print(Fore.YELLOW + "Your words, your keys, your world.")
        print(Fore.GREEN + "Made by Bell (github.com/Bell-O)")
        print(Fore.MAGENTA + "Support: https://ko-fi.com/bell_o")
        print(Fore.CYAN + "=" * 60)
    
    def check_env_file(self):
        """Check if .env file exists and prompt for Supabase credentials if not"""
        if not os.path.exists(".env"):
            print(Fore.YELLOW + "\n[!] No Supabase configuration found.")
            print(Fore.YELLOW + "[*] Please enter your Supabase credentials:")
            
            supabase_url = input(Fore.YELLOW + "[?] Supabase URL: ").strip()
            supabase_key = input(Fore.YELLOW + "[?] Supabase Key: ").strip()
            
            with open(".env", "w") as f:
                f.write(f"SUPABASE_URL={supabase_url}\n")
                f.write(f"SUPABASE_KEY={supabase_key}\n")
            
            print(Fore.GREEN + "[+] Supabase configuration saved.")
            
            # Ask if user wants to run database setup
            setup_db = input(Fore.YELLOW + "[?] Run database setup now? (y/n): ").lower()
            if setup_db == 'y':
                print(Fore.YELLOW + "[*] Running database setup...")
                try:
                    from setup_database import setup_database
                    setup_database()
                except Exception as e:
                    print(Fore.RED + f"[!] Database setup failed: {e}")
                    print(Fore.YELLOW + "[*] You can run 'python setup_database.py' later.")
    
    def initialize_managers(self):
        """Initialize all managers after successful login"""
        self.db_manager = DatabaseManager(self.user_data)
        
        # Check if database connection was successful
        if not self.db_manager.supabase:
            print(Fore.RED + "[!] Failed to connect to database.")
            print(Fore.YELLOW + "[*] You can:")
            print("1. Check your internet connection")
            print("2. Verify your Supabase credentials in .env file")
            print("3. Run 'python setup_database.py' to set up tables")
            
            retry = input(Fore.YELLOW + "[?] Try to continue anyway? (y/n): ").lower()
            if retry != 'y':
                return False
        
        self.chat_manager = ChatManager(self.user_data, self.db_manager)
        self.key_manager = KeyRotationManager(self.user_data, self.db_manager)
        
        # Initialize message storage
        if self.user_password:
            self.message_storage = MessageStorage(self.user_data['username'], self.user_password)
        
        return True
    
    def login_or_register(self):
        """Handle login or registration"""
        self.display_banner()
        
        # Check if user profile exists
        if not os.path.exists("user_profile.json.he"):
            print(Fore.YELLOW + "\n[*] No user profile found. Let's create one!")
            username = input(Fore.YELLOW + "[?] Enter username: ").strip()
            password = getpass.getpass(Fore.YELLOW + "[?] Enter password: ")
            confirm_password = getpass.getpass(Fore.YELLOW + "[?] Confirm password: ")
            
            if password != confirm_password:
                print(Fore.RED + "[!] Passwords do not match.")
                return False
            
            # Store password for message storage
            self.user_password = password
            
            # Register new user
            self.user_data = self.login_manager.register_user(username, password)
            if self.user_data:
                self.is_logged_in = True
                print(Fore.GREEN + "[+] Registration successful!")
                return True
            else:
                print(Fore.RED + "[!] Registration failed.")
                return False
        else:
            # Login existing user
            password = getpass.getpass(Fore.YELLOW + "[?] Enter password: ")
            
            # Store password for message storage
            self.user_password = password
            
            self.user_data = self.login_manager.login_user(password)
            
            if self.user_data:
                self.is_logged_in = True
                print(Fore.GREEN + f"[+] Welcome back, {self.user_data['username']}!")
                return True
            else:
                print(Fore.RED + "[!] Login failed. Incorrect password.")
                return False
    
    def main_menu(self):
        """Display and handle main menu"""
        while self.is_logged_in:
            clear_screen()
            self.display_banner()
            
            print(Fore.MAGENTA + "\nMain Menu:")
            print(Fore.CYAN + "  1. List users")
            print(Fore.CYAN + "  2. Start chat")
            print(Fore.CYAN + "  3. Rotate key")
            print(Fore.CYAN + "  4. Logout")
            print(Fore.CYAN + "  5. Credits & Support")
            print(Fore.RED + "  191. Emergency Data Wipe")
            
            choice = input(Fore.YELLOW + "\n[?] Select an option: ").strip()
            
            if choice == '1':
                self.list_users()
            elif choice == '2':
                self.start_chat()
            elif choice == '3':
                self.rotate_key()
            elif choice == '4':
                self.logout()
                break
            elif choice == '5':
                self.show_credits()
            elif choice == '191':
                self.emergency_wipe()
            else:
                print(Fore.RED + "\n[!] Invalid option. Please try again.")
                time.sleep(1)
    
    def emergency_wipe(self):
        """Emergency data wipe function"""
        clear_screen()
        print(Fore.RED + "⚠️  EMERGENCY DATA WIPE ⚠️")
        print(Fore.RED + "=" * 40)
        print(Fore.YELLOW + "This will permanently delete:")
        print(Fore.WHITE + "• User profile")
        print(Fore.WHITE + "• All stored messages")
        print(Fore.WHITE + "• All encryption keys")
        print(Fore.WHITE + "• All local data")
        print()
        
        confirm1 = input(Fore.RED + "[?] Type 'DELETE' to confirm: ").strip()
        if confirm1 != 'DELETE':
            print(Fore.GREEN + "[+] Operation cancelled.")
            time.sleep(2)
            return
        
        confirm2 = input(Fore.RED + "[?] Type your username to confirm: ").strip()
        if confirm2 != self.user_data['username']:
            print(Fore.GREEN + "[+] Operation cancelled.")
            time.sleep(2)
            return
        
        print(Fore.RED + "\n[!] Wiping all data...")
        
        try:
            # Delete user profile
            if os.path.exists("user_profile.json.he"):
                os.remove("user_profile.json.he")
                print(Fore.YELLOW + "[*] User profile deleted")
            
            # Delete message storage
            if self.message_storage:
                self.message_storage.clear_all_messages()
                print(Fore.YELLOW + "[*] Message storage cleared")
            
            # Delete any other user-specific files
            username = self.user_data['username']
            files_to_delete = [
                f"messages_{username}.hee",
                f"keys_{username}.hee",
                f"backup_{username}.hee"
            ]
            
            for file_path in files_to_delete:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(Fore.YELLOW + f"[*] Deleted {file_path}")
            
            print(Fore.GREEN + "\n[+] Emergency wipe completed successfully!")
            print(Fore.YELLOW + "[*] All user data has been permanently deleted.")
            print(Fore.YELLOW + "[*] Application will now exit.")
            
            time.sleep(3)
            sys.exit(0)
            
        except Exception as e:
            print(Fore.RED + f"[!] Error during wipe: {e}")
            time.sleep(2)
    
    def show_credits(self):
        """Display credits and support information"""
        clear_screen()
        print(Fore.CYAN + "=" * 60)
        print(Fore.CYAN + "  UrChats.hee - Credits & Support")
        print(Fore.CYAN + "=" * 60)
        print()
        print(Fore.GREEN + "🔐 UrChats.hee")
        print(Fore.YELLOW + "Your words, your keys, your world.")
        print()
        print(Fore.BLUE + "👨‍💻 Developer:")
        print(Fore.WHITE + "   Bell (github.com/Bell-O)")
        print()
        print(Fore.MAGENTA + "☕ Support the Developer:")
        print(Fore.WHITE + "   https://ko-fi.com/bell_o")
        print()
        print(Fore.CYAN + "🛡️ Features:")
        print(Fore.WHITE + "   • End-to-End Encryption")
        print(Fore.WHITE + "   • Secure Local Message Storage")
        print(Fore.WHITE + "   • Real-time Message Updates")
        print(Fore.WHITE + "   • Emergency Data Wipe (191)")
        print(Fore.WHITE + "   • Privacy-focused Design")
        print()
        print(Fore.YELLOW + "🔧 Built with:")
        print(Fore.WHITE + "   • Python & Supabase")
        print(Fore.WHITE + "   • NaCl Cryptography")
        print(Fore.WHITE + "   • FlightCode V2")
        print()
        input(Fore.YELLOW + "Press Enter to continue...")
    
    def list_users(self):
        """List all users from the database"""
        clear_screen()
        print(Fore.CYAN + "\nUser List:")
        
        users = self.db_manager.get_users()
        if not users:
            print(Fore.YELLOW + "[*] No users found or couldn't connect to database.")
        else:
            for idx, user in enumerate(users):
                if user['username'] == self.user_data['username']:
                    print(Fore.GREEN + f"  {idx + 1}. {user['username']} (You)")
                else:
                    print(Fore.CYAN + f"  {idx + 1}. {user['username']}")
        
        input(Fore.YELLOW + "\nPress Enter to continue...")
    
    def start_chat(self):
        """Start the interactive chat interface"""
        clear_screen()
        print(Fore.CYAN + "\nSelect Chat Partner:")
        
        # Get list of users
        users = self.db_manager.get_users()
        if not users:
            print(Fore.YELLOW + "[*] No users found or couldn't connect to database.")
            input(Fore.YELLOW + "\nPress Enter to continue...")
            return
        
        # Filter out current user
        other_users = [user for user in users if user['username'] != self.user_data['username']]
        
        if not other_users:
            print(Fore.YELLOW + "[*] No other users found to chat with.")
            input(Fore.YELLOW + "\nPress Enter to continue...")
            return
        
        # Display other users
        print(Fore.CYAN + "\nAvailable Users:")
        for idx, user in enumerate(other_users):
            print(Fore.CYAN + f"  {idx + 1}. {user['username']}")
        
        # Select chat partner
        try:
            choice = int(input(Fore.YELLOW + "\n[?] Select chat partner (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(other_users):
                chat_partner = other_users[choice - 1]
                self.chat_interface(chat_partner)
            else:
                print(Fore.RED + "[!] Invalid selection.")
                time.sleep(1)
        except ValueError:
            print(Fore.RED + "[!] Please enter a valid number.")
            time.sleep(1)

    def chat_interface(self, chat_partner):
        """Interactive chat interface with working real-time updates"""
        import queue
        import select
        
        # Chat state
        input_queue = queue.Queue()
        stop_chat = threading.Event()
        displayed_message_ids = set()
        last_message_count = 0
        
        def get_new_messages():
            """Get new messages from database"""
            try:
                # Get messages from database
                db_messages = self.chat_manager.receive_messages()
                partner_messages = [
                    msg for msg in db_messages 
                    if msg['sender_username'] == chat_partner['username']
                ]
            
                new_messages = []
                for msg in partner_messages:
                    msg_id = f"db_{msg['sender_username']}_{msg['timestamp']}"
                    if msg_id not in displayed_message_ids:
                        # Save to local storage
                        if self.message_storage:
                            self.message_storage.add_message(
                                msg['sender_username'],
                                self.user_data['username'],
                                msg['decrypted_content'],
                                'received'
                            )
                    
                        new_messages.append({
                            'sender': msg['sender_username'],
                            'content': msg['decrypted_content'],
                            'timestamp': msg['timestamp'],
                            'type': 'received',
                            'id': msg_id
                        })
                        displayed_message_ids.add(msg_id)
            
                return new_messages
            except Exception as e:
                print(f"Error getting messages: {e}")
                return []
    
        def display_chat_screen():
            """Display the complete chat screen"""
            clear_screen()

            # Header with online status
            print(Fore.CYAN + "=" * 70)
            print(Fore.CYAN + f"  💬 Chat with {chat_partner['username']}")
            print(Fore.GREEN + f"  🟢 {chat_partner['username']} is online")
            print(Fore.GREEN + f"  🟢 FlightCode is Online")
            print(Fore.CYAN + f"  🔒 End-to-end encrypted • Auto-refresh every 3s")
            print(Fore.CYAN + "=" * 70)
            print(Fore.YELLOW + "Commands: 'quit' to exit, 'clear' to clear, 'refresh' to update")
            print(Fore.CYAN + "-" * 70)
        
            # Get stored messages
            if self.message_storage:
                stored_messages = self.message_storage.get_chat_messages(chat_partner['username'], 15)
            
                if stored_messages:
                    print(Fore.GREEN + f"📝 Chat History ({len(stored_messages)} recent messages):")
                    print()
                
                    for msg in stored_messages:
                        timestamp = msg['timestamp']
                        content = msg['content']
                        msg_type = msg['type']
                    
                        # Format timestamp
                        try:
                            if 'T' in timestamp:
                                time_part = timestamp.split('T')[1].split('.')[0]
                            else:
                                time_part = timestamp.split(' ')[1] if ' ' in timestamp else timestamp
                        except:
                            time_part = timestamp
                    
                        if msg_type == 'sent':
                            print(Fore.GREEN + f"  [{time_part}] You: {content}")
                        else:
                            print(Fore.BLUE + f"  [{time_part}] {msg['sender']}: {content}")
                else:
                    print(Fore.YELLOW + "📝 No messages yet. Start chatting!")
            else:
                print(Fore.YELLOW + "📝 Message storage not available.")
        
            print(Fore.CYAN + "-" * 70)
    
        def check_messages_periodically():
            """Check for new messages every 3 seconds"""
            while not stop_chat.is_set():
                try:
                    time.sleep(3)
                    if not stop_chat.is_set():
                        new_messages = get_new_messages()
                        if new_messages:
                            # Display new messages immediately
                            print(f"\n{Fore.GREEN}🔔 {len(new_messages)} new message(s)")
                            for msg in new_messages:
                                timestamp = msg['timestamp']
                                try:
                                    if 'T' in timestamp:
                                        time_part = timestamp.split('T')[1].split('.')[0]
                                    else:
                                        time_part = timestamp.split(' ')[1] if ' ' in timestamp else timestamp
                                except:
                                    time_part = timestamp
                            
                                print(Fore.BLUE + f"  [{time_part}] {msg['sender']}: {msg['content']}")
                        
                            print(Fore.WHITE + f"💬 Message to {chat_partner['username']}: ", end='', flush=True)
                except Exception as e:
                    if not stop_chat.is_set():
                        print(f"Error checking messages: {e}")
                    break
    
        # Start message checking thread
        message_thread = threading.Thread(target=check_messages_periodically, daemon=True)
        message_thread.start()
    
        # Initial display
        display_chat_screen()

        # Show connection status (clean format)
        print(Fore.GREEN + f"🟢 You are now chatting with {chat_partner['username']}")
        print(Fore.GREEN + f"🟢 FlightCode is Online")
        print()
    
        try:
            while not stop_chat.is_set():
                try:
                    print(Fore.WHITE + f"💬 Message to {chat_partner['username']}: ", end='', flush=True)
                    user_input = input().strip()
                
                    if not user_input:
                        continue
                
                    # Handle user commands
                    if user_input.lower() in ['quit', '/quit', 'exit']:
                        break
                    elif user_input.lower() in ['clear', '/clear']:
                        display_chat_screen()
                        continue
                    elif user_input.lower() in ['refresh', '/refresh', 'r']:
                        new_messages = get_new_messages()
                        display_chat_screen()
                        if new_messages:
                            print(Fore.GREEN + f"🔄 Found {len(new_messages)} new messages!")
                            for msg in new_messages:
                                timestamp = msg['timestamp']
                                try:
                                    if 'T' in timestamp:
                                        time_part = timestamp.split('T')[1].split('.')[0]
                                    else:
                                        time_part = timestamp.split(' ')[1] if ' ' in timestamp else timestamp
                                except:
                                    time_part = timestamp
                                print(Fore.BLUE + f"  [{time_part}] {msg['sender']}: {msg['content']}")
                        else:
                            print(Fore.YELLOW + "🔄 No new messages found.")
                        continue
                    elif user_input.lower() in ['help', '/help']:
                        print(Fore.YELLOW + "\n📋 Commands:")
                        print(Fore.YELLOW + "  quit - Exit chat")
                        print(Fore.YELLOW + "  clear - Clear and refresh screen")
                        print(Fore.YELLOW + "  refresh - Manual refresh")
                        print(Fore.YELLOW + "  help - Show this help")
                        continue
                
                    # Send message
                    if user_input.strip():
                        try:
                            success = self.chat_manager.send_message(
                                chat_partner['username'], 
                                chat_partner['public_key'], 
                                user_input
                            )
                            
                            if success:
                                timestamp = get_timestamp()
                                
                                # Save sent message to local storage (silent)
                                if self.message_storage:
                                    self.message_storage.add_message(
                                        self.user_data['username'],
                                        chat_partner['username'],
                                        user_input,
                                        'sent'
                                    )
                                
                                # Show sent message immediately (clean format)
                                try:
                                    if 'T' in timestamp:
                                        time_part = timestamp.split('T')[1].split('.')[0]
                                    else:
                                        time_part = timestamp.split(' ')[1] if ' ' in timestamp else timestamp
                                except:
                                    time_part = timestamp
                                
                                print(Fore.GREEN + f"  [{time_part}] You: {user_input}")
                            else:
                                print(Fore.RED + "❌ Failed to send message")
                            
                        except Exception as e:
                            print(Fore.RED + f"❌ Error sending message: {e}")
                
                except KeyboardInterrupt:
                    break
                except EOFError:
                    break
                except Exception as e:
                    print(Fore.RED + f"❌ Input error: {e}")
                    time.sleep(1)
        
        except Exception as e:
            print(Fore.RED + f"❌ Chat interface error: {e}")
        finally:
            stop_chat.set()
            print(Fore.YELLOW + f"\n🔴 {self.user_data['username']} left the chat")
            print(Fore.YELLOW + f"👋 Chat with {chat_partner['username']} ended")
            time.sleep(2)
    
    def rotate_key(self):
        """Rotate encryption keys"""
        clear_screen()
        print(Fore.CYAN + "\nKey Rotation:")
        
        confirm = input(Fore.YELLOW + "[?] Rotate your encryption key? This will update your public key. (y/n): ")
        
        if confirm.lower() == 'y':
            success = self.key_manager.rotate_key()
            
            if success:
                print(Fore.GREEN + "[+] Key rotated successfully!")
                # Update user data with new keys
                self.user_data = self.login_manager.get_user_data()
            else:
                print(Fore.RED + "[!] Failed to rotate key.")
        
        input(Fore.YELLOW + "\nPress Enter to continue...")
    
    def logout(self):
        """Log out the current user"""
        self.is_logged_in = False
        self.user_data = None
        self.user_password = None
        self.db_manager = None
        self.chat_manager = None
        self.key_manager = None
        self.message_storage = None
        
        print(Fore.GREEN + "[+] Logged out successfully.")
    
    def run(self):
        """Run the application"""
        try:
            if self.login_or_register():
                self.check_env_file()
                if self.initialize_managers():
                    self.main_menu()
                else:
                    print(Fore.RED + "[!] Failed to initialize application.")
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n[*] Application terminated by user.")
        except Exception as e:
            print(Fore.RED + f"\n[!] An error occurred: {e}")
        finally:
            print(Fore.YELLOW + "\n[*] Goodbye!")


if __name__ == "__main__":
    app = Application()
    app.run()
