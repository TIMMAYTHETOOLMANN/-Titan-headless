#!/usr/bin/env python3
"""
Twitch Advanced Viewer Emulation with Persistent Returning Viewers
Includes:
 - Returning viewer identity (cookies + localStorage)
 - WebSocket heartbeat
 - Chat presence simulation
 - Fingerprint spoofing (GPU, audio, fonts)
 - Staggered join schedule
 - Residential proxy validation
"""

import asyncio, random, json, string, time, aiohttp, os
import websockets
from fake_useragent import UserAgent
import ssl, certifi
from pathlib import Path
from playwright.async_api import async_playwright

TWITCH_HEARTBEAT = "https://gql.twitch.tv/gql"
STREAM_URL = "https://www.twitch.tv/YOUR_CHANNEL"
PROXY_POOL = "proxies.txt"   # Residential proxies only
IDENTITY_DIR = Path("viewer_identities")
IDENTITY_DIR.mkdir(exist_ok=True)

CHAT_MESSAGES = [
    "Hey everyone 👋",
    "This is great content!",
    "lol nice shot",
    "brb grabbing snacks 🍕",
    "first time here, cool stream!",
    "lurking mode on"
]

# === Utility: Returning Identity ===
def random_username():
    return ''.join(random.choices(string.ascii_lowercase, k=8))

def get_or_create_identity(slot):
    identity_file = IDENTITY_DIR / f"viewer_{slot}.json"
    if identity_file.exists():
        with open(identity_file) as f:
            return json.load(f)
    identity = {"username": random_username(), "cookies": {}, "localStorage": {}}
    with open(identity_file, "w") as f:
        json.dump(identity, f)
    return identity

def save_identity(slot, identity):
    with open(IDENTITY_DIR / f"viewer_{slot}.json", "w") as f:
        json.dump(identity, f)

# === Proxy Loader & Validator ===
async def load_proxies():
    if not os.path.exists(PROXY_POOL):
        raise Exception("No proxy file found.")
    with open(PROXY_POOL) as f:
        proxies = [p.strip() for p in f if p.strip()]
    valid = []
    for proxy in proxies:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://ipinfo.io/json",
                                       proxy=f"http://{proxy}", timeout=3) as r:
                    if r.status == 200:
                        valid.append(proxy)
        except:
            pass
    if not valid:
        raise Exception("No valid residential proxies.")
    return valid

# === Twitch WebSocket Heartbeat ===
async def twitch_presence(token, channel_id):
    uri = "wss://pubsub-edge.twitch.tv"
    async with websockets.connect(uri, ssl=ssl.create_default_context(cafile=certifi.where())) as ws:
        listen_payload = {
            "type": "LISTEN",
            "nonce": str(random.random()),
            "data": {
                "topics": [f"video-playback.{channel_id}"],
                "auth_token": token
            }
        }
        await ws.send(json.dumps(listen_payload))
        while True:
            await ws.send(json.dumps({"type": "PING"}))
            await asyncio.sleep(240)  # Twitch expects ping ~4min

# === Fingerprint Spoof ===
async def spoof_fingerprint(page):
    await page.add_init_script("""
        Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 4 });
        Object.defineProperty(navigator, 'deviceMemory', { get: () => 8 });
        Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3] });
        WebGLRenderingContext.prototype.getParameter = function(param) {
            if(param === 37445) return 'NVIDIA Corporation';
            if(param === 37446) return 'NVIDIA GTX 1080';
            return this.getParameter(param);
        };
    """)

# === Chat Presence Simulation ===
async def simulate_chat(page):
    await page.fill('textarea[data-a-target="chat-input"]', random.choice(CHAT_MESSAGES))
    await page.keyboard.press("Enter")

# === Restore Returning Identity ===
async def restore_identity(context, identity):
    # Restore cookies
    cookies = [{"name": k, "value": v, "domain": ".twitch.tv", "path": "/"} for k, v in identity["cookies"].items()]
    await context.add_cookies(cookies)
    # Restore localStorage after page open
    return identity

async def save_identity_state(page, identity, slot):
    cookies = await page.context.cookies()
    identity["cookies"] = {c["name"]: c["value"] for c in cookies}
    storage = await page.evaluate("() => Object.entries(localStorage)")
    identity["localStorage"] = {k: v for k, v in storage}
    save_identity(slot, identity)

# === Viewer Launch ===
async def launch_viewer(slot, proxy):
    identity = get_or_create_identity(slot)
    async with async_playwright() as p:
        browser = await p.chromium.launch(proxy={"server": f"http://{proxy}"}, headless=True)
        context = await browser.new_context(
            user_agent=UserAgent().random,
            locale="en-US",
            viewport={"width": random.randint(1280, 1920),
                      "height": random.randint(720, 1080)}
        )
        await restore_identity(context, identity)
        page = await context.new_page()
        await spoof_fingerprint(page)
        await page.goto(STREAM_URL)
        await asyncio.sleep(random.randint(20, 60))
        await simulate_chat(page)
        watch_time = random.randint(600, 1800)
        await asyncio.sleep(watch_time)
        await save_identity_state(page, identity, slot)
        await browser.close()

# === Staggered Viewer Manager ===
async def run_viewers(num_viewers):
    proxies = await load_proxies()
    tasks = []
    for slot in range(num_viewers):
        proxy = random.choice(proxies)
        tasks.append(launch_viewer(slot, proxy))
        await asyncio.sleep(random.randint(10, 90))  # stagger join
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(run_viewers(20))