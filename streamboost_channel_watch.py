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

# CONFIGURATION
CHANNEL_URL = 'https://www.youtube.com/@timmaythetoolan'
WINDOWS = 20  # Set how many windows you want to deploy (adjust as needed)
BASE_PORT = 9333
PROFILE_BASE = './profiles'
PROXY_LIST = []  # Add your proxies here if desired
ROTATE_VIDEO_EVERY = (180, 320)  # Seconds to watch each video before rotating (min, max)
MAX_VIDEOS = 25  # How many videos to pull from the channel

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
    """Scrapes video URLs from a YouTube channel page."""
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
        print(f'[INFO] Scraped {len(video_links)} videos from channel.')
        return video_links
    except Exception as e:
        print(f'[ERROR] Failed to scrape channel videos: {e}')
        return []

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

async def launch_instance(playwright, video_url, port, profile_dir, user_agent, lang, tz, proxy):
    args = [
        f'--remote-debugging-port={port}',
        '--disable-blink-features=AutomationControlled',
        '--disable-background-timer-throttling',
        '--disable-renderer-backgrounding',
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-infobars',
        '--window-size=1280,800'
    ]

    browser_args = {
        'headless': False,
        'args': args,
        'user_data_dir': profile_dir
    }
    if proxy:
        browser_args['proxy'] = {'server': proxy}

    browser = await playwright.chromium.launch_persistent_context(
        **browser_args,
        locale=lang,
        timezone_id=tz
    )

    page = await browser.new_page()
    stealth = Stealth()
    await stealth.apply_stealth_async(page)
    await page.set_extra_http_headers({'User-Agent': user_agent})
    await page.goto(video_url)
    await human_emulation(page)
    return browser, page

async def watch_loop(page, video_list):
    while True:
        watch_time = random.randint(*ROTATE_VIDEO_EVERY)
        print(f"[INFO] Watching for {watch_time}s on video: {page.url}")
        await asyncio.sleep(watch_time)
        new_video = random.choice(video_list)
        print(f"[ROTATE] Switching to video: {new_video}")
        await page.goto(new_video)
        await human_emulation(page)

async def babysitter(video_list, num_windows, port_start):
    tasks = []
    for i in range(num_windows):
        for _ in range(45):  # Up to 90s wait if resources are high
            if resource_ok():
                break
            print(f'[WARN] High resource usage. Waiting...')
            await asyncio.sleep(2)
        port = port_start + i
        profile_dir = os.path.join(PROFILE_BASE, f'yt_{random_string(10)}')
        os.makedirs(profile_dir, exist_ok=True)
        user_agent = random.choice(USER_AGENTS)
        lang = random.choice(LANGUAGES)
        tz = random.choice(TIMEZONES)
        proxy = pick_proxy()
        video_url = random.choice(video_list)
        print(f'[LAUNCH] Port: {port} | Profile: {profile_dir} | UA: {user_agent[:25]}... | Proxy: {proxy}')
        tasks.append((video_url, port, profile_dir, user_agent, lang, tz, proxy))
        await asyncio.sleep(random.uniform(1.5, 5.5))  # Random launch interval

    async with async_playwright() as playwright:
        processes = []
        for params in tasks:
            try:
                browser, page = await launch_instance(playwright, *params)
                # Start the background watch/rotate loop
                asyncio.create_task(watch_loop(page, video_list))
                processes.append((params, browser, page))
                print(f'[READY] Window at port {params[1]} running.')
            except Exception as e:
                print(f'[FAIL] Launch at port {params[1]}: {e}')
        try:
            while True:
                for idx, (params, browser, page) in enumerate(processes):
                    if browser.is_closed():
                        print(f'[RESTART] Relaunching window at port {params[1]}')
                        browser, page = await launch_instance(playwright, *params)
                        asyncio.create_task(watch_loop(page, video_list))
                        processes[idx] = (params, browser, page)
                    else:
                        await human_emulation(page)
                await asyncio.sleep(random.uniform(25, 60))
        except KeyboardInterrupt:
            for _, browser, _ in processes:
                await browser.close()
            print('All windows closed.')

async def main():
    # Scrape videos from the channel
    videos = get_channel_videos(CHANNEL_URL, MAX_VIDEOS)
    if not videos:
        print('[CRITICAL] No videos scraped, aborting.')
        return
    await babysitter(videos, WINDOWS, BASE_PORT)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as exc:
        print(f'[ERROR] {exc}')