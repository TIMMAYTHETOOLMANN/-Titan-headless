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