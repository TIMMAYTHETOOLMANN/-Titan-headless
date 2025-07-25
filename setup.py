#!/usr/bin/env python3
"""
Titan Headless Setup Script
Legacy compatibility setup for StreamBoost Python version
"""

import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Python dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    
    # Install Playwright browsers
    try:
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        print("✅ Playwright browsers installed")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Failed to install Playwright browsers: {e}")
    
    return True

def create_directories():
    """Create necessary directories"""
    dirs = ['./profiles', './logs']
    for dir_path in dirs:
        Path(dir_path).mkdir(exist_ok=True)
    print("✅ Directories created")

def main():
    print("Titan Headless - StreamBoost Setup")
    print("==================================")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version} detected")
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    print("\n✅ Setup completed!")
    print("\nAvailable scripts:")
    print("  python3 streamboost.py                    - Multi-platform StreamBoost")
    print("  python3 streamboost_channel_watch.py      - Basic YouTube watcher")
    print("  python3 streamboost_channel_watch_enhanced.py - Enhanced YouTube watcher")
    print("\nFor single-click deployment, use:")
    print("  ./deploy_master.sh")

if __name__ == "__main__":
    main()