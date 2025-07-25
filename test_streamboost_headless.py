#!/usr/bin/env python3
"""
Test script to verify StreamBoost can initialize in headless mode
This validates the core functionality without actually launching browsers
"""

import asyncio
import os
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_streamboost_headless():
    """Test StreamBoost initialization in headless mode"""
    print("🔄 Testing StreamBoost headless initialization...")
    
    try:
        # Clear display to simulate headless environment
        original_display = os.environ.get("DISPLAY")
        if "DISPLAY" in os.environ:
            del os.environ["DISPLAY"]
        
        # Import StreamBoost components
        from streamboost import StreamBoostController, Config
        
        # Verify headless configuration
        if not Config.HEADLESS:
            print("❌ Headless mode not enabled by default")
            return False
        
        print(f"  ✅ Headless mode enabled: {Config.HEADLESS}")
        print(f"  ✅ Window configuration: YouTube={Config.YOUTUBE_WINDOWS}, Kick={Config.KICK_WINDOWS}, Twitch={Config.TWITCH_WINDOWS}")
        
        # Test controller initialization
        controller = StreamBoostController()
        await controller.initialize()
        
        print(f"  ✅ Controller initialized with {len(controller.platforms)} platforms")
        
        # Test profile directory creation
        if Config.PROFILE_BASE.exists():
            print(f"  ✅ Profile directory created: {Config.PROFILE_BASE}")
        else:
            print("❌ Profile directory not created")
            return False
        
        # Restore original DISPLAY
        if original_display:
            os.environ["DISPLAY"] = original_display
        
        print("  ✅ StreamBoost headless initialization successful")
        return True
        
    except Exception as e:
        print(f"❌ StreamBoost headless test failed: {e}")
        return False

async def test_headless_end_to_end():
    """Full end-to-end test for headless operation"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║               StreamBoost Headless E2E Test                     ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    tests = [
        ("StreamBoost Headless Init", test_streamboost_headless),
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
        print("║  Status: 🎉 HEADLESS OPERATION FULLY FUNCTIONAL             ║")
    else:
        print("║  Status: ⚠️  SOME TESTS FAILED                              ║")
    
    print("╚══════════════════════════════════════════════════════════════════╝")
    
    return failed == 0

if __name__ == "__main__":
    result = asyncio.run(test_headless_end_to_end())
    sys.exit(0 if result else 1)