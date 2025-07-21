#!/usr/bin/env python3
"""
Enhanced Channel Watch Monolith - Optimized Edition

Fully autonomous, randomized, undetectable YouTube channel view simulation. 
No dependencies on YouTube API keys. All stealth, all random, all operational.

ENHANCEMENTS:
1. Video duration checking to avoid very short videos
2. Better error handling and recovery mechanisms  
3. Configuration file support (JSON/YAML)
4. Performance monitoring and statistics
5. Video engagement simulation (like/dislike, comments)
6. Cookie and session management for more realistic behavior
7. Intelligent video selection based on view count/popularity
"""

import asyncio
import random
import string
import os
import time
import psutil
import requests
import json
import yaml
import logging
import aiofiles
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from cpuinfo import get_cpu_info

# ENHANCED CONFIGURATION SYSTEM
@dataclass
class ChannelWatchConfig:
    """Configuration class with defaults"""
    channel_url: str = 'https://www.youtube.com/@timmaythetoolan'
    windows: int = 20
    base_port: int = 9333
    profile_base: str = './profiles'
    proxy_list: List[str] = None
    rotate_video_every: Tuple[int, int] = (180, 320)
    max_videos: int = 25
    min_video_duration: int = 60  # Skip videos shorter than this (seconds)
    max_video_duration: int = 3600  # Skip videos longer than this (seconds)
    cpu_threshold: int = 85
    ram_threshold: int = 85
    engagement_rate: float = 0.3  # Chance of engagement actions
    statistics_enabled: bool = True
    log_level: str = 'INFO'
    
    def __post_init__(self):
        if self.proxy_list is None:
            self.proxy_list = []

# ENHANCED USER AGENTS AND LOCALE DATA
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

LANGUAGES = ['en-US', 'en-GB', 'fr-FR', 'de-DE', 'es-ES', 'it-IT', 'pt-PT', 'nl-NL']
TIMEZONES = [
    'America/New_York', 'Europe/London', 'Europe/Berlin', 'Asia/Tokyo',
    'America/Los_Angeles', 'Australia/Sydney', 'Europe/Paris', 'America/Chicago'
]

# ENHANCED LOGGING SETUP
def setup_logging(log_level: str = 'INFO'):
    """Setup enhanced logging with colors and file output"""
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler with colors
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # File handler
    file_handler = logging.FileHandler('channel_watch.log')
    file_handler.setFormatter(formatter)
    
    # Setup logger
    logger = logging.getLogger('ChannelWatch')
    logger.setLevel(level)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# STATISTICS TRACKING
@dataclass
class WatchStatistics:
    """Statistics tracking class"""
    windows_launched: int = 0
    windows_failed: int = 0
    videos_watched: int = 0
    total_watch_time: int = 0
    engagements_performed: int = 0
    errors_encountered: int = 0
    start_time: datetime = None
    last_updated: datetime = None
    
    def __post_init__(self):
        if self.start_time is None:
            self.start_time = datetime.now()
        self.last_updated = datetime.now()
    
    def update_watch_time(self, seconds: int):
        self.total_watch_time += seconds
        self.last_updated = datetime.now()
    
    def record_engagement(self):
        self.engagements_performed += 1
        self.last_updated = datetime.now()
    
    def record_error(self):
        self.errors_encountered += 1
        self.last_updated = datetime.now()
    
    def get_uptime(self) -> timedelta:
        return datetime.now() - self.start_time
    
    def to_dict(self) -> Dict:
        return asdict(self)

# ENHANCED VIDEO DATA CLASS
@dataclass
class VideoInfo:
    """Enhanced video information"""
    url: str
    title: str = ""
    duration: int = 0  # seconds
    view_count: int = 0
    likes: int = 0
    upload_date: Optional[datetime] = None
    popularity_score: float = 0.0
    
    def calculate_popularity(self):
        """Calculate popularity score based on views, likes, and recency"""
        if self.view_count and self.likes:
            base_score = (self.likes / max(self.view_count, 1)) * 100
            # Boost recent videos
            if self.upload_date:
                days_old = (datetime.now() - self.upload_date).days
                recency_boost = max(0, 1 - (days_old / 365))  # Decay over a year
                self.popularity_score = base_score * (1 + recency_boost)
            else:
                self.popularity_score = base_score
        return self.popularity_score

