#!/usr/bin/env python3
"""
Setup script for Enhanced Channel Watch Monolith
Installs dependencies and sets up Playwright
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║           Enhanced Channel Watch Monolith Setup                 ║
║                      Installation Script                        ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version} detected")
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        sys.exit(1)
    
    # Install Playwright browsers
    if not run_command("playwright install chromium", "Installing Playwright Chromium browser"):
        print("⚠️  Browser installation failed, but may work if browser is already installed")
    
    # Create directories
    os.makedirs("./profiles", exist_ok=True)
    os.makedirs("./logs", exist_ok=True)
    
    print("✅ Directory structure created")
    
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                        Setup Complete!                          ║
║                                                                  ║
║  Available Scripts:                                              ║
║  • streamboost_channel_watch.py          - Basic version        ║
║  • streamboost_channel_watch_enhanced.py - Enhanced version     ║
║                                                                  ║
║  Configuration:                                                  ║
║  • Edit channel_watch_config.yaml for settings                  ║
║                                                                  ║
║  Usage:                                                          ║
║  python streamboost_channel_watch_enhanced.py                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)

if __name__ == "__main__":
    main()