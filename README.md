# -Titan-headless

StreamBoost: Nexus Edition - A tool to boost your stream numbers across multiple platforms.

## Implementations

This repository contains two implementations:
1. **Python Version** (`streamboost.py`) - Advanced browser automation with Playwright
2. **Shell Version** (`streamboost.sh`) - Original bash script for Ubuntu 22.04+

## Python Implementation (Recommended)

### Features

- **Advanced Browser Automation**: Uses Playwright with stealth detection evasion
- **Resource Management**: Monitors CPU/RAM and staggers window launches
- **Self-Healing**: Automatically restarts failed browser instances
- **Human Emulation**: Simulates realistic mouse movements, scrolling, and clicks
- **Multi-Platform Support**: YouTube, Kick, and Twitch simultaneously
- **Proxy Support**: Built-in proxy rotation capabilities
- **Unique Profiles**: Isolated browser profiles prevent session conflicts
- **Cross-Platform**: Works on Windows, macOS, and Linux

### Quick Start

```bash
# Install dependencies and setup
python setup.py

# Run StreamBoost
python streamboost.py
```

### Configuration

Edit the `Config` class in `streamboost.py`:

```python
class Config:
    TARGET_ACCOUNT = "your_username"
    YOUTUBE_WINDOWS = 10
    KICK_WINDOWS = 11
    TWITCH_WINDOWS = 15
    # Add your proxies here:
    PROXY_LIST = [
        'http://user:pass@proxy1:port',
        'http://user:pass@proxy2:port',
    ]
```

### Requirements

- Python 3.8+
- 4GB+ RAM recommended for multiple windows
- Internet connection
- Optional: Proxy servers for enhanced anonymity

## StreamBoost Script (Shell Version)

This repository contains `streamboost.sh`, an all-in-one deployment script that opens multiple streaming windows on Ubuntu 22.04+.

### Features

- Automatically installs Chromium/Firefox if missing
- Opens multiple browser windows for YouTube, Kik, and Twitch
- Configurable account names and window counts
- Built-in help documentation

### Usage

```bash
# Show help
./streamboost.sh --help

# Run the script (requires GUI/X11 session)
./streamboost.sh
```

### Requirements

- Ubuntu 22.04+ with Xorg running (needs a GUI session)
- Sudo privileges for package installation

### Configuration

Edit the variables at the top of `streamboost.sh` to customize:
- Target account name
- Number of windows per platform
- Streaming URLs
