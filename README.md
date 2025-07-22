# -Titan-headless

StreamBoost: Nexus Edition - A tool to boost your stream numbers across multiple platforms.

## 🆕 Titan Headless v2.0 - Unified Deployment System

**NEW: Two Separate Deployment Capabilities**

The system now provides **two independent deployment capabilities** that can be used separately or together:

### 1. 🔴 Live Stream Deployment
- **Multi-platform live streaming** (YouTube Live, Kick, Twitch)
- **Real-time live detection** with automatic fallback
- **Production-ready monitoring** and health checks
- **Independent deployment** from static video system

### 2. 🎬 Static Video Deployment  
- **YouTube video watching** with intelligent selection
- **Advanced engagement simulation** (likes, comments, subscribes)
- **Duration filtering** and popularity-based selection
- **Modular design** separate from live streaming

### 3. 🚀 Quick Start - New Deployment System

```bash
# Option 1: Use launcher scripts (Recommended)
./launch_live_stream.sh      # For live streams
./launch_static_video.sh     # For static videos

# Option 2: Use unified deployment script
python3 titan_deployment.py --mode live_stream    # Live streams only
python3 titan_deployment.py --mode static_video   # Static videos only  
python3 titan_deployment.py --mode both          # Both simultaneously

# Option 3: Use individual modules directly
python3 live_stream_deployment.py     # Direct live stream deployment
python3 static_video_deployment.py    # Direct static video deployment
```

### 4. 📋 Installation & Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install browser
python -m playwright install chromium

# Create configuration files
python3 titan_deployment.py --create-configs

# Validate setup
python3 titan_deployment.py --validate-only

# Run comprehensive tests
python3 test_deployment_system.py
```

### 5. ⚙️ Configuration

The new system uses a unified YAML configuration (`deployment_config.yaml`) supporting both deployment types:

```yaml
# Select deployment mode
deployment_mode: "live_stream"  # Options: "live_stream", "static_video", "both"

# Live stream configuration
live_stream:
  target_account: "timmaythetoolman"
  platforms:
    youtube:
      enabled: true
      windows: 10
      url_template: "https://www.youtube.com/@{account}/live"
    kick:
      enabled: true
      windows: 11
    twitch:
      enabled: true  
      windows: 15

# Static video configuration
static_video:
  channel_url: "https://www.youtube.com/@timmaythetoolan"
  windows: 20
  video_selection:
    max_videos: 25
    min_video_duration: 60
    max_video_duration: 3600
    engagement_rate: 0.3
```

📖 **[Read Full Deployment Documentation](./DEPLOYMENT_DOCS.md)**

---

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
