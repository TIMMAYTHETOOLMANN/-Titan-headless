#!/usr/bin/env python3
"""
Nexus Maximus validation and testing script
"""

import os
import sys
import subprocess
import importlib.util

def check_file(filepath, description):
    """Check if file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description}")
        return False

def check_module(module_name):
    """Check if Python module is available"""
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is not None:
            print(f"✅ {module_name} module available")
            return True
    except ImportError:
        pass
    print(f"❌ {module_name} module not available")
    return False

def check_command(command):
    """Check if command is available"""
    try:
        result = subprocess.run(['which', command], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {command} command available")
            return True
    except:
        pass
    print(f"❌ {command} command not available")
    return False

def main():
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║                 Nexus Maximus Validation                        ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()
    
    checks_passed = 0
    total_checks = 0
    
    # File checks
    file_checks = [
        ('nexus_maximus.py', 'Main application file'),
        ('nexus_config.yaml', 'Configuration file'),
        ('run_nexus.sh', 'Launch script'),
        ('proxies.txt', 'Proxy list'),
        ('.nexusvenv/bin/activate', 'Virtual environment')
    ]
    
    for filepath, description in file_checks:
        if check_file(filepath, description):
            checks_passed += 1
        total_checks += 1
    
    print()
    
    # Module checks
    module_checks = [
        'yaml', 'requests', 'playwright', 'psutil', 'fake_useragent'
    ]
    
    for module in module_checks:
        if check_module(module):
            checks_passed += 1
        total_checks += 1
    
    print()
    
    # Command checks
    command_checks = [
        'python3', 'chromium-browser', 'firefox'
    ]
    
    for command in command_checks:
        if check_command(command):
            checks_passed += 1
        total_checks += 1
    
    print()
    print(f"Validation Results: {checks_passed}/{total_checks} checks passed")
    
    if checks_passed == total_checks:
        print("🎉 All validations passed! Nexus Maximus is ready to run.")
        return 0
    else:
        print("⚠️  Some validations failed. Run enhance.sh to fix issues.")
        return 1

if __name__ == "__main__":
    sys.exit(main())