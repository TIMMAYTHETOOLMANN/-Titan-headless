# Titan Headless v2.0 - Unified Deployment System

## Overview

Titan Headless v2.0 provides **two separate deployment capabilities** that can be used independently or together:

1. **Live Stream Deployment** - Multi-platform live stream watching (YouTube, Kick, Twitch)
2. **Static Video Deployment** - YouTube static video watching with advanced features

Both systems are production-ready with comprehensive error handling, monitoring, and stealth features.

## 🚀 Quick Start

### Option 1: Use Launcher Scripts (Recommended)

```bash
# For Live Stream Deployment
./launch_live_stream.sh

# For Static Video Deployment  
./launch_static_video.sh
```

### Option 2: Use Main Deployment Script

```bash
# Live Stream Mode
python3 titan_deployment.py --mode live_stream

# Static Video Mode
python3 titan_deployment.py --mode static_video

# Both Modes Simultaneously
python3 titan_deployment.py --mode both
```

### Option 3: Use Individual Modules

```bash
# Direct Live Stream Deployment
python3 live_stream_deployment.py

# Direct Static Video Deployment
python3 static_video_deployment.py
```

## 📋 Installation

### Prerequisites
- Python 3.8+
- 4GB+ RAM recommended
- Internet connection

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Install browser (try one of these)
python -m playwright install chromium
# OR if chromium fails:
python -m playwright install firefox

# Create configuration files
python3 titan_deployment.py --create-configs

# Test the system
python3 test_deployment_system.py
```

## ⚙️ Configuration

The system uses a unified YAML configuration file (`deployment_config.yaml`) that supports both deployment types:

### Deployment Mode Selection
```yaml
deployment_mode: "live_stream"  # Options: "live_stream", "static_video", "both"
```

### Live Stream Configuration
```yaml
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
      url_template: "https://www.kick.com/{account}"
    twitch:
      enabled: true
      windows: 15
      url_template: "https://www.twitch.tv/{account}"
  live_detection:
    check_interval: 30
    fallback_to_videos: true
    max_wait_time: 300
```

### Static Video Configuration
```yaml
static_video:
  channel_url: "https://www.youtube.com/@timmaythetoolan"
  windows: 20
  video_selection:
    max_videos: 25
    min_video_duration: 60
    max_video_duration: 3600
    rotate_video_every: [180, 320]
    prefer_popular: true
  engagement:
    enabled: true
    rate: 0.3
    actions: ["like", "comment", "subscribe"]
```

### Shared Configuration
```yaml
shared:
  browser:
    base_port: 9333
    profile_base: "./profiles"
    window_width: 1280
    window_height: 800
    headless: false
  resources:
    cpu_threshold: 85
    ram_threshold: 85
  proxy:
    enabled: false
    proxy_list: []
  monitoring:
    statistics_enabled: true
    log_level: "INFO"
