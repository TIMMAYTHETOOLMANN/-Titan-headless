#!/usr/bin/env python3

"""
Simplified test script for Titan Headless implementation
Tests basic configuration loading and core functionality without requiring all dependencies
"""

import sys
import os
import yaml
import json
from pathlib import Path

def test_config_loading():
    """Test that configuration loads correctly"""
    print("[TEST] Testing configuration loading...")
    try:
        config_path = "enhanced_nexus_config.yaml"
        assert os.path.exists(config_path), f"Config file {config_path} not found"
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Test required sections
        assert 'streaming' in config, "Missing 'streaming' section in config"
        platforms = config['streaming']
        
        expected_platforms = ['youtube', 'twitch', 'kick']
        for platform in expected_platforms:
            assert platform in platforms, f"Platform {platform} not in config"
            assert 'enabled' in platforms[platform], f"Platform {platform} missing 'enabled' key"
            assert 'url' in platforms[platform], f"Platform {platform} missing 'url' key"
            assert 'count' in platforms[platform], f"Platform {platform} missing 'count' key"
        
        print("✓ Configuration loaded successfully")
        print(f"✓ Found platforms: {list(platforms.keys())}")
        
        # Test proxy configuration
        proxy_config = config.get('proxy', {})
        proxy_file = proxy_config.get('file', 'proxies.txt')
        print(f"✓ Proxy file configured: {proxy_file}")
        
        # Test AI chat configuration
        ai_config = config.get('advanced', {}).get('ai_chat', {})
        ai_enabled = ai_config.get('enabled', False)
        print(f"✓ AI Chat configured - Enabled: {ai_enabled}")
        
        return True
    except Exception as e:
        print(f"✗ Config loading test failed: {e}")
        return False

def test_proxy_file():
    """Test proxy file existence and format"""
    print("[TEST] Testing proxy file...")
    try:
        # Load config to get proxy file path
        with open("enhanced_nexus_config.yaml", 'r') as f:
            config = yaml.safe_load(f)
        
        proxy_file = config.get('proxy', {}).get('file', 'proxies.txt')
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
        
        # Test that port is numeric
        try:
            port = int(parts[1])
            assert 1 <= port <= 65535, f"Invalid port number: {port}"
        except ValueError:
            raise AssertionError(f"Non-numeric port in proxy: {sample_proxy}")
        
        print(f"✓ Proxy format validation passed (sample: {sample_proxy})")
        
        return True
    except Exception as e:
        print(f"✗ Proxy file test failed: {e}")
        return False

def test_titan_headless_script():
    """Test that the titan_headless.py script is valid Python"""
    print("[TEST] Testing titan_headless.py script...")
    try:
        script_path = "titan_headless.py"
        assert os.path.exists(script_path), f"Script {script_path} not found"
        print(f"✓ Script {script_path} exists")
        
        # Test that the script can be compiled (basic syntax check)
        with open(script_path, 'r') as f:
            script_content = f.read()
        
        compile(script_content, script_path, 'exec')
        print("✓ Script syntax is valid")
        
        # Test that required functions/variables are present
        required_elements = [
            'load_proxies',
            'random_username', 
            'get_or_create_identity',
            'save_identity',
            'generate_chat_response',
            'twitch_viewer',
            'youtube_viewer', 
            'kick_viewer',
            'run',
            'CONFIG',
            'PLATFORMS'
        ]
        
        for element in required_elements:
            assert element in script_content, f"Required element '{element}' not found in script"
        
        print("✓ All required functions/variables present")
        
        return True
    except Exception as e:
        print(f"✗ Script test failed: {e}")
        return False

def test_identity_system():
    """Test identity persistence system setup"""
    print("[TEST] Testing identity system...")
    try:
        identity_dir = Path("viewer_identities")
        
        # Test directory creation
        identity_dir.mkdir(exist_ok=True)
        assert identity_dir.exists(), f"Identity directory {identity_dir} not created"
        print(f"✓ Identity directory {identity_dir} exists")
        
        # Test identity structure
        test_identity = {
            "username": "testuser123",
            "cookies": {},
            "localStorage": {}
        }
        
        # Test identity file creation
        test_identity_file = identity_dir / "test_0.json"
        with open(test_identity_file, "w") as f:
            json.dump(test_identity, f)
        
        assert test_identity_file.exists(), "Identity file not created"
        
        # Test identity file reading
        with open(test_identity_file) as f:
            loaded_identity = json.load(f)
        
        assert loaded_identity == test_identity, "Identity data mismatch"
        print("✓ Identity persistence works")
        
        # Clean up test identity
        test_identity_file.unlink()
        
        return True
    except Exception as e:
        print(f"✗ Identity system test failed: {e}")
        return False

def test_platform_configuration():
    """Test platform-specific configuration"""
    print("[TEST] Testing platform configuration...")
    try:
        with open("enhanced_nexus_config.yaml", 'r') as f:
            config = yaml.safe_load(f)
        
        platforms = config['streaming']
        
        # Test each platform configuration
        for platform_name, platform_config in platforms.items():
            print(f"  Testing {platform_name}...")
            
            # Check required fields
            assert 'url' in platform_config, f"{platform_name} missing URL"
            assert 'enabled' in platform_config, f"{platform_name} missing enabled flag"
            assert 'count' in platform_config, f"{platform_name} missing count"
            
            # Validate URL format
            url = platform_config['url']
            assert url.startswith('http'), f"{platform_name} URL should start with http"
            
            # Validate expected domain
            if platform_name == 'twitch':
                assert 'twitch.tv' in url, f"Twitch URL should contain twitch.tv: {url}"
            elif platform_name == 'youtube':
                assert 'youtube.com' in url, f"YouTube URL should contain youtube.com: {url}"
            elif platform_name == 'kick':
                assert 'kick.com' in url, f"Kick URL should contain kick.com: {url}"
            
            # Validate count
            count = platform_config['count']
            assert isinstance(count, int) and count > 0, f"{platform_name} count should be positive integer"
            
            print(f"  ✓ {platform_name} configuration valid")
        
        print("✓ All platform configurations valid")
        return True
    except Exception as e:
        print(f"✗ Platform configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=== Titan Headless Basic Validation Suite ===\n")
    
    tests = [
        ("Configuration Loading", test_config_loading),
        ("Proxy File", test_proxy_file),
        ("Titan Headless Script", test_titan_headless_script),
        ("Identity System", test_identity_system),
        ("Platform Configuration", test_platform_configuration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
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
        print("🎉 All basic tests passed! Titan Headless core is ready.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Install playwright browsers: playwright install chromium")
        print("3. Run: python3 titan_headless.py")
        return True
    else:
        print(f"❌ {total - passed} tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)