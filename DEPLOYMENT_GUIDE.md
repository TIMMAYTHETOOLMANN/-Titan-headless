# 🚀 Titan Headless - Single-Click Deployment Guide

**Ubuntu 22.04+ Optimized | True Single-Click Deployment**

This repository provides **two powerful streaming tools** with **completely automated deployment**:

1. **🎯 StreamBoost** - Multi-platform stream boosting (YouTube, Kick, Twitch)
2. **🎥 YouTube Watcher** - Enhanced channel view simulation with advanced features

## ⚡ Quick Start (Single-Click)

### Option 1: Deploy Everything (Recommended)
```bash
# One command deploys both programs with virtual environments
./deploy_master.sh --auto
```

### Option 2: Interactive Menu
```bash
# Interactive menu with deployment options
./deploy_master.sh
```

### Option 3: Individual Programs
```bash
# Deploy only StreamBoost
./deploy_streamboost.sh

# Deploy only YouTube Watcher  
./deploy_youtube_watcher.sh
```

## ✅ What Single-Click Deployment Does

### Automatic System Setup
- ✅ **Ubuntu 22.04+ compatibility check**
- ✅ **System dependency installation** (browsers, Python packages)
- ✅ **Virtual environment creation** (isolated for each program)
- ✅ **Python dependency installation** (Playwright, Stealth, etc.)
- ✅ **Browser installation** (Chromium, Firefox)
- ✅ **Configuration optimization** for Ubuntu 22.04
- ✅ **Launcher script creation** for future use

### No Manual Steps Required
- ❌ No manual virtual environment creation
- ❌ No manual dependency installation  
- ❌ No manual browser setup
- ❌ No manual configuration
- ❌ No technical knowledge required

## 🎯 StreamBoost Features

**Multi-platform streaming boost with unique port allocation**

- **Advanced Browser Automation** with Playwright + Stealth
- **Resource Management** (CPU/RAM monitoring)
- **Self-Healing** (automatic restart of failed instances)
- **Human Emulation** (realistic mouse movements, scrolling)
- **Multi-Platform Support** (YouTube, Kick, Twitch simultaneously)
- **Proxy Support** (built-in proxy rotation)
- **Unique Profiles** (isolated browser sessions)

### StreamBoost Configuration
Edit variables in `streamboost.sh`:
```bash
TARGET_ACCOUNT="your_username"
YOUTUBE_COUNT=10    # Number of YouTube windows
KIK_COUNT=11       # Number of Kick windows  
TWITCH_COUNT=15    # Number of Twitch windows
```

## 🎥 YouTube Watcher Features

**Enhanced Channel Watch Monolith with 7+ optimizations**

- **Video Duration Checking** (skip too short/long videos)
- **Better Error Handling** (comprehensive recovery)
- **Configuration File Support** (YAML config)
- **Performance Monitoring** (real-time statistics)
- **Video Engagement Simulation** (realistic likes/interactions)
- **Cookie & Session Management** (enhanced fingerprinting)
- **Intelligent Video Selection** (popularity-based rotation)

### YouTube Watcher Configuration
Edit `channel_watch_config.yaml`:
```yaml
channel_url: "https://www.youtube.com/@your_channel"
windows: 27                    # Number of browser windows
engagement_rate: 0.3          # Rate of video interactions
cpu_threshold: 85             # CPU usage limit
ram_threshold: 85             # RAM usage limit
```

## 🖥️ System Requirements

### Minimum Requirements
- **Ubuntu 22.04+** (optimized for this version)
- **Python 3.8+** (automatically verified)
- **4GB+ RAM** (recommended for multiple windows)
- **GUI Session** (X11 or Wayland)
- **Internet connection**
- **Sudo privileges** (for system dependency installation)

### Automatic Compatibility Check
The deployment scripts automatically verify:
- Ubuntu version compatibility
- Python version requirements
- GUI session availability
- System resource adequacy

## 📁 File Structure After Deployment

