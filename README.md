# 🚀 Titan Headless - Single-Click Stream Boost Suite

**Ubuntu 22.04+ Optimized | True Single-Click Deployment | 🆕 Headless Operation Support**

StreamBoost: Nexus Edition + Enhanced YouTube Watcher - Automated stream boosting with **zero manual configuration** and **full headless Ubuntu support**.

## ⚡ Single-Click Deployment (Headless & GUI Support)

**Deploy everything with one command (works in headless environments):**
```bash
./deploy_master.sh --auto
```

**Or use interactive menu:**
```bash
./deploy_master.sh
```

✅ **Automatic virtual environment creation**  
✅ **System dependency installation**  
✅ **Browser setup & configuration**  
✅ **Ubuntu 22.04+ optimization**  
✅ **🆕 Headless operation with Xvfb virtual display**  
✅ **Zero manual steps required**

📖 **[Complete Deployment Guide](./DEPLOYMENT_GUIDE.md)**

---

## 🎯 Headless Operation (New!)

StreamBoost now supports complete headless operation on Ubuntu servers without GUI:

### Features
- **Automatic Xvfb Setup**: Virtual display automatically configured
- **No GUI Required**: Runs on headless Ubuntu 22.04+ servers
- **All Functionality Preserved**: Full feature compatibility in headless mode
- **Zero Configuration**: Headless mode enabled by default

### Quick Headless Start
```bash
# Works on headless Ubuntu servers
./deploy_streamboost.sh

# Or directly run streamboost
python3 streamboost.py

# Test headless functionality
python3 test_headless.py
```

### Headless Requirements
- Ubuntu 22.04+ (headless server)
- Python 3.8+
- Xvfb (automatically installed)
- 4GB+ RAM recommended

---

## 🎯 Two Powerful Tools

### 1. **StreamBoost** - Multi-Platform Stream Boosting
- YouTube, Kick, and Twitch simultaneously
- Advanced browser automation with Playwright
- Resource management and self-healing
- Human emulation and stealth features

### 2. **YouTube Watcher** - Enhanced Channel View Simulation  
- Intelligent video selection and duration checking
- Performance monitoring and statistics
- Video engagement simulation
- Cookie & session management

## Implementations

This repository contains multiple implementations:
1. **Python Version** (`streamboost.py`) - Advanced browser automation with Playwright
2. **Shell Version** (`streamboost.sh`) - Original bash script for Ubuntu 22.04+
3. **🆕 Enhanced Channel Watch Monolith** - Optimized YouTube channel view simulation
4. **🆕 Node.js Version** (`stream_boost/`) - Enhanced 16-module stream viewer emulation with Puppeteer

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

## 🚀 Node.js Implementation (NEW)

### Enhanced 16-Module Stream Viewer Emulation

A comprehensive Node.js + Puppeteer implementation featuring advanced stealth detection evasion and realistic human behavior simulation.

### Key Features

- **16 Advanced Modules**: Complete viewer emulation from proxy setup to watch history simulation
- **Historical Browsing**: Pre-stream channel browsing to establish realistic user profiles
- **Advanced Stealth**: Hardware fingerprinting, bandwidth simulation, anti-detection layers
- **Human Emulation**: Realistic mouse movements, scrolling, engagement actions
- **Proxy Integration**: Built-in proxy rotation and anonymization

### Quick Start (Node.js Version)
```bash
# Navigate to stream_boost directory
cd stream_boost

# Test the implementation
npm test

# Run stream viewer emulation
npm start
```

### Configuration
Edit `stream_boost/stream_boost.js`:
```javascript
const STREAM_URL = "https://www.youtube.com/watch?v=YOUR_STREAM_ID";
const VIEWER_COUNT = 50;
const SESSION_DURATION = 300000; // 5 minutes
```

📖 **[Read Node.js Implementation Guide](./stream_boost/README.md)**

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
    HEADLESS = True  # Default: True for Ubuntu compatibility
    # Add your proxies here:
    PROXY_LIST = [
        'http://user:pass@proxy1:port',
        'http://user:pass@proxy2:port',
    ]
```

### Headless Configuration
- `HEADLESS = True`: Enables headless browser operation (default)
- Automatic Xvfb virtual display setup on Linux systems
- No GUI session required for operation

### Requirements

- Python 3.8+
- 4GB+ RAM recommended for multiple windows
- Internet connection
- Ubuntu 22.04+ (supports both GUI and headless operation)
- Optional: Proxy servers for enhanced anonymity

### Testing Headless Operation

Validate headless functionality with included test suites:

```bash
# Test headless system components
python3 test_headless.py

# Test StreamBoost headless initialization
python3 test_streamboost_headless.py

# Test full enhanced system
python3 test_enhanced_system.py
```

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
