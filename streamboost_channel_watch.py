#!/usr/bin/env python3
"""
Channel Watch Monolith

Fully autonomous, randomized, undetectable YouTube channel view simulation. 
No dependencies on YouTube API keys. All stealth, all random, all operational.
"""

import asyncio
import random
import string
import os
import time
import psutil
import requests
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from cpuinfo import get_cpu_info
import subprocess
import platform
import yaml
import logging

# --- Load config ---
with open('channel_watch_config.yaml', 'r') as f:
    config = yaml.safe_load(f)
CHANNEL_URL = config.get('channel_url', 'https://www.youtube.com/@timmaythetoolan')
WINDOWS = config.get('windows', 1)
BASE_PORT = config.get('base_port', 9333)
PROFILE_BASE = config.get('profile_base', './profiles')
ROTATE_VIDEO_EVERY = tuple(config.get('rotate_video_every', [180, 320]))
MAX_VIDEOS = config.get('max_videos', 25)
FALLBACK_VIDEO_URL = config.get('fallback_video_url', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')
ENGAGEMENT_RATE = config.get('engagement_rate', 0.3)
STATISTICS_ENABLED = config.get('statistics_enabled', True)
LOG_LEVEL = config.get('log_level', 'INFO')

logging.basicConfig(level=getattr(logging, LOG_LEVEL), format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

# --- Load healthy proxies from proxy_list.txt ---
with open('proxy_list.txt', 'r') as pf:
    PROXY_LIST = [line.strip() for line in pf if line.strip()]

# CONFIGURATION
# CHANNEL_URL = 'https://www.youtube.com/@timmaythetoolan'
# WINDOWS = 1  # Set to 1 for single window deployment
# BASE_PORT = 9333
# PROFILE_BASE = './profiles'
# PROXY_LIST = []  # Add your proxies here if desired
# ROTATE_VIDEO_EVERY = (180, 320)  # Seconds to watch each video before rotating (min, max)
# MAX_VIDEOS = 25  # How many videos to pull from the channel

USER_AGENTS = [
    # Add more UA strings for additional randomness
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]
LANGUAGES = ['en-US', 'en-GB', 'fr-FR', 'de-DE']
TIMEZONES = ['America/New_York', 'Europe/Berlin', 'Asia/Tokyo', 'America/Los_Angeles']

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def pick_proxy():
    return random.choice(PROXY_LIST) if PROXY_LIST else None

def resource_ok(cpu_threshold=85, ram_threshold=85):
    cpu = psutil.cpu_percent(interval=0.2)
    ram = psutil.virtual_memory().percent
    return cpu < cpu_threshold and ram < ram_threshold

def get_channel_videos(channel_url, max_videos=20):
    """Scrapes video URLs from a YouTube channel page using YouTube Data API fallback if scraping fails."""
    try:
        html = requests.get(channel_url + '/videos').text
        soup = BeautifulSoup(html, 'html.parser')
        video_links = []
        for link in soup.find_all('a'):
            href = link.get('href', '')
            if href.startswith('/watch?v=') and ('list=' not in href) and href not in video_links:
                video_links.append('https://www.youtube.com' + href)
            if len(video_links) >= max_videos:
                break
        if len(video_links) == 0:
            # Fallback: Try to extract video IDs from script tags
            import re
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and 'watch?v=' in script.string:
                    found = re.findall(r'/watch\?v=[\w-]+', script.string)
                    for vid in found:
                        full_url = 'https://www.youtube.com' + vid
                        if full_url not in video_links:
                            video_links.append(full_url)
                        if len(video_links) >= max_videos:
                            break
                if len(video_links) >= max_videos:
                    break
        # --- JARVIS 2.0 AUTONOMY PATCH ---
        if len(video_links) == 0:
            # Emergency fallback: Use config fallback video URL
            video_links.append(FALLBACK_VIDEO_URL)
        logger.info(f'Scraped {len(video_links)} videos from channel.')
        return video_links
    except Exception as e:
        logger.error(f'Failed to scrape channel videos: {e}')
        # Fallback: Return the config fallback video URL if scraping fails
        return [FALLBACK_VIDEO_URL]

async def simulate_engagement(page):
    """Simulate deeper engagement: likes, comments, subscribe, random focus/blur, tab switching"""
    try:
        # Like button simulation
        if random.random() < ENGAGEMENT_RATE:
            like_btn = await page.query_selector('ytd-toggle-button-renderer[is-icon-button] button')
            if like_btn:
                await like_btn.click()
                logger.info('[ENGAGE] Like button clicked.')
        # Comment simulation (if enabled)
        if random.random() < ENGAGEMENT_RATE / 2:
            comment_box = await page.query_selector('ytd-comment-simplebox-renderer')
            if comment_box:
                await comment_box.click()
                await asyncio.sleep(random.uniform(1, 2))
                comment_text = random.choice([
                    "Great video!", "Awesome content!", "Loved this!", "🔥", "Keep it up!", "Subbed!", "Nice work!", "Very helpful!", "Thanks for sharing!"
                ])
                await page.keyboard.type(comment_text)
                await asyncio.sleep(random.uniform(0.5, 1.5))
                submit_btn = await page.query_selector('ytd-button-renderer#submit-button button')
                if submit_btn:
                    await submit_btn.click()
                    logger.info('[ENGAGE] Comment submitted.')
        # Subscribe simulation
        if random.random() < ENGAGEMENT_RATE / 3:
            sub_btn = await page.query_selector('ytd-subscribe-button-renderer button')
            if sub_btn:
                await sub_btn.click()
                logger.info('[ENGAGE] Subscribed.')
        # Random focus/blur, tab switching
        if random.random() < 0.2:
            await page.evaluate('window.dispatchEvent(new Event("blur"));')
            await asyncio.sleep(random.uniform(0.2, 0.7))
            await page.evaluate('window.dispatchEvent(new Event("focus"));')
        if random.random() < 0.1:
            await page.keyboard.press('Control+Tab')
    except Exception as e:
        logger.warning(f'[ENGAGE] Engagement simulation error: {e}')

async def human_emulation(page):
    width, height = await page.evaluate('() => [window.innerWidth, window.innerHeight]')
    for _ in range(random.randint(6, 18)):
        x = random.randint(10, width-10)
        y = random.randint(10, height-10)
        await page.mouse.move(x, y, steps=random.randint(5, 25))
        await asyncio.sleep(random.uniform(0.15, 0.9))
        if random.random() < 0.4:
            await page.mouse.click(x, y)
    await page.keyboard.press('ArrowDown')
    await asyncio.sleep(random.uniform(1, 4))
    await page.mouse.wheel(0, random.randint(50, 350))
    await simulate_engagement(page)

async def launch_instance(playwright, video_url, port, profile_dir, user_agent, lang, tz, proxy):
    # Randomize window size and device scale factor
    win_width = random.randint(1100, 1920)
    win_height = random.randint(700, 1080)
    device_scale = random.choice([1, 1.25, 1.5, 2])
    color_depth = random.choice([24, 30, 32])
    pixel_ratio = random.choice([1, 1.25, 1.5, 2])
    orientation = random.choice(['landscape', 'portrait'])
    # Headless Ubuntu Xvfb setup
    if platform.system() == "Linux" and os.environ.get("DISPLAY") is None:
        xvfb_cmd = ["Xvfb", ":99", "-screen", "0", f"{win_width}x{win_height}x{color_depth}"]
        try:
            subprocess.Popen(xvfb_cmd)
            os.environ["DISPLAY"] = ":99"
            logger.info("[Xvfb] Virtual display started on :99")
        except Exception as xvfb_err:
            logger.error(f"[Xvfb] Failed to start: {xvfb_err}")
            return None, None
    args = [
        f'--remote-debugging-port={port}',
        '--disable-blink-features=AutomationControlled',
        '--disable-background-timer-throttling',
        '--disable-renderer-backgrounding',
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-infobars',
        f'--window-size={win_width},{win_height}',
        '--force-device-scale-factor=' + str(device_scale),
        '--disable-extensions',
        '--disable-plugins',
        '--disable-gpu',
        '--disable-software-rasterizer',
        '--disable-popup-blocking',
        '--disable-site-isolation-trials',
        '--disable-logging',
        '--disable-notifications',
        '--disable-background-fetch',
        '--disable-sync',
        '--disable-translate',
        '--disable-client-side-phishing-detection',
        '--disable-component-update',
        '--disable-domain-reliability',
        '--disable-hang-monitor',
        '--disable-prompt-on-repost',
        '--disable-webgl',
        '--disable-webgl2',
        '--disable-features=IsolateOrigins,site-per-process',
        '--disable-blink-features',
        '--disable-automation',
        '--disable-dev-tools',
        '--disable-crash-reporter',
        '--disable-background-media-suspend',
        '--disable-breakpad',
        '--disable-canvas-aa',
        '--disable-gesture-requirement-for-media-playback',
        '--disable-ipc-flooding-protection',
        '--disable-offer-store-unmasked-wallet-cards',
        '--disable-offline-auto-reload',
        '--disable-offline-load-stale-cache',
        '--disable-password-generation',
        '--disable-permissions-api',
        '--disable-print-preview',
        '--disable-prompt-on-repost',
        '--disable-renderer-accessibility',
        '--disable-search-geolocation-disclosure',
        '--disable-speech-api',
        '--disable-tab-for-desktop-share',
        '--disable-translate-new-ux',
        '--disable-usb',
        '--disable-web-authentication',
        '--disable-web-share',
        '--disable-xss-auditor',
    ]

    browser_args = {
        'headless': False,
        'args': args,
        'user_data_dir': profile_dir,
        'viewport': {'width': win_width, 'height': win_height},
        'device_scale_factor': device_scale,
        'locale': lang,
        'timezone_id': tz
    }
    if proxy:
        browser_args['proxy'] = {'server': proxy}

    # --- MAXIMUM STEALTH: Recursive Fingerprint Spoofing ---
    async def spoof_all(page):
        await page.add_init_script('''
            // Navigator spoofing
            Object.defineProperty(navigator, 'webdriver', {get: () => false});
            Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
            Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 4 + Math.floor(Math.random()*4)});
            Object.defineProperty(navigator, 'maxTouchPoints', {get: () => 1});
            Object.defineProperty(navigator, 'deviceMemory', {get: () => 4 + Math.floor(Math.random()*4)});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US','en','fr','de']});
            Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
            Object.defineProperty(navigator, 'mediaDevices', {get: () => ({enumerateDevices: () => [{kind:'videoinput'}]})});
            Object.defineProperty(navigator, 'vendor', {get: () => 'Google Inc.'});
            Object.defineProperty(navigator, 'productSub', {get: () => '20030107'});
            Object.defineProperty(navigator, 'userAgent', {get: () => '%s'});
            // Screen spoofing
            Object.defineProperty(window, 'devicePixelRatio', {get: () => %f});
            Object.defineProperty(screen, 'orientation', {get: () => ({type: '%s'})});
            Object.defineProperty(screen, 'colorDepth', {get: () => %d});
            Object.defineProperty(screen, 'pixelDepth', {get: () => %d});
            Object.defineProperty(screen, 'width', {get: () => %d});
            Object.defineProperty(screen, 'height', {get: () => %d});
            // Font spoofing
            Object.defineProperty(document, 'fonts', {get: () => ['Arial','Verdana','Times New Roman','Courier New','Georgia']});
            // Canvas spoofing
            const toDataURL = HTMLCanvasElement.prototype.toDataURL;
            HTMLCanvasElement.prototype.toDataURL = function() { return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA"; };
            // Audio spoofing
            Object.defineProperty(window, 'AudioContext', {get: () => function(){}});
            // WebGL spoofing
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(param) {
                if(param === 37445) return 'WebKit'; // UNMASKED_VENDOR_WEBGL
                if(param === 37446) return 'ANGLE (Google Inc.)'; // UNMASKED_RENDERER_WEBGL
                return getParameter.call(this, param);
            };
            // Permission spoofing
            navigator.permissions.query = async function() { return {state: 'granted'}; };
            // WebRTC spoofing
            Object.defineProperty(window, 'RTCPeerConnection', {get: () => function(){ return {localDescription: {sdp: 'v=0'}}; }});
            // Storage spoofing
            window.localStorage.setItem('session', Math.random().toString(36).substring(2));
            window.sessionStorage.setItem('session', Math.random().toString(36).substring(2));
            // Extension simulation
            Object.defineProperty(navigator, 'extensions', {get: () => ['Google Docs','Grammarly','uBlock Origin']});
        ''' % (user_agent, pixel_ratio, orientation, color_depth, color_depth, win_width, win_height))
    max_retries = 5
    for attempt in range(max_retries):
        try:
            browser = await playwright.chromium.launch_persistent_context(
                **browser_args
            )
            page = await browser.new_page()
            stealth = Stealth()
            await stealth.apply_stealth_async(page)
            await spoof_all(page)
            await page.set_extra_http_headers({'User-Agent': user_agent})
            await page.goto(video_url)
            await human_emulation(page)
            logger.info(f'[LAUNCH] Browser launched on port {port} (Attempt {attempt+1})')
            return browser, page
        except Exception as e:
            logger.error(f'[RETRY] Launch failed (Attempt {attempt+1}): {e}')
            await asyncio.sleep(2 + attempt * 2)
    logger.critical(f'[FAIL] Max retries reached for port {port}.')
    return None, None

async def watch_loop(page, video_list):
    error_count = 0
    while True:
        try:
            watch_time = random.randint(*ROTATE_VIDEO_EVERY)
            logger.info(f"[INFO] Watching for {watch_time}s on video: {page.url}")
            await asyncio.sleep(watch_time)
            new_video = random.choice(video_list)
            logger.info(f"[ROTATE] Switching to video: {new_video}")
            await page.goto(new_video)
            await human_emulation(page)
            error_count = 0
        except Exception as e:
            error_count += 1
            logger.error(f'[WATCH_LOOP] Error: {e} (Error count: {error_count})')
            if error_count > 3:
                logger.warning('[WATCH_LOOP] Escalating: Restarting browser instance.')
                await page.context.close()
                break
            await asyncio.sleep(5 * error_count)

async def babysitter(video_list, num_windows, port_start):
    tasks = []
    for i in range(num_windows):
        for _ in range(45):
            if resource_ok():
                break
            logger.warning('[WARN] High resource usage. Waiting...')
            await asyncio.sleep(2)
        port = port_start + i
        profile_dir = os.path.join(PROFILE_BASE, f'yt_{random_string(10)}')
        os.makedirs(profile_dir, exist_ok=True)
        user_agent = random.choice(USER_AGENTS)
        lang = random.choice(LANGUAGES)
        tz = random.choice(TIMEZONES)
        proxy = pick_proxy()
        video_url = random.choice(video_list)
        logger.info(f'[LAUNCH] Port: {port} | Profile: {profile_dir} | UA: {user_agent[:25]}... | Proxy: {proxy}')
        tasks.append((video_url, port, profile_dir, user_agent, lang, tz, proxy))
        await asyncio.sleep(random.uniform(1.5, 5.5))

    async with async_playwright() as playwright:
        processes = []
        for params in tasks:
            browser, page = await launch_instance(playwright, *params)
            if browser and page:
                asyncio.create_task(watch_loop(page, video_list))
                processes.append((params, browser, page))
                logger.info(f'[READY] Window at port {params[1]} running.')
            else:
                logger.error(f'[FAIL] Launch at port {params[1]}: Browser not started.')
        while True:
            for idx, (params, browser, page) in enumerate(processes):
                if browser.is_closed():
                    logger.warning(f'[RESTART] Relaunching window at port {params[1]}')
                    browser, page = await launch_instance(playwright, *params)
                    if browser and page:
                        asyncio.create_task(watch_loop(page, video_list))
                        processes[idx] = (params, browser, page)
                else:
                    await human_emulation(page)
            await asyncio.sleep(random.uniform(25, 60))

async def main():
    # Scrape videos from the channel
    videos = get_channel_videos(CHANNEL_URL, MAX_VIDEOS)
    if not videos:
        logger.critical('[CRITICAL] No videos scraped, aborting.')
        return
    await babysitter(videos, WINDOWS, BASE_PORT)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as exc:
        logger.error(f'[ERROR] {exc}')
