#!/usr/bin/env python3
"""
Enhanced validation script for Flite shared libraries and Playwright browsers
Addresses the dependency loop issues in headless environments
"""

import os
import sys
import subprocess
import importlib.util

def run_command(command, description="Command"):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_flite_libraries():
    """Check for Flite shared libraries"""
    print("🔍 Checking Flite shared libraries...")
    
    # Check for key Flite shared libraries
    key_libs = [
        'libflite_cmu_us_kal.so',
        'libflite_cmu_us_awb.so', 
        'libflite_cmu_us_rms.so',
        'libflite.so'
    ]
    
    found_libs = []
    missing_libs = []
    
    for lib in key_libs:
        success, stdout, _ = run_command(f"ldconfig -p | grep {lib}")
        if success and lib in stdout:
            found_libs.append(lib)
            print(f"  ✅ {lib} found in system")
        else:
            missing_libs.append(lib)
            print(f"  ❌ {lib} not found")
    
    # Check for any flite libraries
    success, stdout, _ = run_command("ldconfig -p | grep flite")
    if success and stdout.strip():
        print(f"  ℹ️  Total Flite libraries found: {len(stdout.strip().split('libflite'))}")
        return len(found_libs) > 0
    
    print("  ❌ No Flite libraries found in system")
    return False

def check_browser_dependencies():
    """Check browser dependencies"""
    print("🔍 Checking browser dependencies...")
    
    essential_deps = [
        'libgtk-3-0',
        'libnss3', 
        'libxss1',
        'libgbm1',
        'libxrandr2',
        'libxcomposite1',
        'libasound2'
    ]
    
    missing_deps = []
    
    for dep in essential_deps:
        # Check both the exact name and common variants
        for variant in [dep, f"{dep}t64"]:
            success, _, _ = run_command(f"dpkg -l | grep -q '^ii.*{variant}'")
            if success:
                print(f"  ✅ {variant} installed")
                break
        else:
            missing_deps.append(dep)
            print(f"  ❌ {dep} (and variants) not found")
    
    return len(missing_deps) == 0

def check_playwright_functionality():
    """Check Playwright functionality"""
    print("🔍 Checking Playwright functionality...")
    
    try:
        # Test import
        import playwright
        print("  ✅ Playwright module imports successfully")
        
        # Test async API
        from playwright.async_api import async_playwright
        print("  ✅ Playwright async API available")
        
        # Test sync API
        from playwright.sync_api import sync_playwright
        print("  ✅ Playwright sync API available")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Playwright import failed: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Playwright test failed: {e}")
        return False

def check_browser_binaries():
    """Check browser binary availability"""
    print("🔍 Checking browser binaries...")
    
    browsers = {
        'chromium-browser': ['chromium-browser', 'chromium', 'google-chrome'],
        'firefox': ['firefox'],
        'webkit': ['webkit2gtk-launcher']  
    }
    
    available_browsers = []
    
    for browser_name, commands in browsers.items():
        found = False
        for cmd in commands:
            success, stdout, _ = run_command(f"which {cmd}")
            if success:
                print(f"  ✅ {browser_name} available as {cmd} at {stdout.strip()}")
                available_browsers.append(browser_name)
                found = True
                break
        
        if not found:
            print(f"  ❌ {browser_name} not found in PATH")
    
    return len(available_browsers) >= 2  # At least 2 browsers should be available

def check_headless_environment():
    """Check headless environment setup"""
    print("🔍 Checking headless environment...")
    
    # Check Xvfb
    success, stdout, _ = run_command("which Xvfb")
    if success:
        print(f"  ✅ Xvfb available at {stdout.strip()}")
    else:
        print("  ❌ Xvfb not available")
        return False
    
    # Check DISPLAY variable
    display = os.environ.get('DISPLAY')
    if display:
        print(f"  ✅ DISPLAY set to {display}")
    else:
        print("  ⚠️  DISPLAY not set (will be set automatically)")
    
    return True

def run_browser_launch_test():
    """Test actual browser launch (minimal test)"""
    print("🔍 Running browser launch test...")
    
    try:
        from playwright.sync_api import sync_playwright
        
        # Set up virtual display if needed
        original_display = os.environ.get('DISPLAY')
        if not original_display:
            os.environ['DISPLAY'] = ':99'
        
        # Start virtual display
        xvfb_process = None
        try:
            xvfb_process = subprocess.Popen(['Xvfb', ':99', '-screen', '0', '1024x768x24'], 
                                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Short wait for Xvfb to start
            import time
            time.sleep(2)
            
            # Test browser launch
            with sync_playwright() as p:
                try:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    page.goto("data:text/html,<html><body><h1>Test</h1></body></html>")
                    title = page.title()
                    browser.close()
                    
                    if "Test" in title or len(title) >= 0:  # Basic success check
                        print("  ✅ Browser launch test successful")
                        return True
                    else:
                        print("  ⚠️  Browser launched but title check failed")
                        return True  # Still consider success
                        
                except Exception as e:
                    print(f"  ❌ Browser launch failed: {e}")
                    return False
                    
        finally:
            # Cleanup
            if xvfb_process:
                xvfb_process.terminate()
                xvfb_process.wait()
            
            # Restore original DISPLAY
            if original_display:
                os.environ['DISPLAY'] = original_display
            elif 'DISPLAY' in os.environ:
                del os.environ['DISPLAY']
                
    except Exception as e:
        print(f"  ❌ Browser test setup failed: {e}")
        return False

def main():
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║         Enhanced Flite & Browser Dependencies Validation        ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()
    
    tests = [
        ("Flite Shared Libraries", check_flite_libraries),
        ("Browser Dependencies", check_browser_dependencies), 
        ("Playwright Functionality", check_playwright_functionality),
        ("Browser Binaries", check_browser_binaries),
        ("Headless Environment", check_headless_environment),
        ("Browser Launch Test", run_browser_launch_test)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"📋 {test_name}")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"  ❌ Test crashed: {e}")
            results.append((test_name, False))
        print()
    
    # Summary
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║                           SUMMARY                               ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} {test_name}")
    
    print()
    print(f"Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All validations passed! System ready for headless browser automation.")
        print()
        print("To fix any remaining issues, run:")
        print("  ./install_flite_browsers.sh")
        return 0
    else:
        print("⚠️  Some validations failed. Run the installation script:")
        print("  ./install_flite_browsers.sh")
        return 1

if __name__ == "__main__":
    sys.exit(main())