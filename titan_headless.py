#!/usr/bin/env python3

"""
Titan Headless: All-Platform Viewer/Engagement Bot
* Fully config-driven: reads everything from enhanced_nexus_config.yaml
* Platforms: Twitch, YouTube, Kick
* Uses only proxies.txt (or as specified in config)
* AI chat: only enabled if configured and API key provided (real context-aware responses to real chat)
* Advanced stealth, session, playback, error logging, identity persistence per viewer
* Copilot/coder-friendly, single file!
"""

import asyncio, random, string, time, aiohttp, os, yaml, json, sys, traceback
from pathlib import Path
from playwright.async_api import async_playwright
from playwright_stealth import stealth
import ssl, certifi

try:
    import openai
except ImportError:
    openai = None

# === Load config ===
CONFIG_PATH = "enhanced_nexus_config.yaml"

with open(CONFIG_PATH, 'r') as f:
    CONFIG = yaml.safe_load(f)

PLATFORMS = CONFIG['streaming']
PROXY_FILE = CONFIG.get('proxy', {}).get('file', 'proxies.txt')
AI_CHAT_ENABLED = CONFIG.get('advanced', {}).get('ai_chat', {}).get('enabled', False)
AI_CHAT_API_KEY = CONFIG.get('advanced', {}).get('ai_chat', {}).get('api_key', '')
AI_CHAT_PROVIDER = CONFIG.get('advanced', {}).get('ai_chat', {}).get('provider', 'openai')

IDENTITY_DIR = Path("viewer_identities")
IDENTITY_DIR.mkdir(exist_ok=True)

# === Proxy Loader ===
async def load_proxies():
    if not os.path.exists(PROXY_FILE):
        raise Exception(f"No proxy file found at {PROXY_FILE}")
    with open(PROXY_FILE) as f:
        proxies = [p.strip() for p in f if p.strip()]
    valid = []
    print(f"[INFO] Validating {len(proxies)} proxies...")
    for proxy in proxies:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://ipinfo.io/json",
                        proxy=f"http://{proxy}", timeout=4) as r:
                    if r.status == 200:
                        valid.append(proxy)
        except Exception:
            pass
    if not valid:
        raise Exception("No valid proxies found.")
    print(f"[INFO] {len(valid)} proxies validated.")
    return valid

# === Identity Persistence ===
def random_username():
    return ''.join(random.choices(string.ascii_lowercase, k=8))

def get_or_create_identity(platform, slot):
    identity_file = IDENTITY_DIR / f"{platform}_{slot}.json"
    if identity_file.exists():
        with open(identity_file) as f:
            return json.load(f)
    identity = {"username": random_username(), "cookies": {}, "localStorage": {}}
    with open(identity_file, "w") as f:
        json.dump(identity, f)
    return identity

def save_identity(platform, slot, identity):
    with open(IDENTITY_DIR / f"{platform}_{slot}.json", "w") as f:
        json.dump(identity, f)

async def restore_identity(context, identity, domain):
    cookies = [{"name": k, "value": v, "domain": domain, "path": "/"} for k, v in identity["cookies"].items()]
    if cookies:
        await context.add_cookies(cookies)

async def save_identity_state(page, identity, platform, slot):
    cookies = await page.context.cookies()
    identity["cookies"] = {c["name"]: c["value"] for c in cookies}
    try:
        storage = await page.evaluate("() => Object.entries(localStorage)")
        identity["localStorage"] = {k: v for k, v in storage}
    except Exception:
        identity["localStorage"] = {}
    save_identity(platform, slot, identity)

# === AI Chat Generator ===
async def generate_chat_response(history, platform="twitch"):
    if not AI_CHAT_ENABLED or not AI_CHAT_API_KEY or not openai:
        return None
    try:
        openai.api_key = AI_CHAT_API_KEY
        # Use only last 5 chat messages as context, platform-aware prompt
        context = "\n".join([f"{m['user']}: {m['text']}" for m in history[-5:]])
        prompt = f"You are a real viewer chatting on {platform}. Only reply if you have something human and relevant to say. Current chat:\n{context}\n\nYour message (short, casual, natural):"
        resp = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo", messages=[{"role":"user","content":prompt}],
            max_tokens=40, temperature=0.85, stop=["\n"]
        )
        chat = resp['choices'][0]['message']['content'].strip()
        # Only reply if the model gives a plausible short response
        if 3 < len(chat) < 140:
            return chat
    except Exception as e:
        print(f"[AI CHAT ERROR]: {e}")
    return None

# === Stealth Setup ===
async def stealthify(page):
    await stealth(page)

