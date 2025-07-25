#!/usr/bin/env python3
"""
Comprehensive test for StreamBoost headless deployment simulation
Tests all components without actually launching browsers
"""

import asyncio
import os
import sys
import subprocess
import tempfile
from pathlib import Path

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_virtual_display_creation():
    """Test creating and using virtual display"""
    print("🔄 Testing virtual display creation...")
    
    try:
        # Clear any existing DISPLAY
        original_display = os.environ.get("DISPLAY")
        if "DISPLAY" in os.environ:
            del os.environ["DISPLAY"]
        
        # Start virtual display
        display_num = "99"
        xvfb_cmd = ["Xvfb", f":{display_num}", "-screen", "0", "1920x1080x24", "-ac"]
        xvfb_process = subprocess.Popen(xvfb_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Set DISPLAY environment
        os.environ["DISPLAY"] = f":{display_num}"
        
        print(f"  ✅ Virtual display started on :{display_num}")
        
        # Clean up
        xvfb_process.terminate()
        xvfb_process.wait()
        
        # Restore original DISPLAY
        if original_display:
            os.environ["DISPLAY"] = original_display
        elif "DISPLAY" in os.environ:
            del os.environ["DISPLAY"]
        
        return True
        
    except Exception as e:
        print(f"❌ Virtual display test failed: {e}")
        return False

async def test_streamboost_window_creation():
    """Test StreamWindow creation without browser launch"""
    print("🔄 Testing StreamWindow creation...")
    
    try:
        from streamboost import StreamWindow, Config
        
        # Create temporary profile directory
        with tempfile.TemporaryDirectory() as temp_dir:
            profile_dir = Path(temp_dir) / "test_profile"
            
            # Create StreamWindow instance
            window = StreamWindow(
                platform="YouTube",
                url="https://www.youtube.com/@timmaythetoolman/live",
                port=9223,
                profile_dir=profile_dir
            )
            
            print(f"  ✅ StreamWindow created: {window.platform} on port {window.port}")
            print(f"  ✅ Profile directory: {window.profile_dir}")
            print(f"  ✅ User agent configured: {window.user_agent[:50]}...")
            print(f"  ✅ Headless mode: {Config.HEADLESS}")
            
            return True
            
    except Exception as e:
        print(f"❌ StreamWindow creation test failed: {e}")
        return False

async def test_platform_manager():
    """Test PlatformManager functionality"""
    print("🔄 Testing PlatformManager...")
    
    try:
        from streamboost import PlatformManager
        
        # Create platform manager
        manager = PlatformManager(
            platform="YouTube",
            url="https://www.youtube.com/@timmaythetoolman/live",
            window_count=2,
            port_start=9223
        )
        
        print(f"  ✅ PlatformManager created for {manager.platform}")
        print(f"  ✅ Configuration: {manager.window_count} windows starting at port {manager.port_start}")
        
        return True
        
    except Exception as e:
        print(f"❌ PlatformManager test failed: {e}")
        return False

async def test_resource_monitoring():
    """Test resource monitoring functionality"""
    print("🔄 Testing resource monitoring...")
    
    try:
        from streamboost import resource_check
        
        is_ok, resources = resource_check()
        
        print(f"  ✅ Resource check completed")
        print(f"  ✅ CPU usage: {resources['cpu']:.1f}%")
        print(f"  ✅ RAM usage: {resources['ram']:.1f}%")
        print(f"  ✅ Disk usage: {resources['disk']:.1f}%")
        print(f"  ✅ System status: {'OK' if is_ok else 'High usage'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Resource monitoring test failed: {e}")
        return False

async def test_configuration_loading():
    """Test configuration and utilities"""
    print("🔄 Testing configuration loading...")
    
    try:
        from streamboost import Config, get_platform_urls, USER_AGENTS, LANGUAGES, TIMEZONES
        
        urls = get_platform_urls()
        
        print(f"  ✅ Target account: {Config.TARGET_ACCOUNT}")
        print(f"  ✅ Platform URLs configured: {len(urls)} platforms")
        print(f"  ✅ User agents pool: {len(USER_AGENTS)} agents")
        print(f"  ✅ Languages pool: {len(LANGUAGES)} languages")
        print(f"  ✅ Timezones pool: {len(TIMEZONES)} timezones")
        print(f"  ✅ Base port: {Config.BASE_PORT}")
        print(f"  ✅ Profile base: {Config.PROFILE_BASE}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

async def run_deployment_simulation():
    """Run complete deployment simulation"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║              StreamBoost Deployment Simulation                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    tests = [
        ("Virtual Display Creation", test_virtual_display_creation),
        ("StreamWindow Creation", test_streamboost_window_creation),
        ("PlatformManager Setup", test_platform_manager),
        ("Resource Monitoring", test_resource_monitoring),
        ("Configuration Loading", test_configuration_loading),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}...")
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
║                    Simulation Results                           ║
║                                                                  ║
║  Passed: {passed:<2}                                                ║
║  Failed: {failed:<2}                                                ║
║  Total:  {passed + failed:<2}                                                ║
║                                                                  ║
""", end="")
    
    if failed == 0:
        print("║  Status: 🎉 DEPLOYMENT SIMULATION SUCCESSFUL                ║")
        print("║          All components ready for headless operation        ║")
    else:
        print("║  Status: ⚠️  SOME COMPONENTS FAILED                         ║")
    
    print("╚══════════════════════════════════════════════════════════════════╝")
    
    if failed == 0:
        print("\n🚀 StreamBoost is ready for headless operation!")
        print("   To deploy: ./deploy_streamboost.sh")
        print("   To run: python3 streamboost.py")
    
    return failed == 0

if __name__ == "__main__":
    result = asyncio.run(run_deployment_simulation())
    sys.exit(0 if result else 1)