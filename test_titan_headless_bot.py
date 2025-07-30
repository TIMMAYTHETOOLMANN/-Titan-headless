#!/usr/bin/env python3

"""
Test script for Titan Headless Bot CLI interface
Validates CLI functionality, configuration management, and integration
"""

import asyncio
import sys
import os
import tempfile
import shutil
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that titan_headless_bot imports correctly"""
    print("[TEST] Testing titan_headless_bot imports...")
    try:
        import titan_headless_bot
        print("✓ titan_headless_bot imported successfully")
        
        # Test class instantiation
        bot = titan_headless_bot.TitanHeadlessBot()
        assert hasattr(bot, 'config_path'), "TitanHeadlessBot missing config_path"
        assert hasattr(bot, 'load_config'), "TitanHeadlessBot missing load_config method"
        assert hasattr(bot, 'save_config'), "TitanHeadlessBot missing save_config method"
        print("✓ TitanHeadlessBot class instantiated successfully")
        
        return True
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False

def test_config_operations():
    """Test configuration loading and saving"""
    print("[TEST] Testing configuration operations...")
    try:
        import titan_headless_bot
        
        # Create a temporary config file for testing
        test_config = {
            'streaming': {
                'youtube': {'enabled': True, 'count': 10, 'url': 'test_url'},
                'twitch': {'enabled': False, 'count': 0, 'url': 'test_url'},
                'kick': {'enabled': True, 'count': 5, 'url': 'test_url'}
            },
            'proxy': {'file': 'proxies.txt'}
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(test_config, f)
            temp_config_path = f.name
        
        try:
            # Test with temporary config
            bot = titan_headless_bot.TitanHeadlessBot()
            bot.config_path = temp_config_path
            
            # Test loading
            loaded_config = bot.load_config()
            assert loaded_config['streaming']['youtube']['count'] == 10, "Config loading failed"
            print("✓ Configuration loading works")
            
            # Test configuration updates
            updated_config = bot.configure_platforms(youtube_count=20, twitch_count=15)
            assert updated_config['streaming']['youtube']['count'] == 20, "YouTube count update failed"
            assert updated_config['streaming']['twitch']['count'] == 15, "Twitch count update failed"
            assert updated_config['streaming']['youtube']['enabled'] == True, "YouTube should be enabled"
            assert updated_config['streaming']['twitch']['enabled'] == True, "Twitch should be enabled"
            print("✓ Platform configuration updates work")
            
            # Test backup/restore
            bot.create_backup()
            assert bot.backup_config is not None, "Config backup failed"
            print("✓ Configuration backup works")
            
        finally:
            # Clean up temporary file
            os.unlink(temp_config_path)
        
        return True
    except Exception as e:
        print(f"✗ Config operations test failed: {e}")
        return False

def test_cli_parser():
    """Test command-line argument parser"""
    print("[TEST] Testing CLI argument parser...")
    try:
        import titan_headless_bot
        
        parser = titan_headless_bot.create_parser()
        
        # Test basic arguments
        args = parser.parse_args(['--status'])
        assert args.status == True, "Status argument parsing failed"
        
        args = parser.parse_args(['--youtube', '10', '--twitch', '5'])
        assert args.youtube == 10, "YouTube count parsing failed"
        assert args.twitch == 5, "Twitch count parsing failed"
        
        args = parser.parse_args(['--run', '--duration', '3600'])
        assert args.run == True, "Run argument parsing failed"
        assert args.duration == 3600, "Duration parsing failed"
        
        # Test URL arguments
        args = parser.parse_args(['--youtube-url', 'https://example.com'])
        assert args.youtube_url == 'https://example.com', "YouTube URL parsing failed"
        
        print("✓ CLI argument parser works correctly")
        return True
    except Exception as e:
        print(f"✗ CLI parser test failed: {e}")
        return False

def test_validation():
    """Test bot validation functionality"""
    print("[TEST] Testing bot validation...")
    try:
        import titan_headless_bot
        
        # Create temporary files for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create mock files
            titan_file = os.path.join(temp_dir, 'titan_headless.py')
            config_file = os.path.join(temp_dir, 'enhanced_nexus_config.yaml')
            proxy_file = os.path.join(temp_dir, 'proxies.txt')
            
            # Create mock titan_headless.py
            with open(titan_file, 'w') as f:
                f.write("# Mock titan_headless.py")
            
            # Create mock config
            test_config = {
                'streaming': {
                    'youtube': {'enabled': True, 'count': 10, 'url': 'test'},
                    'twitch': {'enabled': False, 'count': 0, 'url': 'test'},
                    'kick': {'enabled': False, 'count': 0, 'url': 'test'}
                },
                'proxy': {'file': 'proxies.txt'}
            }
            with open(config_file, 'w') as f:
                yaml.dump(test_config, f)
            
            # Create mock proxy file
            with open(proxy_file, 'w') as f:
                f.write("127.0.0.1:8080\n192.168.1.1:3128\n")
            
            # Change to temp directory for testing
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                bot = titan_headless_bot.TitanHeadlessBot()
                bot.config_path = config_file
                
                # This should pass validation
                result = bot.validate_setup()
                assert result == True, "Validation should pass with proper setup"
                print("✓ Validation passes with correct setup")
                
                # Test with missing proxy file
                os.unlink(proxy_file)
                result = bot.validate_setup()
                assert result == False, "Validation should fail with missing proxy file"
                print("✓ Validation correctly fails with missing proxy file")
                
            finally:
                os.chdir(original_cwd)
        
        return True
    except Exception as e:
        print(f"✗ Validation test failed: {e}")
        return False

def test_status_display():
    """Test status display functionality"""
    print("[TEST] Testing status display...")
    try:
        import titan_headless_bot
        
        # Create temporary config for testing
        test_config = {
            'streaming': {
                'youtube': {'enabled': True, 'count': 25, 'url': 'https://youtube.com/test'},
                'twitch': {'enabled': False, 'count': 0, 'url': 'https://twitch.tv/test'},
                'kick': {'enabled': True, 'count': 15, 'url': 'https://kick.com/test'}
            },
            'proxy': {'file': 'proxies.txt'},
            'advanced': {'ai_chat': {'enabled': False}}
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(test_config, f)
            temp_config_path = f.name
        
        try:
            bot = titan_headless_bot.TitanHeadlessBot()
            bot.config_path = temp_config_path
            
            # Capture output (this will print to console, but won't fail)
            bot.show_status()
            print("✓ Status display completed without errors")
            
        finally:
            os.unlink(temp_config_path)
        
        return True
    except Exception as e:
        print(f"✗ Status display test failed: {e}")
        return False

async def test_integration():
    """Test integration with main titan_headless module"""
    print("[TEST] Testing integration with titan_headless...")
    try:
        import titan_headless_bot
        import titan_headless
        
        # Test that we can create bot instance and access titan_headless functions
        bot = titan_headless_bot.TitanHeadlessBot()
        
        # Test that titan_headless module has required components
        assert hasattr(titan_headless, 'CONFIG'), "titan_headless missing CONFIG"
        assert hasattr(titan_headless, 'run'), "titan_headless missing run function"
        assert hasattr(titan_headless, 'load_proxies'), "titan_headless missing load_proxies function"
        
        print("✓ Integration with titan_headless module works")
        return True
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("=== Titan Headless Bot Test Suite ===\n")
    
    tests = [
        ("Import and Instantiation", test_imports),
        ("Configuration Operations", test_config_operations),
        ("CLI Parser", test_cli_parser),
        ("Bot Validation", test_validation),
        ("Status Display", test_status_display),
        ("Integration", test_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            if result:
                passed += 1
                print(f"✓ {test_name} PASSED\n")
            else:
                print(f"✗ {test_name} FAILED\n")
        except Exception as e:
            print(f"✗ {test_name} FAILED with exception: {e}\n")
    
    print("=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Titan Headless Bot CLI is ready to use.")
        print("\nUsage examples:")
        print("  python titan_headless_bot.py --status")
        print("  python titan_headless_bot.py --youtube 10 --twitch 5")
        print("  python titan_headless_bot.py --run --duration 3600")
        return True
    else:
        print(f"❌ {total - passed} tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)