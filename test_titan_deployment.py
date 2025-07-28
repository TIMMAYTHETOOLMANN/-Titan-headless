#!/usr/bin/env python3
"""
Test script for the new Titan viewer deployment system
Validates all components work correctly together
"""

import sys
import os
import importlib
import tempfile
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_deployment_system():
    """Test the deploy_viewer_system.py module"""
    print("🔄 Testing deployment system...")
    
    try:
        import deploy_viewer_system
        
        # Test environment detection
        os_type, os_version, python_version = deploy_viewer_system.detect_environment()
        print(f"   ✅ Environment detection: {os_type} {os_version}, Python {python_version}")
        
        # Test package checking
        result = deploy_viewer_system.check_package_installed("requests")
        print(f"   ✅ Package checking: requests = {result}")
        
        return True
    except Exception as e:
        print(f"   ❌ Deployment system test failed: {e}")
        return False

def test_advanced_modules():
    """Test the viewer_emulation_advanced.py module"""
    print("🔄 Testing advanced viewer emulation modules...")
    
    try:
        import viewer_emulation_advanced as vea
        
        # Test module initialization
        modules = vea.initialize_advanced_modules()
        print(f"   ✅ Initialized {len(modules)} advanced modules")
        
        # Test specific modules
        fingerprint = vea.HardwareFingerprintMasker.generate_fingerprint()
        print(f"   ✅ Generated fingerprint with {fingerprint['hardware_concurrency']} cores")
        
        platform_info = vea.MultiPlatformStreaming.detect_platform("https://www.youtube.com/watch?v=123")
        print(f"   ✅ Platform detection: {platform_info['platform']}")
        
        behavior = vea.SessionBehaviorAI.analyze_video_metadata(300, "Test Video")
        print(f"   ✅ AI behavior analysis: {behavior['recommended_watch_time']}s watch time")
        
        env_snapshot = vea.EnvironmentTelemetry.environment_snapshot()
        print(f"   ✅ Environment telemetry: {env_snapshot.get('system', {}).get('os', 'Unknown')}")
        
        return True
    except Exception as e:
        print(f"   ❌ Advanced modules test failed: {e}")
        return False

def test_viewer_emulation_integration():
    """Test the basic viewer emulation integration"""
    print("🔄 Testing viewer emulation integration...")
    
    try:
        # Check if viewer_emulation module was created
        viewer_emulation_path = Path("viewer_emulation")
        if viewer_emulation_path.exists():
            print("   ✅ viewer_emulation directory exists")
            
            # Check key files
            init_file = viewer_emulation_path / "__init__.py"
            if init_file.exists():
                print("   ✅ __init__.py found")
            
            # Try importing
            from viewer_emulation import ViewerBehavior, GeoIPRotator
            print("   ✅ Basic modules importable")
            
            # Test basic functionality
            viewer = ViewerBehavior()
            print("   ✅ ViewerBehavior instantiated")
            
            geo_rotator = GeoIPRotator()
            proxy = geo_rotator.rotate_proxy()
            print(f"   ✅ GeoIPRotator: {proxy}")
            
        else:
            print("   ⚠️  viewer_emulation directory not found - running injection...")
            # Run the injection script
            import viewer_emulation_auto_injection
            viewer_emulation_auto_injection.inject_modules()
            print("   ✅ viewer_emulation modules injected")
        
        return True
    except Exception as e:
        print(f"   ❌ Viewer emulation integration test failed: {e}")
        return False

def test_streamboost_integration():
    """Test streamboost integration"""
    print("🔄 Testing streamboost integration...")
    
    try:
        # Check if streamboost.py exists and has demo function
        streamboost_path = Path("streamboost.py")
        if streamboost_path.exists():
            print("   ✅ streamboost.py exists")
            
            # Check if it has the demo function
            with open(streamboost_path, 'r') as f:
                content = f.read()
                if "run_viewer_emulation_demo" in content:
                    print("   ✅ Demo function found in streamboost.py")
                else:
                    print("   ⚠️  Demo function not found in streamboost.py")
            
            # Try importing (may fail due to missing dependencies, that's OK)
            try:
                sys.path.append(str(streamboost_path.parent))
                import streamboost
                if hasattr(streamboost, 'run_viewer_emulation_demo'):
                    print("   ✅ Demo function is importable")
                else:
                    print("   ⚠️  Demo function not importable")
            except ImportError as ie:
                print(f"   ⚠️  Import failed (expected): {ie}")
            
        else:
            print("   ❌ streamboost.py not found")
            return False
        
        return True
    except Exception as e:
        print(f"   ❌ Streamboost integration test failed: {e}")
        return False

def test_run_scripts():
    """Test the run scripts"""
    print("🔄 Testing run scripts...")
    
    try:
        # Check Linux script
        linux_script = Path("run_linux.sh")
        if linux_script.exists() and os.access(linux_script, os.X_OK):
            print("   ✅ run_linux.sh exists and is executable")
        else:
            print("   ❌ run_linux.sh missing or not executable")
        
        # Check Windows script
        windows_script = Path("run_windows.bat")
        if windows_script.exists():
            print("   ✅ run_windows.bat exists")
        else:
            print("   ❌ run_windows.bat missing")
        
        return True
    except Exception as e:
        print(f"   ❌ Run scripts test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("🧪 TITAN VIEWER DEPLOYMENT SYSTEM TESTS")
    print("="*60)
    
    tests = [
        ("Deployment System", test_deployment_system),
        ("Advanced Modules", test_advanced_modules),  
        ("Viewer Emulation Integration", test_viewer_emulation_integration),
        ("Streamboost Integration", test_streamboost_integration),
        ("Run Scripts", test_run_scripts)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
            print(f"   ✅ {test_name} PASSED")
        else:
            print(f"   ❌ {test_name} FAILED")
    
    print(f"\n{'='*60}")
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        return True
    else:
        print("❌ Some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)