# === Platform Logic: Twitch ===
async def twitch_viewer(slot, proxy, config):
    from fake_useragent import UserAgent
    url = config["url"]
    channel = config.get("channel", "")
    identity = get_or_create_identity("twitch", slot)
    try:
        async with async_playwright() as p:
            print(f"[TWITCH][{slot}] Proxy {proxy}")
            browser = await p.chromium.launch(proxy={"server": f"http://{proxy}"}, headless=False)
            context = await browser.new_context(
                user_agent=UserAgent().random,
                locale="en-US",
                viewport={"width": random.randint(1280, 1920), "height": random.randint(720, 1080)},
                timezone_id=random.choice(["America/New_York", "Europe/London"])
            )
            await restore_identity(context, identity, ".twitch.tv")
            page = await context.new_page()
            await stealthify(page)
            await page.goto(url, timeout=45000)
            # Accept mature prompt if present
            try:
                await page.click('[data-a-target="player-overlay-mature-accept-button"]', timeout=4000)
            except Exception: pass
            await asyncio.sleep(random.uniform(5, 12))
            # Playback: ensure player loaded, click play, unmute
            try:
                await page.wait_for_selector('button[data-a-target="player-play-pause"]', timeout=20000)
                await page.click('button[data-a-target="player-play-pause"]')
                await asyncio.sleep(1)
                await page.keyboard.press('m')
            except Exception: pass
            # Read recent chat messages
            chat_history = []
            try:
                chat_msgs = await page.query_selector_all('[data-a-target="chat-line-message-body"]')
                for el in chat_msgs[-8:]:
                    txt = (await el.inner_text()).strip()
                    userel = await el.evaluate_handle('node => node.parentElement.parentElement.querySelector(\'span.chat-author__display-name\')')
                    user = await userel.evaluate('el => el.innerText') if userel else "user"
                    chat_history.append({"user": user, "text": txt})
            except Exception: pass
            # AI chat only if allowed and context available
            chat_msg = await generate_chat_response(chat_history, platform="twitch") if chat_history else None
            if chat_msg:
                try:
                    await page.fill('textarea[data-a-target="chat-input"]', chat_msg)
                    await asyncio.sleep(random.uniform(1.2, 2.5))
                    await page.keyboard.press("Enter")
                    print(f"[TWITCH][{slot}] Sent AI chat: {chat_msg}")
                except Exception as e:
                    print(f"[TWITCH][{slot}] Chat fail: {e}")
            # Simulate some human behavior
            await page.mouse.move(random.randint(100, 800), random.randint(100, 400))
            if random.random() < 0.5:
                await page.mouse.wheel(0, random.randint(100, 400))
            watch_time = random.randint(600, 1800)
            print(f"[TWITCH][{slot}] Watch {watch_time//60} min")
            await asyncio.sleep(watch_time)
            await save_identity_state(page, identity, "twitch", slot)
            await browser.close()
    except Exception as e:
        print(f"[TWITCH][{slot}][ERROR] {e}")
        try:
            await page.screenshot(path=f"twitch_error_{slot}.png")
        except Exception: pass

# === Platform Logic: YouTube ===
async def youtube_viewer(slot, proxy, config):
    from fake_useragent import UserAgent
    url = config["url"]
    identity = get_or_create_identity("youtube", slot)
    try:
        async with async_playwright() as p:
            print(f"[YOUTUBE][{slot}] Proxy {proxy}")
            browser = await p.chromium.launch(proxy={"server": f"http://{proxy}"}, headless=False)
            context = await browser.new_context(
                user_agent=UserAgent().random,
                locale="en-US",
                viewport={"width": random.randint(1280, 1920), "height": random.randint(720, 1080)},
                timezone_id=random.choice(["America/New_York", "Europe/London"])
            )
            await restore_identity(context, identity, ".youtube.com")
            page = await context.new_page()
            await stealthify(page)
            await page.goto(url, timeout=45000)
            await asyncio.sleep(random.uniform(5, 12))
            # Ensure player loaded, click play, unmute
            try:
                await page.wait_for_selector('button.ytp-play-button', timeout=20000)
                await page.click('button.ytp-play-button')
                await asyncio.sleep(1)
                await page.keyboard.press('m')
            except Exception: pass
            # Read chat if live
            chat_history = []
            try:
                chat_iframe = await page.query_selector('iframe#chatframe')
                if chat_iframe:
                    chat_page = await chat_iframe.content_frame()
                    chat_lines = await chat_page.query_selector_all('#item-list .style-scope.yt-live-chat-item-list-renderer')
                    for el in chat_lines[-8:]:
                        user = (await el.query_selector('#author-name')).inner_text() if await el.query_selector('#author-name') else "user"
                        txt = (await el.query_selector('#message')).inner_text() if await el.query_selector('#message') else ""
                        chat_history.append({"user": user, "text": txt})
            except Exception: pass
            chat_msg = await generate_chat_response(chat_history, platform="youtube") if chat_history else None
            if chat_msg:
                try:
                    chat_iframe = await page.query_selector('iframe#chatframe')
                    if chat_iframe:
                        chat_page = await chat_iframe.content_frame()
                        await chat_page.fill('#input', chat_msg)
                        await asyncio.sleep(random.uniform(1.2, 2.5))
                        await chat_page.keyboard.press("Enter")
                        print(f"[YOUTUBE][{slot}] Sent AI chat: {chat_msg}")
                except Exception as e:
                    print(f"[YOUTUBE][{slot}] Chat fail: {e}")
            await page.mouse.move(random.randint(100, 800), random.randint(100, 400))
            if random.random() < 0.5:
                await page.mouse.wheel(0, random.randint(100, 400))
            watch_time = random.randint(600, 1800)
            print(f"[YOUTUBE][{slot}] Watch {watch_time//60} min")
            await asyncio.sleep(watch_time)
            await save_identity_state(page, identity, "youtube", slot)
            await browser.close()
    except Exception as e:
        print(f"[YOUTUBE][{slot}][ERROR] {e}")
        try:
            await page.screenshot(path=f"youtube_error_{slot}.png")
        except Exception: pass

