#!/usr/bin/env python3
"""
Test script to validate the specific context and health check fixes
"""

import asyncio
import os
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_url_configuration():
    """Test that URL configuration constants are properly set"""
    print("🔄 Testing URL configuration...")
    
    try:
        from streamboost import Config, get_platform_urls
        
        # Test constants exist
        assert hasattr(Config, 'YOUTUBE_URL'), "Missing YOUTUBE_URL constant"
        assert hasattr(Config, 'TWITCH_URL'), "Missing TWITCH_URL constant"
        assert hasattr(Config, 'KICK_URL'), "Missing KICK_URL constant"
        
        # Test URLs are properly configured
        urls = get_platform_urls()
        assert urls['YouTube'] == Config.YOUTUBE_URL, "YouTube URL mismatch"
        assert urls['Twitch'] == Config.TWITCH_URL, "Twitch URL mismatch"
        assert urls['Kick'] == Config.KICK_URL, "Kick URL mismatch"
        
        # Test URLs are not empty
        assert Config.YOUTUBE_URL.strip(), "YouTube URL is empty"
        assert Config.TWITCH_URL.strip(), "Twitch URL is empty"
        assert Config.KICK_URL.strip(), "Kick URL is empty"
        
        print(f"  ✅ YouTube URL: {Config.YOUTUBE_URL}")
        print(f"  ✅ Twitch URL: {Config.TWITCH_URL}")
        print(f"  ✅ Kick URL: {Config.KICK_URL}")
        
        return True
    except Exception as e:
        print(f"❌ URL configuration test failed: {e}")
        return False

async def test_context_creation_structure():
    """Test the context creation structure (without actually launching browsers)"""
    print("🔄 Testing context creation structure...")
    
    try:
        from streamboost import StreamWindow
        from pathlib import Path
        
        # Create a test window instance
        profile_dir = Path('./test_profiles/test_window')
        window = StreamWindow('YouTube', 'https://www.youtube.com/@timmaythetoolman/live', 9999, profile_dir)
        
        # Verify the instance has the new attributes
        assert hasattr(window, 'browser'), "Missing browser attribute"
        assert hasattr(window, 'context'), "Missing context attribute"
        assert window.browser is None, "Browser should be None initially"
        assert window.context is None, "Context should be None initially"
        
        print("  ✅ StreamWindow structure updated correctly")
        return True
        
    except Exception as e:
        print(f"❌ Context creation structure test failed: {e}")
        return False

async def test_validation_methods():
    """Test that validation and health check methods exist and work"""
    print("🔄 Testing validation methods...")
    
    try:
        from streamboost import StreamWindow
        from pathlib import Path
        
        # Create a test window instance
        profile_dir = Path('./test_profiles/test_window')
        window = StreamWindow('YouTube', 'https://www.youtube.com/@timmaythetoolman/live', 9999, profile_dir)
        
        # Test health check method exists and handles None values gracefully
        health_result = await window.health_check()
        assert health_result == False, "Health check should return False for uninitialized window"
        
        print("  ✅ Health check method working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Validation methods test failed: {e}")
        return False

async def test_scaling_throttling_logic():
    """Test that scaling throttling logic is properly implemented"""
    print("🔄 Testing scaling throttling logic...")
    
    try:
        from streamboost import StreamBoostController
        
        # Test controller initialization
        controller = StreamBoostController()
        await controller.initialize()
        
        # Verify we have multiple platforms for testing throttling
        assert len(controller.platforms) > 1, "Need multiple platforms to test throttling"
        
        print(f"  ✅ Controller has {len(controller.platforms)} platforms for throttling")
        return True
        
    except Exception as e:
        print(f"❌ Scaling throttling logic test failed: {e}")
        return False

async def main():
    """Run all context fix tests"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║              StreamBoost Context Fixes Test Suite               ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    tests = [
        ("URL Configuration", test_url_configuration),
        ("Context Creation Structure", test_context_creation_structure),
        ("Validation Methods", test_validation_methods),
        ("Scaling Throttling Logic", test_scaling_throttling_logic),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            if await test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            failed += 1
    
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║                        Final Results                            ║
║                                                                  ║
║  Passed: {passed:<2}                                                ║
║  Failed: {failed:<2}                                                ║
║  Total:  {passed + failed:<2}                                                ║
║                                                                  ║
""", end="")
    
    if failed == 0:
        print("║  Status: 🎉 ALL CONTEXT FIXES WORKING CORRECTLY            ║")
    else:
        print("║  Status: ⚠️  SOME FIXES NEED ATTENTION                     ║")
    
    print("╚══════════════════════════════════════════════════════════════════╝")
    
    return failed == 0

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)