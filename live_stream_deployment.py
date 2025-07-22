#!/usr/bin/env python3
"""
Titan Headless - Live Stream Deployment Module
Specialized deployment system for live streaming across multiple platforms
"""

import asyncio
import logging
import random
import time
import psutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from playwright.async_api import async_playwright, Browser, Page, BrowserContext
from playwright_stealth import Stealth

from deployment_core import (
    DeploymentConfig, ConfigManager, DeploymentValidator, 
    DeploymentMode, PlatformConfig
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('live_stream_deployment.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# User agents for rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0'
]

class LiveStreamWindow:
    """Individual live stream window manager"""
    
    def __init__(self, platform: str, url: str, port: int, profile_dir: Path, config: DeploymentConfig):
        self.platform = platform
        self.url = url
        self.port = port
        self.profile_dir = profile_dir
        self.config = config
        self.user_agent = random.choice(USER_AGENTS)
        self.browser: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.is_running = False
        self.is_live = False
        self.last_live_check = 0
        
    async def launch(self, playwright) -> bool:
        """Launch browser instance for live stream watching"""
        try:
            # Ensure profile directory exists
            self.profile_dir.mkdir(parents=True, exist_ok=True)
            
            # Browser launch arguments
            args = [
                f'--remote-debugging-port={self.port}',
                '--disable-blink-features=AutomationControlled',
                '--disable-background-timer-throttling',
                '--disable-renderer-backgrounding',
                '--disable-backgrounding-occluded-windows',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-infobars',
                '--disable-extensions',
                '--no-first-run',
                '--no-default-browser-check',
                f'--window-size={self.config.shared.window_width},{self.config.shared.window_height}',
                '--disable-web-security'
            ]
            
            # Browser context configuration
            context_options = {
                'user_data_dir': str(self.profile_dir),
                'args': args,
                'headless': self.config.shared.headless,
                'viewport': {
                    'width': self.config.shared.window_width, 
                    'height': self.config.shared.window_height
                }
            }
            
            # Add proxy if available
            if self.config.shared.proxy_list:
                proxy = random.choice(self.config.shared.proxy_list)
                context_options['proxy'] = {'server': proxy}
            
            # Launch persistent context
            self.browser = await playwright.chromium.launch_persistent_context(**context_options)
            
            # Create new page and apply stealth
            self.page = await self.browser.new_page()
            stealth_instance = Stealth()
            await stealth_instance.apply_stealth_async(self.page)
            
            # Set user agent
            await self.page.set_extra_http_headers({
                'User-Agent': self.user_agent
            })
            
            # Navigate to platform URL
            await self.page.goto(self.url, wait_until='domcontentloaded', timeout=30000)
            await self.human_emulation()
            
            self.is_running = True
            logger.info(f"✓ {self.platform} live stream window launched - Port: {self.port}")
            
            return True
            
        except Exception as e:
            logger.error(f"✗ Failed to launch {self.platform} live stream window: {str(e)}")
            return False
    
    async def human_emulation(self):
        """Simulate human behavior on the page"""
        try:
            # Random mouse movements and scrolling
            await asyncio.sleep(random.uniform(2, 5))
            
            # Scroll to simulate user interaction
            for _ in range(random.randint(2, 4)):
                await self.page.mouse.wheel(0, random.randint(100, 300))
                await asyncio.sleep(random.uniform(1, 3))
            
            # Click on video player if present (platform-specific)
            if self.platform.lower() == 'youtube':
                try:
                    await self.page.click('video', timeout=5000)
                except:
                    pass
            elif self.platform.lower() == 'twitch':
                try:
                    await self.page.click('[data-a-target="player-overlay-click-handler"]', timeout=5000)
                except:
                    pass
            elif self.platform.lower() == 'kick':
                try:
                    await self.page.click('video', timeout=5000)
                except:
                    pass
                    
        except Exception as e:
            logger.debug(f"Human emulation error on {self.platform}: {str(e)}")
    
    async def check_if_live(self) -> bool:
        """Check if the stream is currently live"""
        try:
            current_time = time.time()
            if current_time - self.last_live_check < self.config.live_stream.check_interval:
                return self.is_live
            
            self.last_live_check = current_time
            
            # Platform-specific live detection
            if self.platform.lower() == 'youtube':
                # Check for live indicator
                live_indicators = [
                    '[class*="live"]',
                    '[aria-label*="live"]',
                    'text=LIVE',
                    '.ytp-live'
                ]
                for selector in live_indicators:
                    try:
                        element = await self.page.query_selector(selector)
                        if element:
                            self.is_live = True
                            return True
                    except:
                        continue
                        
            elif self.platform.lower() == 'twitch':
                # Check for live indicator
                try:
                    live_element = await self.page.query_selector('[data-a-target="animated-channel-viewers-count"]')
                    self.is_live = live_element is not None
                    return self.is_live
                except:
                    pass
                    
            elif self.platform.lower() == 'kick':
                # Check for live indicator
                try:
                    live_element = await self.page.query_selector('.text-danger')
                    if live_element:
                        text = await live_element.text_content()
                        self.is_live = 'live' in text.lower()
                        return self.is_live
                except:
                    pass
            
            self.is_live = False
            return False
            
        except Exception as e:
            logger.debug(f"Live check error on {self.platform}: {str(e)}")
            return False
    
    async def wait_for_live_stream(self) -> bool:
        """Wait for stream to go live or timeout"""
        start_time = time.time()
        max_wait = self.config.live_stream.max_wait_time
        
        logger.info(f"Waiting for {self.platform} stream to go live (max {max_wait}s)...")
        
        while time.time() - start_time < max_wait:
            if await self.check_if_live():
                logger.info(f"🔴 {self.platform} stream is now LIVE!")
                return True
            
            await asyncio.sleep(self.config.live_stream.check_interval)
        
        logger.warning(f"⏰ {self.platform} stream did not go live within {max_wait}s")
        return False
    
    async def monitor_live_status(self):
        """Continuously monitor live status and handle accordingly"""
        while self.is_running:
            try:
                is_currently_live = await self.check_if_live()
                
                if not is_currently_live and self.config.live_stream.fallback_to_videos:
                    # Fallback to regular videos if stream goes offline
                    await self.fallback_to_videos()
                
                await asyncio.sleep(self.config.live_stream.check_interval)
                
            except Exception as e:
                logger.error(f"Live monitoring error on {self.platform}: {str(e)}")
                await asyncio.sleep(self.config.live_stream.check_interval)
    
    async def fallback_to_videos(self):
        """Fallback to watching regular videos when stream is offline"""
        try:
            if self.platform.lower() == 'youtube':
                # Navigate to videos tab
                videos_url = self.url.replace('/live', '/videos')
                await self.page.goto(videos_url, wait_until='domcontentloaded')
                
                # Click on a random video
                await asyncio.sleep(3)
                videos = await self.page.query_selector_all('a[href*="/watch"]')
                if videos:
                    random_video = random.choice(videos)
                    await random_video.click()
                    logger.info(f"📺 {self.platform} fallback: watching regular video")
                    
        except Exception as e:
            logger.debug(f"Fallback error on {self.platform}: {str(e)}")
    
    async def close(self):
        """Close the browser window"""
        try:
            self.is_running = False
            if self.browser:
                await self.browser.close()
            logger.info(f"🔒 {self.platform} live stream window closed")
        except Exception as e:
            logger.error(f"Error closing {self.platform} window: {str(e)}")

class LiveStreamDeployment:
    """Main live stream deployment controller"""
    
    def __init__(self, config: DeploymentConfig):
        self.config = config
        self.windows: List[LiveStreamWindow] = []
        self.is_running = False
        
    async def deploy(self):
        """Deploy live stream windows for all enabled platforms"""
        if self.config.deployment_mode not in [DeploymentMode.LIVE_STREAM, DeploymentMode.BOTH]:
            logger.error("Live stream deployment not enabled in configuration")
            return
        
        logger.info("🚀 Starting live stream deployment...")
        
        async with async_playwright() as playwright:
            self.is_running = True
            
            # Launch windows for each enabled platform
            port_offset = 0
            
            for platform_name, platform_config in self.config.live_stream.platforms.items():
                if not platform_config.enabled:
                    continue
                
                await self._deploy_platform(playwright, platform_name, platform_config, port_offset)
                port_offset += platform_config.windows
            
            if not self.windows:
                logger.error("No platforms deployed successfully")
                return
            
            # Start monitoring tasks
            monitor_tasks = [window.monitor_live_status() for window in self.windows]
            
            logger.info(f"🎮 Live stream deployment active - {len(self.windows)} windows monitoring")
            
            try:
                await asyncio.gather(*monitor_tasks)
            except KeyboardInterrupt:
                logger.info("🛑 Shutdown signal received...")
                await self.shutdown()
    
    async def _deploy_platform(self, playwright, platform_name: str, platform_config: PlatformConfig, port_offset: int):
        """Deploy windows for a specific platform"""
        try:
            # Generate URL for the platform
            url = platform_config.url_template.format(account=self.config.live_stream.target_account)
            
            logger.info(f"Deploying {platform_config.windows} windows for {platform_name}")
            
            for i in range(platform_config.windows):
                # Check system resources before launching
                if not self._check_resources():
                    logger.warning("System resources at threshold, delaying launch...")
                    await asyncio.sleep(30)
                    continue
                
                # Create window
                port = self.config.shared.base_port + port_offset + i
                profile_dir = Path(self.config.shared.profile_base) / f"{platform_name}_{i}"
                
                window = LiveStreamWindow(platform_name, url, port, profile_dir, self.config)
                
                # Launch window
                if await window.launch(playwright):
                    self.windows.append(window)
                    
                    # Wait for live stream or timeout
                    if not await window.wait_for_live_stream():
                        logger.warning(f"{platform_name} stream not live, continuing with monitoring")
                
                # Delay between launches
                delay = random.uniform(2, 7)
                await asyncio.sleep(delay)
                
        except Exception as e:
            logger.error(f"Error deploying {platform_name}: {str(e)}")
    
    def _check_resources(self) -> bool:
        """Check if system resources are within thresholds"""
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            ram = psutil.virtual_memory().percent
            
            return (cpu < self.config.shared.cpu_threshold and 
                   ram < self.config.shared.ram_threshold)
        except:
            return True
    
    async def shutdown(self):
        """Gracefully shutdown all live stream windows"""
        self.is_running = False
        
        logger.info("Shutting down live stream deployment...")
        
        shutdown_tasks = [window.close() for window in self.windows]
        await asyncio.gather(*shutdown_tasks, return_exceptions=True)
        
        logger.info("✅ Live stream deployment shutdown complete")
    
    def status_report(self):
        """Generate status report for live stream deployment"""
        live_count = sum(1 for window in self.windows if window.is_live)
        
        print(f"\n{'='*60}")
        print(f"🔴 LIVE STREAM DEPLOYMENT STATUS")
        print(f"{'='*60}")
        print(f"Total Windows: {len(self.windows)}")
        print(f"Live Streams: {live_count}")
        print(f"Platforms: {len(set(w.platform for w in self.windows))}")
        print(f"Target Account: {self.config.live_stream.target_account}")
        
        # Platform breakdown
        for platform_name in self.config.live_stream.platforms:
            platform_windows = [w for w in self.windows if w.platform == platform_name]
            platform_live = sum(1 for w in platform_windows if w.is_live)
            print(f"  {platform_name}: {len(platform_windows)} windows, {platform_live} live")
        
        print(f"{'='*60}\n")

async def main():
    """Main entry point for live stream deployment"""
    try:
        # Load configuration
        config = ConfigManager.load_config()
        
        # Validate configuration
        issues = DeploymentValidator.validate_config(config)
        if issues:
            logger.error("Configuration validation failed:")
            for issue in issues:
                logger.error(f"  - {issue}")
            return
        
        # Create and start deployment
        deployment = LiveStreamDeployment(config)
        deployment.status_report()
        await deployment.deploy()
        
    except KeyboardInterrupt:
        logger.info("🛑 User interruption detected")
    except Exception as e:
        logger.error(f"💥 Critical error: {str(e)}")
        raise

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                Titan Headless Live Stream                   ║
    ║                  Deployment Module v1.0                     ║
    ║                                                              ║
    ║  Multi-platform live stream watching deployment             ║
    ║  Press Ctrl+C to stop all windows                          ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")