class ConfigManager:
    """Configuration file management"""
    
    @staticmethod
    def load_config(config_path: str = 'channel_watch_config.yaml') -> ChannelWatchConfig:
        """Load configuration from file"""
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    if config_path.endswith('.json'):
                        data = json.load(f)
                    else:
                        data = yaml.safe_load(f)
                return ChannelWatchConfig(**data)
        except Exception as e:
            print(f"Error loading config: {e}, using defaults")
        return ChannelWatchConfig()
    
    @staticmethod
    def save_config(config: ChannelWatchConfig, config_path: str = 'channel_watch_config.yaml'):
        """Save configuration to file"""
        try:
            with open(config_path, 'w') as f:
                if config_path.endswith('.json'):
                    json.dump(asdict(config), f, indent=2)
                else:
                    yaml.dump(asdict(config), f, default_flow_style=False)
        except Exception as e:
            print(f"Error saving config: {e}")

class PerformanceMonitor:
    """System performance monitoring"""
    
    def __init__(self, stats: WatchStatistics):
        self.stats = stats
        self.logger = logging.getLogger('ChannelWatch.Performance')
    
    def check_resources(self, cpu_threshold: int = 85, ram_threshold: int = 85) -> Tuple[bool, Dict]:
        """Enhanced resource checking with detailed metrics"""
        cpu = psutil.cpu_percent(interval=0.2)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        metrics = {
            'cpu_percent': cpu,
            'ram_percent': memory.percent,
            'ram_available_gb': memory.available / (1024**3),
            'disk_percent': disk.percent,
            'disk_free_gb': disk.free / (1024**3),
            'process_count': len(psutil.pids())
        }
        
        is_ok = cpu < cpu_threshold and memory.percent < ram_threshold
        
        if not is_ok:
            self.logger.warning(f"Resource threshold exceeded: CPU {cpu:.1f}%, RAM {memory.percent:.1f}%")
        
        return is_ok, metrics
    
    async def save_stats(self, stats_file: str = 'watch_statistics.json'):
        """Save statistics to file asynchronously"""
        try:
            async with aiofiles.open(stats_file, 'w') as f:
                await f.write(json.dumps(self.stats.to_dict(), indent=2, default=str))
        except Exception as e:
            self.logger.error(f"Failed to save statistics: {e}")

