#!/usr/bin/env python3
"""
Input Handler
Handles non-blocking input for the chat interface
"""

import sys
import select
import threading
import queue
import time

class NonBlockingInput:
    """Non-blocking input handler for chat interface"""
    
    def __init__(self):
        self.input_queue = queue.Queue()
        self.input_thread = None
        self.stop_event = threading.Event()
    
    def start(self):
        """Start the input handler"""
        self.input_thread = threading.Thread(target=self._input_worker, daemon=True)
        self.input_thread.start()
    
    def stop(self):
        """Stop the input handler"""
        self.stop_event.set()
    
    def get_input(self, timeout=0.1):
        """
        Get input with timeout
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            Input string or None if no input
        """
        try:
            return self.input_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def _input_worker(self):
        """Worker thread for input handling"""
        while not self.stop_event.is_set():
            try:
                if hasattr(select, 'select'):
                    # Unix/Linux/Mac
                    ready, _, _ = select.select([sys.stdin], [], [], 0.1)
                    if ready:
                        line = sys.stdin.readline().strip()
                        if line:
                            self.input_queue.put(line)
                else:
                    # Windows fallback
                    line = input()
                    if line:
                        self.input_queue.put(line)
            except Exception:
                time.sleep(0.1)