```
├── deploy_master.sh              # Master deployment script
├── deploy_streamboost.sh         # StreamBoost deployment
├── deploy_youtube_watcher.sh     # YouTube Watcher deployment
├── streamboost.sh                # StreamBoost shell script
├── streamboost.py                # StreamBoost Python version
├── streamboost_channel_watch_enhanced.py  # Enhanced YouTube watcher
├── channel_watch_config.yaml     # YouTube watcher configuration
├── venv_streamboost/             # StreamBoost virtual environment
├── venv_youtube_watcher/         # YouTube watcher virtual environment
├── launch_streamboost.sh         # Quick StreamBoost launcher
├── launch_youtube_watcher.sh     # Quick YouTube watcher launcher
├── launch_both.sh                # Launch both programs
├── stop_all.sh                   # Stop all programs
└── logs/                         # Application logs
```

## 🚀 Usage After Deployment

### Launch Programs
```bash
# Launch individual programs
./launch_streamboost.sh
./launch_youtube_watcher.sh

# Launch both programs simultaneously  
./launch_both.sh

# Stop all programs
./stop_all.sh
```

### Quick System Check
```bash
# Show system info and installation status
./deploy_master.sh
# Select option 5: "Show system information"
```

## ⚙️ Advanced Configuration

### StreamBoost Advanced Settings
For Python version (`streamboost.py`), edit the Config class:
```python
class Config:
    TARGET_ACCOUNT = "your_username"
    YOUTUBE_WINDOWS = 10
    KICK_WINDOWS = 11
    TWITCH_WINDOWS = 15
    # Proxy configuration
    PROXY_LIST = [
        'http://user:pass@proxy1:port',
        'http://user:pass@proxy2:port',
    ]
```

### YouTube Watcher Advanced Settings
Edit `channel_watch_config.yaml` for fine-tuning:
```yaml
min_video_duration: 60        # Skip videos shorter than 60s
max_video_duration: 3600      # Skip videos longer than 1 hour
rotate_video_every: [180, 320] # Rotate videos every 3-5 minutes
max_videos: 25                # Maximum videos to cycle through
statistics_enabled: true      # Enable performance statistics
```

## 🔧 Troubleshooting

### Browser Installation Issues
```bash
# Manual browser installation if needed
sudo apt update
sudo apt install chromium-browser firefox
```

### Virtual Environment Issues
```bash
# Recreate virtual environments
rm -rf venv_streamboost venv_youtube_watcher
./deploy_master.sh
```

### Permission Issues
```bash
# Fix script permissions
chmod +x *.sh
```

### GUI Session Issues
```bash
# Check if GUI session is running
echo $DISPLAY
ps aux | grep -E "(Xorg|Xwayland)"
```

## 📊 Performance Monitoring

Both programs include built-in monitoring:

### Resource Usage
- **CPU monitoring** with configurable thresholds
- **RAM monitoring** with automatic scaling
- **Process management** with self-healing

### Statistics
- **View counts** and engagement tracking
- **Performance metrics** and error rates
- **Session duration** and success rates

## 🛡️ Security Features

### Stealth & Anonymity
- **Browser fingerprint randomization**
- **User agent rotation**
- **Proxy support** (manual configuration)
- **Session isolation** via unique profiles

### Process Isolation
- **Separate virtual environments** for each program
- **Isolated browser profiles** prevent session conflicts
- **Port isolation** with unique debugging ports

## 📝 Logs & Monitoring

### Log Files
- `streamboost_deployment.log` - StreamBoost deployment log
- `youtube_watcher_deployment.log` - YouTube watcher deployment log
- `master_deployment.log` - Master deployment log
- `logs/` - Runtime application logs

### Real-time Monitoring
```bash
# Monitor deployment logs
tail -f *deployment.log

# Monitor application logs  
tail -f logs/*.log
```

## 🆘 Support

### Quick Help
```bash
# Show help for any script
./deploy_master.sh --help
./deploy_streamboost.sh --help
./deploy_youtube_watcher.sh --help
```

### System Information
```bash
# Comprehensive system check
./deploy_master.sh
# Select option 5: "Show system information"
```

## 🎉 Success Verification

After deployment, you should see:
1. ✅ Virtual environments created in `venv_*` directories
2. ✅ Launcher scripts (`launch_*.sh`) created and executable
3. ✅ Configuration files properly configured
4. ✅ All dependencies installed without errors
5. ✅ System compatibility verified

**Ready to boost your streams with true single-click deployment!** 🚀