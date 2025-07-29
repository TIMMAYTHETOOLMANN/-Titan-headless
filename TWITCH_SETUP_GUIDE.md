# Twitch Persistent Viewers Setup Guide

## Overview

The `twitch_persistent_viewers.py` script provides advanced Twitch viewer emulation with persistent returning viewers. It includes features like returning viewer identity management, WebSocket heartbeat, chat presence simulation, fingerprint spoofing, and staggered join scheduling.

## Prerequisites

### System Requirements
- Python 3.7+
- Internet connection
- Residential proxy list (already provided in `proxies.txt`)

### Dependencies Installation

1. **Install Python dependencies:**
   ```bash
   pip install aiohttp websockets fake-useragent playwright certifi
   ```

2. **Install Playwright browsers:**
   ```bash
   playwright install chromium
   ```

## Configuration

### 1. Update Stream URL
Edit the `STREAM_URL` variable in `twitch_persistent_viewers.py`:
```python
STREAM_URL = "https://www.twitch.tv/YOUR_CHANNEL_NAME"
```

### 2. Proxy Configuration
The script uses the existing `proxies.txt` file with residential proxies. The file format is:
```
ip:port
ip:port
...
```

### 3. Viewer Settings
You can modify the number of viewers in the main execution:
```python
if __name__ == "__main__":
    asyncio.run(run_viewers(20))  # Change 20 to desired number
```

## Usage

### Basic Execution
```bash
python3 twitch_persistent_viewers.py
```

### Testing
Run the test suite to validate setup:
```bash
python3 test_twitch_persistent_viewers.py
```

## Features

### 1. Persistent Identities
- Viewers maintain consistent identities across sessions
- Cookies and localStorage are preserved
- Identity files stored in `viewer_identities/` directory

### 2. WebSocket Heartbeat
- Maintains connection to Twitch's pubsub system
- Sends periodic ping messages every 4 minutes
- Simulates real viewer presence

### 3. Chat Simulation
- Random chat messages from predefined list
- Human-like interaction timing
- Realistic engagement patterns

### 4. Fingerprint Spoofing
- Hardware concurrency spoofing
- Device memory modification
- WebGL renderer spoofing (NVIDIA GTX 1080)
- Plugin enumeration masking

### 5. Staggered Joins
- Random delays between viewer connections (10-90 seconds)
- Prevents "shotgun blast" detection
- Natural viewer arrival simulation

### 6. Residential Proxy Validation
- Validates proxy health before use
- Geographic location checking
- Automatic filtering of non-functional proxies

## File Structure

```
├── twitch_persistent_viewers.py    # Main script
├── test_twitch_persistent_viewers.py  # Test suite
├── proxies.txt                     # Proxy list (existing)
├── viewer_identities/              # Identity storage (auto-created)
│   ├── viewer_0.json
│   ├── viewer_1.json
│   └── ...
└── requirements.txt                # Updated dependencies
```

## Important Notes

### Security & Ethics
- This script is for educational purposes
- Ensure compliance with Twitch Terms of Service
- Use responsibly with proper authorization
- Residential proxies recommended to avoid detection

### Performance
- Default watch time: 10-30 minutes per viewer
- Memory usage scales with number of concurrent viewers
- Proxy validation may take time on first run

### Troubleshooting

1. **Import errors:** Ensure all dependencies are installed
2. **Proxy issues:** Check proxy file format and connectivity
3. **Browser issues:** Run `playwright install chromium`
4. **Permission errors:** Ensure write permissions for identity directory

## Customization

### Chat Messages
Modify the `CHAT_MESSAGES` list to customize viewer interactions:
```python
CHAT_MESSAGES = [
    "Your custom message",
    "Another message",
    # Add more messages
]
```

### Watch Time
Adjust the viewing duration in `launch_viewer()`:
```python
watch_time = random.randint(600, 1800)  # 10-30 minutes
```

### Browser Settings
Modify viewport and user agent settings in the browser context creation section.

## Support

For issues or questions:
1. Run the test suite first: `python3 test_twitch_persistent_viewers.py`
2. Check proxy connectivity and format
3. Verify all dependencies are properly installed
4. Ensure proper Twitch channel URL configuration