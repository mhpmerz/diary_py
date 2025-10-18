#!/usr/bin/env python3
"""
Launcher script for the Diary Application
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main application
from main.main import DiaryApp

if __name__ == "__main__":
    app = DiaryApp()
    app.run()