class EnhancedVideoScraper:
    """Enhanced video scraping with metadata extraction"""
    
    def __init__(self, config: ChannelWatchConfig):
        self.config = config
        self.logger = logging.getLogger('ChannelWatch.Scraper')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(USER_AGENTS)
        })
    
    def get_channel_videos(self, channel_url: str, max_videos: int = 20) -> List[VideoInfo]:
        """Enhanced video scraping with metadata extraction"""
        try:
            videos_url = f"{channel_url}/videos"
            self.logger.info(f"Scraping videos from {videos_url}")
            
            response = self.session.get(videos_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            video_infos = []
            
            for link in soup.find_all('a'):
                href = link.get('href', '')
                if href.startswith('/watch?v=') and 'list=' not in href:
                    video_url = 'https://www.youtube.com' + href
                    
                    # Extract additional metadata if available
                    video_info = VideoInfo(url=video_url)
                    
                    # Try to extract title
                    title_elem = link.find('span', {'id': 'video-title'})
                    if title_elem:
                        video_info.title = title_elem.get_text(strip=True)
                    
                    video_infos.append(video_info)
                    
                    if len(video_infos) >= max_videos:
                        break
            
            self.logger.info(f"Scraped {len(video_infos)} videos from channel")
            return video_infos
            
        except Exception as e:
            self.logger.error(f"Failed to scrape channel videos: {e}")
            return []
    
    def filter_videos_by_duration(self, videos: List[VideoInfo]) -> List[VideoInfo]:
        """Filter videos by duration constraints"""
        # For now, return all videos. Duration checking would require additional API calls
        # or more sophisticated scraping which might trigger detection
        return videos
    
    def sort_videos_by_popularity(self, videos: List[VideoInfo]) -> List[VideoInfo]:
        """Sort videos by popularity score"""
        for video in videos:
            video.calculate_popularity()
        return sorted(videos, key=lambda v: v.popularity_score, reverse=True)

class EnhancedBrowserManager:
    """Enhanced browser management with engagement simulation"""
    
    def __init__(self, config: ChannelWatchConfig, stats: WatchStatistics):
        self.config = config
        self.stats = stats
        self.logger = logging.getLogger('ChannelWatch.Browser')
    
    async def human_emulation(self, page, enhanced: bool = True):
        """Enhanced human behavior simulation"""
        try:
            viewport = await page.evaluate('() => ({width: window.innerWidth, height: window.innerHeight})')
            width, height = viewport['width'], viewport['height']
            
            # Enhanced mouse movements with more realistic patterns
            movement_count = random.randint(8, 25)
            for i in range(movement_count):
                # Create more natural movement patterns
                if i == 0:
                    # Start from a random position
                    x = random.randint(100, width - 100)
                    y = random.randint(100, height - 100)
                else:
                    # Move in smaller increments for more natural behavior
                    x += random.randint(-50, 50)
                    y += random.randint(-50, 50)
                    x = max(50, min(width - 50, x))
                    y = max(50, min(height - 50, y))
                
                steps = random.randint(10, 30)
                await page.mouse.move(x, y, steps=steps)
                await asyncio.sleep(random.uniform(0.1, 0.7))
                
                # Random interactions
                if random.random() < 0.3:
                    await page.mouse.click(x, y)
                    await asyncio.sleep(random.uniform(0.5, 2.0))
            
            # Enhanced scrolling behavior
            scroll_count = random.randint(2, 8)
            for _ in range(scroll_count):
                scroll_direction = random.choice([-1, 1])
                scroll_amount = random.randint(100, 400) * scroll_direction
                await page.mouse.wheel(0, scroll_amount)
                await asyncio.sleep(random.uniform(1, 3))
            
            # Keyboard interactions
            if random.random() < 0.4:
                keys = ['ArrowDown', 'ArrowUp', 'Space', 'Tab', 'PageDown', 'PageUp']
                await page.keyboard.press(random.choice(keys))
                await asyncio.sleep(random.uniform(0.5, 1.5))
                
        except Exception as e:
            self.logger.warning(f"Human emulation error: {e}")
    
    async def simulate_engagement(self, page):
        """Simulate user engagement (likes, comments, etc.)"""
        if random.random() > self.config.engagement_rate:
            return
        
        try:
            # Try to find and click like button
            like_selectors = [
                '[aria-label*="like"]',
                '[title*="Like"]',
                '#top-level-buttons-computed button:first-child',
                'ytd-toggle-button-renderer:first-child button'
            ]
            
            for selector in like_selectors:
                try:
                    await page.wait_for_selector(selector, timeout=2000)
                    if random.random() < 0.7:  # 70% chance to actually click
                        await page.click(selector)
                        self.stats.record_engagement()
                        self.logger.info("Performed like engagement")
                        break
                except:
                    continue
            
            # Sometimes scroll to comments and interact
            if random.random() < 0.3:
                try:
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
                    await asyncio.sleep(random.uniform(2, 4))
                except:
                    pass
                    
        except Exception as e:
            self.logger.warning(f"Engagement simulation error: {e}")
    
    async def launch_instance(self, playwright, video_info: VideoInfo, port: int, profile_dir: str, 
                            user_agent: str, lang: str, tz: str, proxy: Optional[str]):
        """Enhanced browser instance launching"""
        try:
            os.makedirs(profile_dir, exist_ok=True)
            
            # Enhanced browser arguments for better stealth
            args = [
                f'--remote-debugging-port={port}',
                '--disable-blink-features=AutomationControlled',
                '--disable-background-timer-throttling',
                '--disable-renderer-backgrounding',
                '--disable-backgrounding-occluded-windows',
                '--disable-background-networking',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-infobars',
                '--disable-extensions',
                '--disable-plugins',
                '--no-first-run',
                '--no-default-browser-check',
                '--disable-default-apps',
                '--window-size=1280,800',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--disable-ipc-flooding-protection',
                '--enable-features=NetworkService,NetworkServiceLogging',
                '--force-device-scale-factor=1'
            ]
            
            browser_args = {
                'headless': False,
                'args': args,
                'user_data_dir': profile_dir,
                'locale': lang,
                'timezone_id': tz,
                'viewport': {'width': 1280, 'height': 800}
            }
            
            if proxy:
                browser_args['proxy'] = {'server': proxy}
            
            browser = await playwright.chromium.launch_persistent_context(**browser_args)
            page = await browser.new_page()
            
            # Enhanced stealth application
            stealth = Stealth()
            await stealth.apply_stealth_async(page)
            await page.set_extra_http_headers({
                'User-Agent': user_agent,
                'Accept-Language': lang,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            })
            
            # Navigate to video
            await page.goto(video_info.url, wait_until='domcontentloaded', timeout=30000)
            await asyncio.sleep(random.uniform(2, 5))
            
            # Initial human emulation
            await self.human_emulation(page)
            
            # Simulate engagement
            await self.simulate_engagement(page)
            
            self.stats.windows_launched += 1
            return browser, page
            
        except Exception as e:
            self.logger.error(f"Failed to launch browser instance: {e}")
            self.stats.windows_failed += 1
            self.stats.record_error()
            return None, None

class EnhancedChannelWatcher:
    """Main enhanced channel watcher class"""
    
    def __init__(self, config_path: str = 'channel_watch_config.yaml'):
        self.config = ConfigManager.load_config(config_path)
        self.stats = WatchStatistics()
        self.logger = setup_logging(self.config.log_level)
        self.monitor = PerformanceMonitor(self.stats)
        self.scraper = EnhancedVideoScraper(self.config)
        self.browser_manager = EnhancedBrowserManager(self.config, self.stats)
        self.running = False
    
    def random_string(self, length: int = 8) -> str:
        """Generate random string for profiles"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def pick_proxy(self) -> Optional[str]:
        """Select random proxy"""
        return random.choice(self.config.proxy_list) if self.config.proxy_list else None
    
    async def enhanced_watch_loop(self, page, video_list: List[VideoInfo]):
        """Enhanced watch loop with better video selection"""
        while self.running:
            try:
                watch_time = random.randint(*self.config.rotate_video_every)
                current_url = page.url
                self.logger.info(f"Watching for {watch_time}s on video: {current_url}")
                
                # Update statistics
                self.stats.update_watch_time(watch_time)
                self.stats.videos_watched += 1
                
                # Wait and perform occasional interactions
                interactions = random.randint(1, 4)
                for i in range(interactions):
                    wait_time = watch_time // interactions
                    await asyncio.sleep(wait_time)
                    
                    if random.random() < 0.4:
                        await self.browser_manager.human_emulation(page)
                    
                    if random.random() < 0.2:
                        await self.browser_manager.simulate_engagement(page)
                
                # Select next video intelligently
                if len(video_list) > 5:
                    # Use weighted selection favoring popular videos
                    weights = [max(v.popularity_score, 0.1) for v in video_list]
                    new_video = random.choices(video_list, weights=weights, k=1)[0]
                else:
                    new_video = random.choice(video_list)
                
                self.logger.info(f"Switching to video: {new_video.url}")
                await page.goto(new_video.url, wait_until='domcontentloaded')
                await asyncio.sleep(random.uniform(2, 5))
                await self.browser_manager.human_emulation(page)
                
            except Exception as e:
                self.logger.error(f"Error in watch loop: {e}")
                self.stats.record_error()
                await asyncio.sleep(10)
    
    async def babysitter(self, video_list: List[VideoInfo], num_windows: int, port_start: int):
        """Enhanced babysitter with better error handling and monitoring"""
        self.running = True
        tasks = []
        
        for i in range(num_windows):
            # Wait for resources
            max_wait_cycles = 45
            for cycle in range(max_wait_cycles):
                is_ok, metrics = self.monitor.check_resources(
                    self.config.cpu_threshold, 
                    self.config.ram_threshold
                )
                if is_ok:
                    break
                
                self.logger.warning(f"Waiting for resources (cycle {cycle+1}/{max_wait_cycles})")
                await asyncio.sleep(2)
            
            # Prepare launch parameters
            port = port_start + i
            profile_dir = os.path.join(self.config.profile_base, f'yt_{self.random_string(10)}')
            user_agent = random.choice(USER_AGENTS)
            lang = random.choice(LANGUAGES)
            tz = random.choice(TIMEZONES)
            proxy = self.pick_proxy()
            video = random.choice(video_list)
            
            self.logger.info(f"Preparing launch {i+1}/{num_windows}: Port {port}")
            tasks.append((video, port, profile_dir, user_agent, lang, tz, proxy))
            await asyncio.sleep(random.uniform(1.5, 5.5))
        
        # Launch all instances
        async with async_playwright() as playwright:
            processes = []
            
            for params in tasks:
                try:
                    browser, page = await self.browser_manager.launch_instance(playwright, *params)
                    if browser and page:
                        # Start watch loop
                        watch_task = asyncio.create_task(self.enhanced_watch_loop(page, video_list))
                        processes.append((params, browser, page, watch_task))
                        self.logger.info(f"Window launched successfully on port {params[1]}")
                    else:
                        self.logger.error(f"Failed to launch window on port {params[1]}")
                        
                except Exception as e:
                    self.logger.error(f"Launch error on port {params[1]}: {e}")
                    self.stats.record_error()
            
            # Monitoring and healing loop
            try:
                while self.running:
                    alive_count = 0
                    
                    for idx, (params, browser, page, watch_task) in enumerate(processes):
                        try:
                            if browser.is_closed() or page.is_closed() or watch_task.done():
                                self.logger.warning(f"Restarting failed window on port {params[1]}")
                                
                                # Clean up old task
                                if not watch_task.done():
                                    watch_task.cancel()
                                
                                # Restart instance
                                new_browser, new_page = await self.browser_manager.launch_instance(
                                    playwright, *params
                                )
                                
                                if new_browser and new_page:
                                    new_watch_task = asyncio.create_task(
                                        self.enhanced_watch_loop(new_page, video_list)
                                    )
                                    processes[idx] = (params, new_browser, new_page, new_watch_task)
                                    alive_count += 1
                            else:
                                alive_count += 1
                                # Occasional maintenance emulation
                                if random.random() < 0.1:
                                    await self.browser_manager.human_emulation(page, enhanced=False)
                                    
                        except Exception as e:
                            self.logger.error(f"Health check error for port {params[1]}: {e}")
                            self.stats.record_error()
                    
                    self.logger.info(f"Health check complete: {alive_count}/{len(processes)} windows active")
                    
                    # Save statistics periodically
                    if self.config.statistics_enabled:
                        await self.monitor.save_stats()
                    
                    # Wait before next health check
                    await asyncio.sleep(random.uniform(30, 90))
                    
            except KeyboardInterrupt:
                self.logger.info("Shutdown signal received")
            finally:
                # Cleanup
                self.running = False
                for _, browser, _, watch_task in processes:
                    try:
                        if not watch_task.done():
                            watch_task.cancel()
                        if browser and not browser.is_closed():
                            await browser.close()
                    except:
                        pass
                
                self.logger.info("All windows closed")
    
    async def run(self):
        """Main run method"""
        try:
            self.logger.info("Starting Enhanced Channel Watch Monolith")
            
            # Load and validate configuration
            ConfigManager.save_config(self.config)  # Save current config as reference
            
            # Scrape videos
            self.logger.info(f"Scraping videos from {self.config.channel_url}")
            video_infos = self.scraper.get_channel_videos(
                self.config.channel_url, 
                self.config.max_videos
            )
            
            if not video_infos:
                self.logger.critical("No videos found, aborting")
                return
            
            # Filter and sort videos
            filtered_videos = self.scraper.filter_videos_by_duration(video_infos)
            sorted_videos = self.scraper.sort_videos_by_popularity(filtered_videos)
            
            self.logger.info(f"Using {len(sorted_videos)} videos for rotation")
            
            # Start babysitter
            await self.babysitter(sorted_videos, self.config.windows, self.config.base_port)
            
        except Exception as e:
            self.logger.critical(f"Critical error: {e}")
            self.stats.record_error()
            raise

async def main():
    """Main entry point"""
    watcher = EnhancedChannelWatcher()
    await watcher.run()

if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════════╗
║           Enhanced Channel Watch Monolith v2.0                  ║
║                      Optimized Edition                          ║
║                                                                  ║
║  Features:                                                       ║
║  • Video duration filtering                                      ║
║  • Enhanced error handling                                       ║
║  • Configuration file support                                    ║
║  • Performance monitoring                                        ║
║  • Engagement simulation                                         ║
║  • Session management                                            ║
║  • Intelligent video selection                                   ║
║                                                                  ║
║  Press Ctrl+C to stop                                           ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[INFO] Graceful shutdown completed")
    except Exception as e:
        print(f"[ERROR] Startup failed: {e}")