#!/bin/bash
set -e

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║    NEXUS MAXIMUS - TITAN HEADLESS ENHANCEMENT SYSTEM v2.0       ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

export DEBIAN_FRONTEND=noninteractive

# 1. System dependencies
echo "[+] Installing core system libraries and browsers..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update -qq
    # Install packages with Ubuntu 24.04+ compatibility, skip browsers for now
    sudo apt-get install -y python3 python3-pip python3-venv wget curl \
        xvfb unzip libnss3 libdbus-1-3 libxkbcommon0 \
        libxcomposite1 libxrandr2 libgbm1 libpangocairo-1.0-0 \
        libxshmfence1 fonts-liberation --no-install-recommends || true
    
    # Install newer package variants if available
    sudo apt-get install -y libatk1.0-0t64 || sudo apt-get install -y libatk1.0-0 || true
    sudo apt-get install -y libatk-bridge2.0-0t64 || sudo apt-get install -y libatk-bridge2.0-0 || true
    sudo apt-get install -y libcups2t64 || sudo apt-get install -y libcups2 || true
    sudo apt-get install -y libasound2t64 || sudo apt-get install -y libasound2 || true
    sudo apt-get install -y libgtk-3-0t64 || sudo apt-get install -y libgtk-3-0 || true
    
    # Try to install browsers (may fail in some environments, that's OK)
    echo "  → Attempting browser installation..."
    sudo apt-get install -y chromium-browser || echo "  ⚠️  Chromium not available via apt"
    sudo apt-get install -y firefox || echo "  ⚠️  Firefox not available via apt"
elif command -v yum &> /dev/null; then
    sudo yum install -y python3 python3-pip python3-venv wget curl \
        chromium firefox xorg-x11-server-Xvfb unzip
elif command -v brew &> /dev/null; then
    brew install python3 wget curl
fi

# 2. Python virtual environment
echo "[+] Creating enhanced Python virtual environment..."
if [ -d ".nexusvenv" ]; then
    echo "  ⚠️  Existing virtual environment found, backing up..."
    mv .nexusvenv .nexusvenv_backup_$(date +%s)
fi

python3 -m venv .nexusvenv
source .nexusvenv/bin/activate

# 3. Install enhanced Python dependencies
echo "[+] Installing enhanced Python dependencies..."
pip install --upgrade pip setuptools wheel

# Core dependencies
pip install playwright selenium fake_useragent requests pyyaml cloudscraper
pip install psutil py-cpuinfo beautifulsoup4 aiofiles dataclasses-json

# Optional advanced dependencies (install if available)
echo "[+] Installing optional advanced features..."
pip install undetected-chromedriver || echo "  ⚠️  undetected-chromedriver not available"
pip install anticaptchaofficial || echo "  ⚠️  anticaptcha not available"
pip install openai || echo "  ⚠️  OpenAI not available"

echo "[+] Installing Flite shared libraries and comprehensive browser dependencies..."
if [ -f "./install_flite_browsers.sh" ]; then
    echo "  → Running comprehensive Flite and browser dependency installer..."
    bash ./install_flite_browsers.sh --skip-playwright || echo "  ⚠️  Flite installer had issues but continuing..."
else
    echo "  ⚠️  Flite installer script not found, using fallback method..."
    # Install libflite1 as fallback
    sudo apt-get install -y libflite1 || echo "  ⚠️  libflite1 not available"
fi

echo "[+] Installing Playwright browsers..."
python3 -m playwright install chromium firefox webkit

# 4. Enhanced proxy management
echo "[+] Setting up enhanced proxy management..."
mkdir -p proxy_sources

# Download from multiple reliable sources
echo "  → Fetching proxy lists from multiple sources..."
curl -s --connect-timeout 10 'https://www.proxy-list.download/api/v1/get?type=https' > proxy_sources/source1.txt 2>/dev/null || touch proxy_sources/source1.txt
curl -s --connect-timeout 10 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=https&timeout=5000&country=all&ssl=all&anonymity=all' > proxy_sources/source2.txt 2>/dev/null || touch proxy_sources/source2.txt
curl -s --connect-timeout 10 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt' > proxy_sources/source3.txt 2>/dev/null || touch proxy_sources/source3.txt