```

## 🎯 Deployment Capabilities

### 1. Live Stream Deployment

**Purpose**: Watch live streams across multiple platforms
**Platforms**: YouTube Live, Kick, Twitch
**Features**:
- Real-time live stream detection
- Automatic fallback to regular videos when stream ends
- Multi-platform simultaneous deployment
- Live status monitoring and reporting

**Use Cases**:
- Boosting live stream viewer counts
- Multi-platform live stream monitoring
- Automated live content engagement

### 2. Static Video Deployment

**Purpose**: Watch regular YouTube videos (non-live content)
**Platform**: YouTube
**Features**:
- Intelligent video selection based on popularity
- Duration filtering (skip too short/long videos)
- Engagement simulation (likes, comments, subscribes)
- Advanced video scraping and rotation

**Use Cases**:
- Channel video view boosting
- Content discovery simulation
- Long-term video watching campaigns

### 3. Unified Deployment (Both)

**Purpose**: Run both live stream and static video deployments simultaneously
**Features**:
- Independent operation of both systems
- Resource sharing and management
- Consolidated monitoring and reporting

## 🛠️ Advanced Features

### Resource Management
- CPU and RAM threshold monitoring
- Automatic delay when resources are constrained
- Configurable resource limits

### Stealth & Anti-Detection
- User agent rotation
- Realistic human behavior simulation
- Browser fingerprint randomization
- Proxy support for IP rotation

### Monitoring & Statistics
- Real-time performance monitoring
- Detailed statistics tracking
- Health checks and auto-recovery
- Comprehensive logging

### Configuration Management
- YAML-based configuration
- Configuration validation
- Sample configuration generation
- Runtime configuration updates

## 📊 Monitoring & Statistics

### Live Stream Deployment
- Number of active live streams
- Platform-specific window counts
- Live stream detection status
- System resource usage

### Static Video Deployment
- Videos watched count
- Total watch time
- Engagement actions performed
- Video rotation statistics

## 🔧 Troubleshooting

### Common Issues

1. **Browser Installation Failed**
```bash
# Try alternative browser
python -m playwright install firefox
```

2. **Configuration Validation Failed**
```bash
# Validate your configuration
python3 titan_deployment.py --validate-only
```

3. **High Resource Usage**
```bash
# Reduce window counts in configuration
# Increase resource thresholds
# Close other applications
```

4. **No Videos Scraped**
```bash
# Check internet connection
# Verify channel URL format
# May be temporary rate limiting
```

### Debug Mode
```bash
python3 titan_deployment.py --debug --mode live_stream
```

## 📁 File Structure

```
.
├── titan_deployment.py                    # Main unified deployment script
├── live_stream_deployment.py              # Live stream deployment module
├── static_video_deployment.py             # Static video deployment module
├── deployment_core.py                     # Core configuration and utilities
├── deployment_config.yaml                 # Main configuration file
├── launch_live_stream.sh                  # Live stream launcher script
├── launch_static_video.sh                 # Static video launcher script
├── test_deployment_system.py              # Comprehensive test suite
├── requirements.txt                       # Python dependencies
├── profiles/                              # Browser profiles directory
└── logs/                                  # Log files directory
```

## 🚀 Production Deployment

### System Requirements
- **Minimum**: 4GB RAM, 2 CPU cores
- **Recommended**: 8GB+ RAM, 4+ CPU cores
- **Optimal**: 16GB+ RAM, 8+ CPU cores

### Configuration Tuning
1. Start with fewer windows (5-10) and scale up
2. Monitor CPU/RAM usage and adjust thresholds
3. Use SSD storage for better profile performance
4. Configure proxy rotation for enhanced stealth

### Security Best Practices
- Use high-quality residential proxies
- Rotate between multiple configurations
- Monitor for detection patterns
- Keep watch times realistic
- Vary engagement patterns

## 🔗 Migration from Previous Versions

### From streamboost.py
- Live streaming functionality → Use `live_stream_deployment.py`
- Multi-platform support → Configure platforms in `deployment_config.yaml`

### From streamboost_channel_watch_enhanced.py
- Static video watching → Use `static_video_deployment.py`
- Enhanced features → All included in new static video deployment

## 🧪 Testing

Run the comprehensive test suite:
```bash
python3 test_deployment_system.py
```

This validates:
- Configuration system
- Deployment modules
- Video scraping functionality
- Resource management
- Integration points

## 📄 License & Legal

This tool is intended for:
- Educational purposes
- Testing automation systems
- Personal channel promotion within platform terms
- Research and development

**Important**: Ensure compliance with platform Terms of Service and use responsibly.

## 🆘 Support

For issues and questions:
1. Check this documentation
2. Run the test suite
3. Review logs for error details
4. Validate configuration files

---

## Summary

Titan Headless v2.0 successfully implements the required **two separate deployment capabilities**:

1. **Live Stream Deployment** - Production-ready multi-platform live streaming system
2. **Static Video Deployment** - Advanced YouTube video watching system

Both systems feature:
- ✅ Modular architecture for independent deployment
- ✅ Sound logic with comprehensive error handling
- ✅ Production-ready monitoring and resource management
- ✅ Unified configuration system
- ✅ Extensive testing and validation

The system can deploy either capability independently or both simultaneously, providing maximum flexibility for different use cases.