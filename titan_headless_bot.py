#!/usr/bin/env python3

"""
Titan Headless Bot: Command-Line Interface
A user-friendly CLI wrapper for the Titan Headless multi-platform viewer bot.

Features:
* Easy command-line configuration
* Quick platform targeting
* Real-time status monitoring
* Integration with existing titan_headless.py core
"""

import argparse
import asyncio
import sys
import os
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional
import time

# Import core functionality
try:
    import titan_headless
except ImportError:
    print("Error: titan_headless.py not found. Please ensure it's in the same directory.")
    sys.exit(1)

class TitanHeadlessBot:
    """CLI Bot Interface for Titan Headless"""
    
    def __init__(self):
        self.config_path = "enhanced_nexus_config.yaml"
        self.original_config = None
        self.backup_config = None
        
    def load_config(self) -> Dict:
        """Load the current configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file {self.config_path} not found.")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"Error parsing configuration file: {e}")
            sys.exit(1)
    
    def save_config(self, config: Dict) -> None:
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        except Exception as e:
            print(f"Error saving configuration: {e}")
            sys.exit(1)
    
    def create_backup(self) -> None:
        """Create a backup of the current configuration"""
        self.original_config = self.load_config()
        self.backup_config = self.original_config.copy()
    
    def restore_config(self) -> None:
        """Restore the original configuration"""
        if self.backup_config:
            self.save_config(self.backup_config)
            print("Configuration restored to original state.")
    
    def configure_platforms(self, youtube_count: Optional[int] = None, 
                          twitch_count: Optional[int] = None, 
                          kick_count: Optional[int] = None,
                          youtube_url: Optional[str] = None,
                          twitch_url: Optional[str] = None,
                          kick_url: Optional[str] = None) -> Dict:
        """Configure platform settings"""
        config = self.load_config()
        
        if youtube_count is not None:
            config['streaming']['youtube']['count'] = youtube_count
            config['streaming']['youtube']['enabled'] = youtube_count > 0
        
        if twitch_count is not None:
            config['streaming']['twitch']['count'] = twitch_count
            config['streaming']['twitch']['enabled'] = twitch_count > 0
            
        if kick_count is not None:
            config['streaming']['kick']['count'] = kick_count
            config['streaming']['kick']['enabled'] = kick_count > 0
        
        # Update URLs if provided
        if youtube_url:
            config['streaming']['youtube']['url'] = youtube_url
        if twitch_url:
            config['streaming']['twitch']['url'] = twitch_url
        if kick_url:
            config['streaming']['kick']['url'] = kick_url
            
        return config
    
    def show_status(self) -> None:
        """Display current bot configuration and status"""
        config = self.load_config()
        
        print("\n🤖 Titan Headless Bot Status")
        print("=" * 50)
        
        for platform, conf in config['streaming'].items():
            status = "🟢 ENABLED" if conf.get('enabled', False) else "🔴 DISABLED"
            count = conf.get('count', 0)
            url = conf.get('url', 'Not set')
            print(f"{platform.upper():8} | {status} | Viewers: {count:3d} | {url}")
        
        print("=" * 50)
        
        # Show proxy info
        proxy_file = config.get('proxy', {}).get('file', 'proxies.txt')
        if os.path.exists(proxy_file):
            with open(proxy_file) as f:
                proxy_count = len([p for p in f if p.strip()])
            print(f"Proxies loaded: {proxy_count}")
        else:
            print("⚠️  Proxy file not found!")
        
        # Show AI chat status
        ai_enabled = config.get('advanced', {}).get('ai_chat', {}).get('enabled', False)
        ai_status = "🟢 ENABLED" if ai_enabled else "🔴 DISABLED"
        print(f"AI Chat: {ai_status}")
        
        print()
    
    def validate_setup(self) -> bool:
        """Validate that the bot setup is correct"""
        print("🔍 Validating bot setup...")
        
        # Check core files
        if not os.path.exists('titan_headless.py'):
            print("❌ titan_headless.py not found")
            return False
        
        if not os.path.exists(self.config_path):
            print(f"❌ {self.config_path} not found")
            return False
        
        # Check proxy file
        config = self.load_config()
        proxy_file = config.get('proxy', {}).get('file', 'proxies.txt')
        if not os.path.exists(proxy_file):
            print(f"❌ Proxy file {proxy_file} not found")
            return False
        
        # Check if at least one platform is enabled
        platforms_enabled = any(
            conf.get('enabled', False) and conf.get('count', 0) > 0
            for conf in config['streaming'].values()
        )
        
        if not platforms_enabled:
            print("❌ No platforms enabled with viewer count > 0")
            return False
        
        print("✅ Bot setup validation passed!")
        return True
    
    async def run_bot(self, duration: Optional[int] = None) -> None:
        """Run the bot with optional duration limit"""
        if not self.validate_setup():
            print("Setup validation failed. Please fix the issues above.")
            return
        
        print("\n🚀 Starting Titan Headless Bot...")
        print("Press Ctrl+C to stop\n")
        
        try:
            if duration:
                print(f"Bot will run for {duration} seconds")
                # Run with timeout
                await asyncio.wait_for(titan_headless.run(), timeout=duration)
            else:
                # Run indefinitely
                await titan_headless.run()
        except asyncio.TimeoutError:
            print(f"\n⏰ Bot stopped after {duration} seconds")
        except KeyboardInterrupt:
            print("\n🛑 Bot stopped by user")
        except Exception as e:
            print(f"\n❌ Bot error: {e}")
        finally:
            if self.backup_config:
                self.restore_config()

def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser"""
    parser = argparse.ArgumentParser(
        description="Titan Headless Bot - Multi-platform Viewer Bot CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python titan_headless_bot.py --status
  python titan_headless_bot.py --youtube 10 --twitch 5
  python titan_headless_bot.py --run --duration 3600
  python titan_headless_bot.py --youtube 20 --run
        """
    )
    
    # Action commands
    parser.add_argument('--status', action='store_true',
                       help='Show current bot status and configuration')
    parser.add_argument('--run', action='store_true',
                       help='Start the bot')
    parser.add_argument('--validate', action='store_true',
                       help='Validate bot setup without running')
    
    # Platform configuration
    parser.add_argument('--youtube', type=int, metavar='COUNT',
                       help='Set YouTube viewer count')
    parser.add_argument('--twitch', type=int, metavar='COUNT',
                       help='Set Twitch viewer count')
    parser.add_argument('--kick', type=int, metavar='COUNT',
                       help='Set Kick viewer count')
    
    # URL configuration
    parser.add_argument('--youtube-url', metavar='URL',
                       help='Set YouTube stream URL')
    parser.add_argument('--twitch-url', metavar='URL',
                       help='Set Twitch stream URL')
    parser.add_argument('--kick-url', metavar='URL',
                       help='Set Kick stream URL')
    
    # Runtime options
    parser.add_argument('--duration', type=int, metavar='SECONDS',
                       help='Run bot for specified duration in seconds')
    
    return parser

async def main():
    """Main function"""
    parser = create_parser()
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    bot = TitanHeadlessBot()
    
    # Handle configuration changes
    if any([args.youtube, args.twitch, args.kick, 
            args.youtube_url, args.twitch_url, args.kick_url]):
        print("📝 Updating configuration...")
        bot.create_backup()
        
        config = bot.configure_platforms(
            youtube_count=args.youtube,
            twitch_count=args.twitch, 
            kick_count=args.kick,
            youtube_url=args.youtube_url,
            twitch_url=args.twitch_url,
            kick_url=args.kick_url
        )
        
        bot.save_config(config)
        print("✅ Configuration updated!")
    
    # Handle action commands
    if args.status:
        bot.show_status()
    
    if args.validate:
        bot.validate_setup()
    
    if args.run:
        await bot.run_bot(duration=args.duration)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)