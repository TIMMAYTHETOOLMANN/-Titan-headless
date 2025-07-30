#!/usr/bin/env python3

"""
Test script for Titan Headless implementation
Validates configuration loading, proxy loading, and basic functionality
"""

import asyncio
import sys
import os
from pathlib import Path

# Add current directory to path to allow importing titan_headless
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required imports work"""
    print("[TEST] Testing imports...")
    try:
        import titan_headless
        print("✓ titan_headless imported successfully")
        
        # Test config loading
        assert hasattr(titan_headless, 'CONFIG'), "CONFIG not found"
        assert hasattr(titan_headless, 'PLATFORMS'), "PLATFORMS not found"
        print("✓ Configuration loaded successfully")
        
        # Test platform configuration
        platforms = titan_headless.PLATFORMS
        expected_platforms = ['youtube', 'twitch', 'kick']
        for platform in expected_platforms:
            assert platform in platforms, f"Platform {platform} not in config"
            assert 'enabled' in platforms[platform], f"Platform {platform} missing 'enabled' key"
            assert 'url' in platforms[platform], f"Platform {platform} missing 'url' key"
            assert 'count' in platforms[platform], f"Platform {platform} missing 'count' key"
        print("✓ All platforms configured correctly")
        
        return True
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False

def test_proxy_file():
    """Test proxy file existence and format"""
    print("[TEST] Testing proxy file...")
    try:
        import titan_headless
        proxy_file = titan_headless.PROXY_FILE
        
        assert os.path.exists(proxy_file), f"Proxy file {proxy_file} not found"
        print(f"✓ Proxy file {proxy_file} exists")
        
        with open(proxy_file) as f:
            proxies = [p.strip() for p in f if p.strip()]
        
        assert len(proxies) > 0, "No proxies found in file"
        print(f"✓ Found {len(proxies)} proxies in file")
        
        # Test proxy format (basic validation)
        sample_proxy = proxies[0]
        assert ":" in sample_proxy, f"Invalid proxy format: {sample_proxy}"
        parts = sample_proxy.split(":")
        assert len(parts) == 2, f"Invalid proxy format: {sample_proxy}"
        print(f"✓ Proxy format validation passed (sample: {sample_proxy})")
        
        return True
    except Exception as e:
        print(f"✗ Proxy file test failed: {e}")
        return False

def test_identity_system():
    """Test identity persistence system"""
    print("[TEST] Testing identity system...")
    try:
        import titan_headless
        
        # Test identity directory creation
        identity_dir = titan_headless.IDENTITY_DIR
        assert identity_dir.exists(), f"Identity directory {identity_dir} not created"
        print(f"✓ Identity directory {identity_dir} exists")
        
        # Test identity creation
        identity = titan_headless.get_or_create_identity("test", 0)
        assert "username" in identity, "Identity missing username"
        assert "cookies" in identity, "Identity missing cookies"
        assert "localStorage" in identity, "Identity missing localStorage"
        print("✓ Identity creation works")
        
        # Test identity persistence
        identity_file = identity_dir / "test_0.json"
        assert identity_file.exists(), "Identity file not created"
        print("✓ Identity persistence works")
        
        # Clean up test identity
        identity_file.unlink()
        
        return True
    except Exception as e:
        print(f"✗ Identity system test failed: {e}")
        return False

async def test_proxy_validation():
    """Test proxy validation function"""
    print("[TEST] Testing proxy validation...")
    try:
        import titan_headless
        
        # Test with a small subset of proxies for speed
        with open(titan_headless.PROXY_FILE) as f:
            all_proxies = [p.strip() for p in f if p.strip()]
        
        # Take only first 5 proxies for testing
        test_proxies = all_proxies[:5]
        
        # Temporarily create a test proxy file
        test_proxy_file = "test_proxies.txt"
        with open(test_proxy_file, 'w') as f:
            f.write('\n'.join(test_proxies))
        
        # Backup original proxy file setting
        original_proxy_file = titan_headless.PROXY_FILE
        titan_headless.PROXY_FILE = test_proxy_file
        
        try:
            # This will validate the test proxies
            valid_proxies = await titan_headless.load_proxies()
            print(f"✓ Proxy validation completed: {len(valid_proxies)} valid out of {len(test_proxies)}")
        finally:
            # Restore original setting and clean up
            titan_headless.PROXY_FILE = original_proxy_file
            os.unlink(test_proxy_file)
        
        return True
    except Exception as e:
        print(f"✗ Proxy validation test failed: {e}")
        return False

async def test_ai_chat_config():
    """Test AI chat configuration"""
    print("[TEST] Testing AI chat configuration...")
    try:
        import titan_headless
        
        # Test AI chat config loading
        ai_enabled = titan_headless.AI_CHAT_ENABLED
        ai_key = titan_headless.AI_CHAT_API_KEY
        ai_provider = titan_headless.AI_CHAT_PROVIDER
        
        print(f"✓ AI Chat - Enabled: {ai_enabled}, Provider: {ai_provider}, Key: {'Set' if ai_key else 'Not set'}")
        
        # Test AI chat function with disabled state
        history = [{"user": "test", "text": "hello"}]
        response = await titan_headless.generate_chat_response(history)
        
        if not ai_enabled or not ai_key:
            assert response is None, "AI chat should return None when disabled"
            print("✓ AI chat correctly disabled")
        else:
            print("✓ AI chat configuration loaded (testing with real API requires key)")
        
        return True
    except Exception as e:
        print(f"✗ AI chat config test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("=== Titan Headless Test Suite ===\n")
    
    tests = [
        ("Import and Config", test_imports),
        ("Proxy File", test_proxy_file),
        ("Identity System", test_identity_system),
        ("Proxy Validation", test_proxy_validation),
        ("AI Chat Config", test_ai_chat_config)
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
        print("🎉 All tests passed! Titan Headless is ready to use.")
        return True
    else:
        print(f"❌ {total - passed} tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)