#!/usr/bin/env python3
"""
Titan Headless - Static Video Deployment Module
Specialized deployment system for static YouTube video viewing
"""

import asyncio
import logging
import random
import time
import psutil
import requests
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from bs4 import BeautifulSoup

from playwright.async_api import async_playwright, Browser, Page, BrowserContext
from playwright_stealth import Stealth

from deployment_core import (
    DeploymentConfig, ConfigManager, DeploymentValidator, 
    DeploymentMode, StaticVideoConfig
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('static_video_deployment.log'),
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

class VideoScraper:
    """Enhanced video scraper for YouTube channels"""
    
    def __init__(self, config: StaticVideoConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(USER_AGENTS)
        })
    
    def scrape_channel_videos(self) -> List[Dict]:
        """Scrape videos from YouTube channel"""
        try:
            # Extract channel handle from URL
            if '@' in self.config.channel_url:
                channel_handle = self.config.channel_url.split('@')[1].split('/')[0]
                videos_url = f"https://www.youtube.com/@{channel_handle}/videos"
            else:
                videos_url = f"{self.config.channel_url.rstrip('/')}/videos"
            
            logger.info(f"Scraping videos from: {videos_url}")
            
            response = self.session.get(videos_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract video information
            videos = []
            scripts = soup.find_all('script')
            
            for script in scripts:
                if script.string and 'var ytInitialData' in script.string:
                    try:
                        # Extract JSON data
                        json_str = script.string.split('var ytInitialData = ')[1].split(';</script>')[0]
                        data = json.loads(json_str)
                        
                        # Navigate through the data structure to find videos
                        videos = self._extract_videos_from_data(data)
                        break
                    except:
                        continue
            
            if not videos:
                # Fallback: simple link extraction
                video_links = soup.find_all('a', href=True)
                for link in video_links:
                    href = link.get('href', '')
                    if '/watch?v=' in href and href.startswith('/watch'):
                        video_id = href.split('v=')[1].split('&')[0]
                        videos.append({
                            'video_id': video_id,
                            'url': f"https://www.youtube.com/watch?v={video_id}",
                            'title': link.get('title', f'Video {video_id}'),
                            'view_count': 0,
                            'duration': 0
                        })
            
            # Filter videos by duration
            filtered_videos = self._filter_videos_by_duration(videos)
            
            # Sort by popularity if enabled
            if self.config.prefer_popular:
                filtered_videos.sort(key=lambda x: x.get('view_count', 0), reverse=True)
            
            # Limit number of videos
            limited_videos = filtered_videos[:self.config.max_videos]
            
            logger.info(f"Found {len(limited_videos)} suitable videos")
            return limited_videos
            
        except Exception as e:
            logger.warning(f"Failed to scrape channel videos: {str(e)}")
            return []
    
    def _extract_videos_from_data(self, data: Dict) -> List[Dict]:
        """Extract video information from YouTube data structure"""
        videos = []
        
        try:
            # Navigate through the complex YouTube data structure
            contents = data.get('contents', {}).get('twoColumnBrowseResultsRenderer', {}).get('tabs', [])
            
            for tab in contents:
                tab_renderer = tab.get('tabRenderer', {})
                if 'videos' in tab_renderer.get('title', '').lower():
                    content = tab_renderer.get('content', {})
                    section_list = content.get('sectionListRenderer', {}).get('contents', [])
                    
                    for section in section_list:
                        item_section = section.get('itemSectionRenderer', {}).get('contents', [])
                        
                        for item in item_section:
                            grid_renderer = item.get('gridRenderer', {}).get('items', [])
                            
                            for grid_item in grid_renderer:
                                video_renderer = grid_item.get('gridVideoRenderer', {})
                                if video_renderer:
                                    video_info = self._parse_video_renderer(video_renderer)
                                    if video_info:
                                        videos.append(video_info)
            
        except Exception as e:
            logger.debug(f"Error extracting videos from data: {str(e)}")
        
        return videos
    
    def _parse_video_renderer(self, video_renderer: Dict) -> Optional[Dict]:
        """Parse individual video renderer data"""
        try:
            video_id = video_renderer.get('videoId', '')
            if not video_id:
                return None
            
            title_runs = video_renderer.get('title', {}).get('runs', [])
            title = title_runs[0].get('text', '') if title_runs else f'Video {video_id}'
            
            # Extract view count
            view_count_text = ''
            view_text = video_renderer.get('viewCountText', {})
            if isinstance(view_text, dict):
                simple_text = view_text.get('simpleText', '')
                if simple_text:
                    view_count_text = simple_text
            
            view_count = self._parse_view_count(view_count_text)
            
            # Extract duration
            duration_text = video_renderer.get('thumbnailOverlays', [{}])[0].get('thumbnailOverlayTimeStatusRenderer', {}).get('text', {}).get('simpleText', '')
            duration = self._parse_duration(duration_text)
            
            return {
                'video_id': video_id,
                'url': f"https://www.youtube.com/watch?v={video_id}",
                'title': title,
                'view_count': view_count,
                'duration': duration
            }
            
        except Exception as e:
            logger.debug(f"Error parsing video renderer: {str(e)}")
            return None
    
    def _parse_view_count(self, view_text: str) -> int:
        """Parse view count from text"""
        try:
            if not view_text:
                return 0
            
            # Remove non-numeric characters except for K, M, B
            clean_text = view_text.lower().replace(',', '').replace(' views', '').replace(' view', '')
            
            if 'k' in clean_text:
                return int(float(clean_text.replace('k', '')) * 1000)
            elif 'm' in clean_text:
                return int(float(clean_text.replace('m', '')) * 1000000)
            elif 'b' in clean_text:
                return int(float(clean_text.replace('b', '')) * 1000000000)
            else:
                return int(''.join(filter(str.isdigit, clean_text)) or 0)
                
        except:
            return 0
    
    def _parse_duration(self, duration_text: str) -> int:
        """Parse duration from text to seconds"""
        try:
            if not duration_text:
                return 0
            
            parts = duration_text.split(':')
            if len(parts) == 2:  # MM:SS
                return int(parts[0]) * 60 + int(parts[1])
            elif len(parts) == 3:  # HH:MM:SS
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            else:
                return 0
                
        except:
            return 0
    
    def _filter_videos_by_duration(self, videos: List[Dict]) -> List[Dict]:
        """Filter videos by duration criteria"""
        filtered = []
        
        for video in videos:
            duration = video.get('duration', 0)
            if duration == 0:  # Unknown duration, include it
                filtered.append(video)
            elif self.config.min_video_duration <= duration <= self.config.max_video_duration:
                filtered.append(video)
        
        return filtered

class StaticVideoWindow:
    """Individual static video watching window"""
    
    def __init__(self, window_id: int, port: int, profile_dir: Path, config: DeploymentConfig):
        self.window_id = window_id
        self.port = port
        self.profile_dir = profile_dir
        self.config = config
        self.user_agent = random.choice(USER_AGENTS)
        self.browser: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.is_running = False
        self.current_video = None
        self.videos = []
        self.watch_stats = {
            'videos_watched': 0,
            'total_watch_time': 0,
            'engagements': 0
        }
    
    async def launch(self, playwright, videos: List[Dict]) -> bool:
        """Launch browser instance for static video watching"""
        try:
            self.videos = videos
            
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
            
            self.is_running = True
            logger.info(f"✓ Static video window {self.window_id} launched - Port: {self.port}")
            
            return True
            
        except Exception as e:
            logger.error(f"✗ Failed to launch static video window {self.window_id}: {str(e)}")
            return False
    
    async def watch_videos(self):
        """Main video watching loop"""
        while self.is_running:
            try:
                if not self.videos:
                    logger.warning(f"Window {self.window_id}: No videos available")
                    await asyncio.sleep(60)
                    continue
                
                # Select random video
                video = random.choice(self.videos)
                self.current_video = video
                
                # Watch the video
                await self.watch_video(video)
                
                # Random delay between videos
                delay = random.randint(*self.config.static_video.rotate_video_every)
                await asyncio.sleep(delay)
                
            except Exception as e:
                logger.error(f"Error in watch loop for window {self.window_id}: {str(e)}")
                await asyncio.sleep(30)
    
    async def watch_video(self, video: Dict):
        """Watch a specific video"""
        try:
            logger.info(f"Window {self.window_id}: Watching '{video['title']}'")
            
            # Navigate to video
            await self.page.goto(video['url'], wait_until='domcontentloaded', timeout=30000)
            
            # Human emulation
            await self.human_emulation()
            
            # Simulate engagement
            if random.random() < self.config.static_video.engagement_rate:
                await self.simulate_engagement()
            
            # Update statistics
            self.watch_stats['videos_watched'] += 1
            watch_time = random.randint(*self.config.static_video.rotate_video_every)
            self.watch_stats['total_watch_time'] += watch_time
            
        except Exception as e:
            logger.debug(f"Error watching video in window {self.window_id}: {str(e)}")
    
    async def human_emulation(self):
        """Simulate human behavior while watching video"""
        try:
            # Wait for page to load
            await asyncio.sleep(random.uniform(2, 5))
            
            # Click play button if video is paused
            try:
                play_button = await self.page.query_selector('.ytp-large-play-button')
                if play_button:
                    await play_button.click()
            except:
                pass
            
            # Random scrolling and mouse movements
            for _ in range(random.randint(2, 4)):
                await self.page.mouse.wheel(0, random.randint(-200, 200))
                await asyncio.sleep(random.uniform(1, 3))
            
            # Simulate seeking behavior occasionally
            if random.random() < 0.3:
                try:
                    progress_bar = await self.page.query_selector('.ytp-progress-bar')
                    if progress_bar:
                        bbox = await progress_bar.bounding_box()
                        if bbox:
                            x = bbox['x'] + random.randint(0, int(bbox['width']))
                            y = bbox['y'] + bbox['height'] / 2
                            await self.page.mouse.click(x, y)
                except:
                    pass
                    
        except Exception as e:
            logger.debug(f"Human emulation error in window {self.window_id}: {str(e)}")
    
    async def simulate_engagement(self):
        """Simulate user engagement (likes, comments, etc.)"""
        try:
            # Try to like the video
            if random.random() < 0.7:
                try:
                    like_button = await self.page.query_selector('button[aria-label*="like"]')
                    if like_button:
                        await like_button.click()
                        await asyncio.sleep(random.uniform(1, 2))
                        self.watch_stats['engagements'] += 1
                        logger.debug(f"Window {self.window_id}: Liked video")
                except:
                    pass
            
            # Try to subscribe (occasionally)
            if random.random() < 0.1:
                try:
                    subscribe_button = await self.page.query_selector('button[aria-label*="Subscribe"]')
                    if subscribe_button:
                        await subscribe_button.click()
                        await asyncio.sleep(random.uniform(1, 2))
                        self.watch_stats['engagements'] += 1
                        logger.debug(f"Window {self.window_id}: Subscribed to channel")
                except:
                    pass
                    
        except Exception as e:
            logger.debug(f"Engagement simulation error in window {self.window_id}: {str(e)}")
    
    async def close(self):
        """Close the browser window"""
        try:
            self.is_running = False
            if self.browser:
                await self.browser.close()
            logger.info(f"🔒 Static video window {self.window_id} closed")
        except Exception as e:
            logger.error(f"Error closing window {self.window_id}: {str(e)}")

class StaticVideoDeployment:
    """Main static video deployment controller"""
    
    def __init__(self, config: DeploymentConfig):
        self.config = config
        self.windows: List[StaticVideoWindow] = []
        self.videos: List[Dict] = []
        self.is_running = False
        self.scraper = VideoScraper(config.static_video)
    
    async def deploy(self):
        """Deploy static video watching windows"""
        if self.config.deployment_mode not in [DeploymentMode.STATIC_VIDEO, DeploymentMode.BOTH]:
            logger.error("Static video deployment not enabled in configuration")
            return
        
        logger.info("🚀 Starting static video deployment...")
        
        # Scrape videos first
        self.videos = self.scraper.scrape_channel_videos()
        if not self.videos:
            logger.error("No videos found to watch")
            return
        
        async with async_playwright() as playwright:
            self.is_running = True
            
            # Launch video watching windows
            await self._deploy_windows(playwright)
            
            if not self.windows:
                logger.error("No windows deployed successfully")
                return
            
            # Start watching tasks
            watch_tasks = [window.watch_videos() for window in self.windows]
            
            logger.info(f"🎬 Static video deployment active - {len(self.windows)} windows watching")
            
            try:
                await asyncio.gather(*watch_tasks)
            except KeyboardInterrupt:
                logger.info("🛑 Shutdown signal received...")
                await self.shutdown()
    
    async def _deploy_windows(self, playwright):
        """Deploy static video watching windows"""
        try:
            logger.info(f"Deploying {self.config.static_video.windows} static video windows")
            
            for i in range(self.config.static_video.windows):
                # Check system resources before launching
                if not self._check_resources():
                    logger.warning("System resources at threshold, delaying launch...")
                    await asyncio.sleep(30)
                    continue
                
                # Create window
                port = self.config.shared.base_port + i
                profile_dir = Path(self.config.shared.profile_base) / f"static_video_{i}"
                
                window = StaticVideoWindow(i, port, profile_dir, self.config)
                
                # Launch window
                if await window.launch(playwright, self.videos):
                    self.windows.append(window)
                
                # Delay between launches
                delay = random.uniform(2, 7)
                await asyncio.sleep(delay)
                
        except Exception as e:
            logger.error(f"Error deploying static video windows: {str(e)}")
    
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
        """Gracefully shutdown all static video windows"""
        self.is_running = False
        
        logger.info("Shutting down static video deployment...")
        
        shutdown_tasks = [window.close() for window in self.windows]
        await asyncio.gather(*shutdown_tasks, return_exceptions=True)
        
        logger.info("✅ Static video deployment shutdown complete")
    
    def status_report(self):
        """Generate status report for static video deployment"""
        total_videos_watched = sum(w.watch_stats['videos_watched'] for w in self.windows)
        total_watch_time = sum(w.watch_stats['total_watch_time'] for w in self.windows)
        total_engagements = sum(w.watch_stats['engagements'] for w in self.windows)
        
        print(f"\n{'='*60}")
        print(f"🎬 STATIC VIDEO DEPLOYMENT STATUS")
        print(f"{'='*60}")
        print(f"Total Windows: {len(self.windows)}")
        print(f"Available Videos: {len(self.videos)}")
        print(f"Videos Watched: {total_videos_watched}")
        print(f"Total Watch Time: {total_watch_time // 3600}h {(total_watch_time % 3600) // 60}m")
        print(f"Total Engagements: {total_engagements}")
        print(f"Channel: {self.config.static_video.channel_url}")
        print(f"Engagement Rate: {self.config.static_video.engagement_rate * 100:.1f}%")
        print(f"{'='*60}\n")

async def main():
    """Main entry point for static video deployment"""
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
        deployment = StaticVideoDeployment(config)
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
    ║               Titan Headless Static Video                   ║
    ║                  Deployment Module v1.0                     ║
    ║                                                              ║
    ║  YouTube static video watching deployment                   ║
    ║  Press Ctrl+C to stop all windows                          ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")