#!/usr/bin/env python3
"""
Test script for Twitch persistent viewer functionality
"""

import sys
import os
import json
import tempfile
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, '/home/runner/work/-Titan-headless/-Titan-headless')

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        import twitch_persistent_viewers as tpv
        print("✓ twitch_persistent_viewers imported successfully")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_identity_management():
    """Test the identity creation and management functions"""
    print("\nTesting identity management...")
    try:
        import twitch_persistent_viewers as tpv
        
        # Create a temporary directory for testing
        original_identity_dir = tpv.IDENTITY_DIR
        tpv.IDENTITY_DIR = Path(tempfile.mkdtemp()) / "test_identities"
        tpv.IDENTITY_DIR.mkdir(exist_ok=True)
        
        # Test identity creation
        identity = tpv.get_or_create_identity(1)
        assert "username" in identity
        assert "cookies" in identity
        assert "localStorage" in identity
        print("✓ Identity creation works")
        
        # Test identity persistence
        identity["cookies"]["test"] = "value"
        tpv.save_identity(1, identity)
        
        loaded_identity = tpv.get_or_create_identity(1)
        assert loaded_identity["cookies"]["test"] == "value"
        print("✓ Identity persistence works")
        
        # Cleanup
        import shutil
        shutil.rmtree(tpv.IDENTITY_DIR.parent)
        tpv.IDENTITY_DIR = original_identity_dir
        
        return True
    except Exception as e:
        print(f"✗ Identity management test failed: {e}")
        return False

def test_proxy_file_handling():
    """Test proxy file loading functionality"""
    print("\nTesting proxy file handling...")
    try:
        import twitch_persistent_viewers as tpv
        
        # Check if proxy file exists
        if os.path.exists(tpv.PROXY_POOL):
            print("✓ Proxy file exists")
            
            # Count proxies
            with open(tpv.PROXY_POOL) as f:
                proxies = [p.strip() for p in f if p.strip()]
            print(f"✓ Found {len(proxies)} proxies in file")
            
            if len(proxies) > 0:
                print("✓ Proxy file has content")
                return True
            else:
                print("⚠ Proxy file is empty")
                return False
        else:
            print(f"⚠ Proxy file not found: {tpv.PROXY_POOL}")
            return False
    except Exception as e:
        print(f"✗ Proxy file test failed: {e}")
        return False

def test_username_generation():
    """Test username generation functionality"""
    print("\nTesting username generation...")
    try:
        import twitch_persistent_viewers as tpv
        
        username1 = tpv.random_username()
        username2 = tpv.random_username()
        
        assert len(username1) == 8
        assert len(username2) == 8
        assert username1 != username2  # Should be different
        assert username1.islower()
        assert username1.isalpha()
        
        print("✓ Username generation works correctly")
        return True
    except Exception as e:
        print(f"✗ Username generation test failed: {e}")
        return False

def test_configuration():
    """Test configuration constants"""
    print("\nTesting configuration...")
    try:
        import twitch_persistent_viewers as tpv
        
        assert tpv.TWITCH_HEARTBEAT == "https://gql.twitch.tv/gql"
        assert tpv.STREAM_URL == "https://www.twitch.tv/YOUR_CHANNEL"
        assert tpv.PROXY_POOL == "proxies.txt"
        assert len(tpv.CHAT_MESSAGES) > 0
        
        print("✓ Configuration constants are set correctly")
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and report results"""
    print("=" * 50)
    print("TWITCH PERSISTENT VIEWERS - TEST SUITE")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_configuration,
        test_username_generation,
        test_identity_management,
        test_proxy_file_handling,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! Script is ready for use.")
        return True
    else:
        print("⚠ Some tests failed. Check the issues above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)