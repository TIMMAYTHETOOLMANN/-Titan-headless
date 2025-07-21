# -Titan-headless

StreamBoost: Nexus Edition - A tool to boost your stream numbers across multiple platforms.

## Implementations

This repository contains multiple implementations:
1. **Python Version** (`streamboost.py`) - Advanced browser automation with Playwright
2. **Shell Version** (`streamboost.sh`) - Original bash script for Ubuntu 22.04+
3. **🆕 Enhanced Channel Watch Monolith** - Optimized YouTube channel view simulation

## 🚀 Enhanced Channel Watch Monolith (NEW)

### Overview
Fully autonomous, randomized, undetectable YouTube channel view simulation with 7+ advanced optimizations.

### 🎯 Enhanced Features
1. **Video Duration Checking** - Skip videos that are too short/long
2. **Better Error Handling** - Comprehensive recovery mechanisms
3. **Configuration File Support** - YAML/JSON config files
4. **Performance Monitoring** - Real-time statistics and resource tracking
5. **Video Engagement Simulation** - Realistic likes and interaction patterns
6. **Cookie & Session Management** - Enhanced browser fingerprinting
7. **Intelligent Video Selection** - Popularity-based smart rotation

### Quick Start (Enhanced Version)
```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Run setup (optional)
python setup_enhanced.py

# Test system
python test_enhanced_system.py

# Run enhanced version
python streamboost_channel_watch_enhanced.py
```

### Configuration
Edit `channel_watch_config.yaml`:
```yaml
channel_url: "https://www.youtube.com/@timmaythetoolan"
windows: 20
engagement_rate: 0.3
cpu_threshold: 85
ram_threshold: 85
```

📖 **[Read Full Enhanced Documentation](./ENHANCED_DOCS.md)**

---

## Python Implementation (Original)

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