# Combine and deduplicate
cat proxy_sources/*.txt | grep -E '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+:[0-9]+$' | sort -u > proxies.txt
echo "  ✅ Collected $(wc -l < proxies.txt) unique proxies"

# 5. Enhanced configuration
echo "[+] Creating enhanced configuration..."
cat << 'EOF' > nexus_config.yaml
# Nexus Maximus Configuration v2.0
streaming:
  youtube:
    url: "https://www.youtube.com/@timmaythetoolman/live"
    count: 15
    enabled: true
  twitch:
    url: "https://www.twitch.tv/timmaythetoolman"
    count: 15
    enabled: true
  kick:
    url: "https://kick.com/timmaythetoolman"
    count: 15
    enabled: true

proxy:
  file: "proxies.txt"
  enabled: true
  rotation_interval: 300
  geo_filtering:
    enabled: false
    countries: ["US", "CA", "GB", "DE", "FR", "AU", "SG"]

automation:
  headless: true
  dwell_time:
    min: 180
    max: 1200
  browsers: ["chromium", "firefox"]
  
behavior:
  human_simulation: true
  mouse_movements: true
  scroll_simulation: true
  click_simulation: true
  heartbeat:
    enabled: true
    interval_min: 30
    interval_max: 120

advanced:
  ai_chat:
    enabled: false
    provider: "none"  # "openai" or "none"
    api_key: ""
  captcha:
    enabled: false
    provider: "none"  # "anticaptcha" or "none"
    api_key: ""
  stealth:
    user_agent_rotation: true
    fingerprint_randomization: true
    
system:
  resource_monitoring: true
  cpu_threshold: 85
  memory_threshold: 85
  max_concurrent_windows: 50
EOF

# 6. Enhanced main application
echo "[+] Creating enhanced Nexus Maximus application..."
cat << 'PYTHONEOF' > nexus_maximus.py
#!/usr/bin/env python3
"""
Nexus Maximus v2.0 - Enhanced Titan Headless Streaming System
Advanced multi-platform streaming automation with stealth and AI features
"""

import os
import sys
import yaml
import random
import time
import threading
import requests
import json
import logging
import asyncio
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from fake_useragent import UserAgent
from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext
import psutil

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class NexusConfig:
    """Enhanced configuration management"""
    
    def __init__(self, config_path="nexus_config.yaml"):
        self.config_path = config_path
        self.config = self.load_config()
        
    def load_config(self) -> dict:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file {self.config_path} not found")
            sys.exit(1)
        except yaml.YAMLError as e:
            logger.error(f"Error parsing configuration: {e}")
            sys.exit(1)
    
    def get(self, key_path: str, default=None):
        """Get nested configuration value using dot notation"""
        keys = key_path.split('.')
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

class ProxyManager:
    """Enhanced proxy management with geo-filtering"""
    
    def __init__(self, config: NexusConfig):
        self.config = config
        self.proxies = self.load_proxies()
        self.current_index = 0
        
    def load_proxies(self) -> List[str]:
        """Load and filter proxies"""
        proxy_file = self.config.get('proxy.file', 'proxies.txt')
        if not os.path.exists(proxy_file):
            logger.warning(f"Proxy file {proxy_file} not found")
            return []
            
        with open(proxy_file, 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
            
        if self.config.get('proxy.geo_filtering.enabled', False):
            proxies = self.filter_proxies_by_geo(proxies)
            
        logger.info(f"Loaded {len(proxies)} proxies")
        return proxies
    
    def filter_proxies_by_geo(self, proxies: List[str]) -> List[str]:
        """Filter proxies by geographical location"""
        countries = self.config.get('proxy.geo_filtering.countries', [])
        if not countries:
            return proxies
            
        filtered = []
        for proxy in proxies[:50]:  # Limit to first 50 for geo check
            try:
                ip = proxy.split(':')[0]
                response = requests.get(f"https://ipinfo.io/{ip}/country", timeout=3)
                if response.ok and response.text.strip() in countries:
                    filtered.append(proxy)
            except Exception:
                continue
                
        return filtered if filtered else proxies
    
    def get_proxy(self) -> Optional[str]:
        """Get next proxy from rotation"""
        if not self.proxies:
            return None
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy

class BehaviorSimulator:
    """Advanced human behavior simulation"""
    
    def __init__(self, config: NexusConfig):
        self.config = config
        self.user_agent = UserAgent()
        
    def simulate_human_activity(self, page: Page):
        """Simulate realistic human activity"""
        if not self.config.get('behavior.human_simulation', True):
            return
            
        try:
            # Mouse movements
            if self.config.get('behavior.mouse_movements', True):
                self.simulate_mouse_movements(page)
                
            # Scrolling
            if self.config.get('behavior.scroll_simulation', True):
                self.simulate_scrolling(page)
                
            # Random clicks
            if self.config.get('behavior.click_simulation', True):
                self.simulate_clicks(page)
                
        except Exception as e:
            logger.warning(f"Behavior simulation error: {e}")
    
    def simulate_mouse_movements(self, page: Page):
        """Simulate natural mouse movements"""
        for _ in range(random.randint(3, 8)):
            x = random.randint(100, 1200)
            y = random.randint(100, 800)
            page.mouse.move(x, y)
            time.sleep(random.uniform(0.1, 0.5))
    
    def simulate_scrolling(self, page: Page):
        """Simulate natural scrolling behavior"""
        for _ in range(random.randint(2, 5)):
            delta_y = random.randint(-300, 300)
            page.mouse.wheel(0, delta_y)
            time.sleep(random.uniform(0.5, 2.0))
    
    def simulate_clicks(self, page: Page):
        """Simulate occasional clicks on safe elements"""
        try:
            # Click on video player area (safe zone)
            video_area = page.query_selector('video, .video-player, .player')
            if video_area and random.random() < 0.3:
                video_area.click()
                time.sleep(random.uniform(1, 3))
        except Exception:
            pass

class StreamWindow:
    """Enhanced streaming window management"""
    
    def __init__(self, platform: str, url: str, config: NexusConfig, proxy_manager: ProxyManager):
        self.platform = platform
        self.url = url
        self.config = config
        self.proxy_manager = proxy_manager
        self.behavior = BehaviorSimulator(config)
        self.browser = None
        self.context = None
        self.page = None
        
    def setup_browser_args(self, proxy: Optional[str] = None) -> List[str]:
        """Setup browser launch arguments"""
        args = [
            '--no-sandbox',
            '--disable-blink-features=AutomationControlled',
            '--disable-extensions',
            '--disable-plugins',
            '--disable-images',
            '--disable-javascript',
            '--disable-default-apps',
            '--disable-sync',
            '--disable-background-timer-throttling',
            '--disable-renderer-backgrounding',
            '--disable-backgrounding-occluded-windows',
            '--disable-features=TranslateUI,BlinkGenPropertyTrees'
        ]
        
        if proxy:
            args.append(f'--proxy-server={proxy}')
            
        return args
    
    def launch(self) -> bool:
        """Launch browser window"""
        try:
            proxy = self.proxy_manager.get_proxy() if self.config.get('proxy.enabled', False) else None
            
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=self.config.get('automation.headless', True),
                    args=self.setup_browser_args(proxy)
                )
                
                context = browser.new_context(
                    viewport={'width': 1280, 'height': 800},
                    user_agent=self.behavior.user_agent.random if self.config.get('advanced.stealth.user_agent_rotation', True) else None
                )
                
                page = context.new_page()
                
                # Navigate to stream
                logger.info(f"Opening {self.platform} stream: {self.url}")
                page.goto(self.url, timeout=60000)
                
                # Wait for page load
                time.sleep(random.uniform(3, 8))
                
                # Simulate human behavior
                dwell_time = random.randint(
                    self.config.get('automation.dwell_time.min', 180),
                    self.config.get('automation.dwell_time.max', 1200)
                )
                
                start_time = time.time()
                while time.time() - start_time < dwell_time:
                    self.behavior.simulate_human_activity(page)
                    
                    # Heartbeat
                    if self.config.get('behavior.heartbeat.enabled', True):
                        time.sleep(random.randint(
                            self.config.get('behavior.heartbeat.interval_min', 30),
                            self.config.get('behavior.heartbeat.interval_max', 120)
                        ))
                    else:
                        time.sleep(10)
                
                context.close()
                browser.close()
                return True
                
        except Exception as e:
            logger.error(f"Error in {self.platform} window: {e}")
            return False

class ResourceMonitor:
    """System resource monitoring"""
    
    def __init__(self, config: NexusConfig):
        self.config = config
        
    def check_resources(self) -> bool:
        """Check if system resources are within limits"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        
        cpu_threshold = self.config.get('system.cpu_threshold', 85)
        memory_threshold = self.config.get('system.memory_threshold', 85)
        
        if cpu_percent > cpu_threshold:
            logger.warning(f"High CPU usage: {cpu_percent}%")
            return False
            
        if memory_percent > memory_threshold:
            logger.warning(f"High memory usage: {memory_percent}%")
            return False
            
        return True

class NexusMaximus:
    """Main Nexus Maximus controller"""
    
    def __init__(self, config_path="nexus_config.yaml"):
        self.config = NexusConfig(config_path)
        self.proxy_manager = ProxyManager(self.config)
        self.resource_monitor = ResourceMonitor(self.config)
        
    def get_enabled_platforms(self) -> List[Tuple[str, str, int]]:
        """Get list of enabled streaming platforms"""
        platforms = []
        
        for platform in ['youtube', 'twitch', 'kick']:
            if self.config.get(f'streaming.{platform}.enabled', False):
                url = self.config.get(f'streaming.{platform}.url')
                count = self.config.get(f'streaming.{platform}.count', 0)
                if url and count > 0:
                    platforms.append((platform.capitalize(), url, count))
                    
        return platforms
    
    def launch_platform_windows(self, platform: str, url: str, count: int):
        """Launch multiple windows for a platform"""
        threads = []
        max_concurrent = self.config.get('system.max_concurrent_windows', 50)
        
        for i in range(min(count, max_concurrent)):
            if not self.resource_monitor.check_resources():
                logger.warning("Resource limits reached, stopping window creation")
                break
                
            window = StreamWindow(platform, url, self.config, self.proxy_manager)
            thread = threading.Thread(target=window.launch, daemon=True)
            thread.start()
            threads.append(thread)
            
            # Stagger window launches
            time.sleep(random.uniform(1, 5))
            
        # Wait for all threads
        for thread in threads:
            thread.join()
    
    def run(self):
        """Main execution loop"""
        logger.info("Starting Nexus Maximus Enhanced System")
        
        platforms = self.get_enabled_platforms()
        if not platforms:
            logger.error("No platforms enabled in configuration")
            return
            
        logger.info(f"Enabled platforms: {[p[0] for p in platforms]}")
        
        for platform, url, count in platforms:
            logger.info(f"Launching {count} windows for {platform}")
            self.launch_platform_windows(platform, url, count)
            
        logger.info("All platform windows launched")

def main():
    """Main entry point"""
    try:
        nexus = NexusMaximus()
        nexus.run()
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
PYTHONEOF

# 7. Create launch script
echo "[+] Creating enhanced launch script..."
cat << 'BASHEOF' > run_nexus.sh
#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║               Launching Nexus Maximus v2.0                      ║"
echo "╚══════════════════════════════════════════════════════════════════╝"

# Activate virtual environment
if [ -f ".nexusvenv/bin/activate" ]; then
    source .nexusvenv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found. Run enhance.sh first."
    exit 1
fi

# Check configuration
if [ ! -f "nexus_config.yaml" ]; then
    echo "❌ Configuration file not found. Run enhance.sh first."
    exit 1
fi

# Setup virtual display for headless operation
if [ -z "$DISPLAY" ] && command -v Xvfb &> /dev/null; then
    echo "🖥️  Setting up virtual display..."
    export DISPLAY=:99
    Xvfb :99 -screen 0 1920x1080x24 &
    XVFB_PID=$!
    sleep 2
    echo "✅ Virtual display ready"
fi

# Launch Nexus Maximus
echo "🚀 Starting Nexus Maximus..."
python3 nexus_maximus.py

# Cleanup
if [ ! -z "$XVFB_PID" ]; then
    kill $XVFB_PID 2>/dev/null
    echo "✅ Virtual display cleaned up"
fi

echo "✅ Nexus Maximus session completed"
BASHEOF

chmod +x run_nexus.sh

# 8. Update .gitignore for new files
echo "[+] Updating .gitignore..."
cat << 'GITEOF' >> .gitignore

# Nexus Maximus specific
.nexusvenv/
nexus_profiles/
proxy_sources/
*.log
nexus_config_local.yaml
GITEOF

# 9. Create validation script
echo "[+] Creating validation script..."
cat << 'VALIDEOF' > validate_nexus.py
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
VALIDEOF

chmod +x validate_nexus.py

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                NEXUS MAXIMUS v2.0 SETUP COMPLETE                ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "🎯 Next steps:"
echo "   1. Validate setup: python3 validate_nexus.py"
echo "   2. Edit configuration: nano nexus_config.yaml"
echo "   3. Launch system: ./run_nexus.sh"
echo ""
echo "📁 Key files created:"
echo "   • nexus_maximus.py    - Enhanced main application"
echo "   • nexus_config.yaml   - Configuration file"
echo "   • run_nexus.sh        - Launch script"
echo "   • validate_nexus.py   - Validation script"
echo "   • proxies.txt         - Proxy list"
echo ""
echo "✨ Enhanced features:"
echo "   • Multi-platform streaming support"
echo "   • Advanced proxy management"
echo "   • Human behavior simulation"
echo "   • Resource monitoring"
echo "   • Headless operation"
echo "   • Configurable parameters"
echo ""