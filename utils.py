#!/usr/bin/env python3
"""
Utility functions
"""

import os
import sys
import json
import time
from datetime import datetime

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_timestamp():
    """
    Get current timestamp in ISO format
    
    Returns:
        Timestamp string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_json(data, file_path):
    """
    Save data to JSON file
    
    Args:
        data: Data to save
        file_path: Path to save to
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving JSON: {e}")
        return False

def load_json(file_path):
    """
    Load data from JSON file
    
    Args:
        file_path: Path to load from
        
    Returns:
        Loaded data if successful, None otherwise
    """
    try:
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return None

def print_progress(message, delay=0.05):
    """
    Print a progress message with animation
    
    Args:
        message: Message to print
        delay: Delay between dots
    """
    sys.stdout.write(message)
    for _ in range(3):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