# === Platform Logic: Kick ===
async def kick_viewer(slot, proxy, config):
    from fake_useragent import UserAgent
    url = config["url"]
    identity = get_or_create_identity("kick", slot)
    try:
        async with async_playwright() as p:
            print(f"[KICK][{slot}] Proxy {proxy}")
            browser = await p.chromium.launch(proxy={"server": f"http://{proxy}"}, headless=False)
            context = await browser.new_context(
                user_agent=UserAgent().random,
                locale="en-US",
                viewport={"width": random.randint(1280, 1920), "height": random.randint(720, 1080)},
                timezone_id=random.choice(["America/New_York", "Europe/London"])
            )
            await restore_identity(context, identity, ".kick.com")
            page = await context.new_page()
            await stealthify(page)
            await page.goto(url, timeout=45000)
            await asyncio.sleep(random.uniform(5, 12))
            # Ensure playback
            try:
                await page.wait_for_selector('button[data-testid="play-pause"]', timeout=20000)
                await page.click('button[data-testid="play-pause"]')
                await asyncio.sleep(1)
                await page.keyboard.press('m')
            except Exception: pass
            # Chat (Kick)
            chat_history = []
            try:
                chat_msgs = await page.query_selector_all('div.chat-message__text')
                chat_users = await page.query_selector_all('span.chat-message__username')
                for el, userel in zip(chat_msgs[-8:], chat_users[-8:]):
                    txt = (await el.inner_text()).strip()
                    user = (await userel.inner_text()).strip()
                    chat_history.append({"user": user, "text": txt})
            except Exception: pass
            chat_msg = await generate_chat_response(chat_history, platform="kick") if chat_history else None
            if chat_msg:
                try:
                    await page.fill('textarea[data-testid="chat-input"]', chat_msg)
                    await asyncio.sleep(random.uniform(1.2, 2.5))
                    await page.keyboard.press("Enter")
                    print(f"[KICK][{slot}] Sent AI chat: {chat_msg}")
                except Exception as e:
                    print(f"[KICK][{slot}] Chat fail: {e}")
            await page.mouse.move(random.randint(100, 800), random.randint(100, 400))
            if random.random() < 0.5:
                await page.mouse.wheel(0, random.randint(100, 400))
            watch_time = random.randint(600, 1800)
            print(f"[KICK][{slot}] Watch {watch_time//60} min")
            await asyncio.sleep(watch_time)
            await save_identity_state(page, identity, "kick", slot)
            await browser.close()
    except Exception as e:
        print(f"[KICK][{slot}][ERROR] {e}")
        try:
            await page.screenshot(path=f"kick_error_{slot}.png")
        except Exception: pass

# === Main orchestrator ===
async def run():
    proxies = await load_proxies()
    tasks = []
    # Launch all platforms in parallel, each using its own config and count
    for platform, conf in PLATFORMS.items():
        if conf.get('enabled', False):
            viewers = conf.get('count', 1)
            for slot in range(viewers):
                proxy = random.choice(proxies)
                if platform == "twitch":
                    tasks.append(twitch_viewer(slot, proxy, conf))
                elif platform == "youtube":
                    tasks.append(youtube_viewer(slot, proxy, conf))
                elif platform == "kick":
                    tasks.append(kick_viewer(slot, proxy, conf))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(run())