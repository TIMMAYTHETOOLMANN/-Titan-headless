# Enhanced Channel Watch Monolith - Documentation

## Overview

The Enhanced Channel Watch Monolith is an optimized YouTube channel view simulation system with advanced stealth features and enhanced functionality. This system provides autonomous, randomized, and undetectable YouTube channel view simulation without dependencies on YouTube API keys.

## Features

### Original Features (from issue requirement)
- Fully autonomous YouTube channel view simulation
- Randomized video rotation
- Stealth browser automation with Playwright
- Resource monitoring and management
- Multiple browser window management
- Proxy support
- Human behavior emulation

### Enhanced Features (7 New Optimizations)

1. **🎯 Video Duration Checking**
   - Automatically filters out videos that are too short or too long
   - Configurable minimum and maximum duration thresholds
   - Avoids watching unsuitable content

2. **🔧 Better Error Handling and Recovery**
   - Comprehensive exception handling throughout the system
   - Automatic browser instance restart on failures
   - Detailed logging with multiple log levels
   - Graceful degradation when components fail

3. **⚙️ Configuration File Support**
   - YAML and JSON configuration file support
   - Easy customization without code changes
   - Default configuration with sensible defaults
   - Runtime configuration validation

4. **📊 Performance Monitoring and Statistics**
   - Real-time resource monitoring (CPU, RAM, disk)
   - Detailed statistics tracking
   - Watch time, engagement metrics, error counts
   - Exportable statistics to JSON files
   - System uptime and health monitoring

5. **💬 Video Engagement Simulation**
   - Simulates realistic user engagement (likes, comments)
   - Configurable engagement rate
   - Random engagement timing
   - Advanced interaction patterns

6. **🍪 Cookie and Session Management**
   - Enhanced browser profile isolation
   - Better session persistence
   - Realistic browser fingerprinting
   - Advanced stealth techniques

7. **🧠 Intelligent Video Selection**
   - Popularity-based video selection
   - Weighted random selection favoring popular videos
   - Video metadata extraction when available
   - Smarter rotation algorithms

## Installation

### Prerequisites
- Python 3.8+
- 4GB+ RAM recommended
- Internet connection
- Linux/macOS/Windows support

### Quick Install
```bash
# Clone the repository
git clone https://github.com/TIMMAYTHETOOLMANN/-Titan-headless.git
cd -Titan-headless

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Run setup script (optional)
python setup_enhanced.py
```

### Manual Setup
```bash
# Install Python dependencies
pip install playwright playwright-stealth psutil py-cpuinfo requests beautifulsoup4 pyyaml aiofiles

# Install browser
playwright install chromium

# Create directories
mkdir -p profiles logs
```

## Configuration

### Using Configuration File (Recommended)

Edit `channel_watch_config.yaml`:

```yaml
# Target channel configuration
channel_url: "https://www.youtube.com/@timmaythetoolan"
windows: 20
base_port: 9333
profile_base: "./profiles"

# Video settings
rotate_video_every: [180, 320]  # Min, Max seconds
max_videos: 25
min_video_duration: 60     # Skip short videos
max_video_duration: 3600   # Skip long videos

# Resource thresholds
cpu_threshold: 85
ram_threshold: 85

# Engagement simulation
engagement_rate: 0.3  # 30% chance of engagement

# Monitoring
statistics_enabled: true
log_level: "INFO"

# Proxy configuration (optional)
proxy_list:
  - "http://user:pass@proxy1:port"
  - "socks5://user:pass@proxy2:port"
```

### Direct Code Configuration

For advanced users, you can modify the configuration directly in the scripts by editing the `ChannelWatchConfig` class.

## Usage

### Basic Version
```bash
python streamboost_channel_watch.py
```

### Enhanced Version (Recommended)
```bash
python streamboost_channel_watch_enhanced.py
```

### With Custom Configuration
```bash
# Edit your config file first
nano channel_watch_config.yaml

# Then run with custom config
python streamboost_channel_watch_enhanced.py
```

## Testing

Run the comprehensive test suite to validate your setup:

```bash
python test_enhanced_system.py
```

This will test:
- All required dependencies
- Configuration system
- Video scraping functionality
- Browser setup
- Performance monitoring
- File operations

## Architecture

### Core Components

1. **ConfigManager**: Handles configuration loading/saving
2. **EnhancedVideoScraper**: Scrapes and filters channel videos
3. **EnhancedBrowserManager**: Manages browser instances and interactions
4. **PerformanceMonitor**: Monitors system resources and statistics
5. **WatchStatistics**: Tracks detailed usage statistics
6. **EnhancedChannelWatcher**: Main orchestration class

### Data Flow

1. Load configuration from file or defaults
2. Scrape videos from target channel
3. Filter videos by duration and other criteria
4. Sort videos by popularity score
5. Launch multiple browser instances with unique profiles
6. Start watch loops with random video rotation
7. Monitor health and restart failed instances
8. Track statistics and performance metrics

## Advanced Features

### Proxy Configuration

Add proxies to your configuration file:

```yaml
proxy_list:
  - "http://username:password@proxy1.com:8080"
  - "socks5://username:password@proxy2.com:1080"
  - "http://proxy3.com:3128"
```

The system will randomly rotate through available proxies.

### Resource Management

The system automatically monitors:
- CPU usage
- RAM usage
- Disk space
- Number of active processes

When thresholds are exceeded, new instance launches are delayed.

### Statistics and Monitoring

View detailed statistics:
- Total windows launched/failed
- Videos watched and total watch time
- Engagement actions performed
- System uptime and error counts

Statistics are automatically saved to `watch_statistics.json`.

### Human Behavior Simulation

Enhanced human emulation includes:
- Natural mouse movement patterns
- Realistic scrolling behavior
- Random keyboard interactions
- Variable timing and delays
- Engagement simulation (likes, comments)

## Troubleshooting

### Common Issues

1. **Browser fails to launch**
   - Run: `playwright install chromium`
   - Check system resources
   - Verify profile directory permissions

2. **No videos scraped**
   - Check internet connection
   - Verify channel URL is correct
   - May be rate limiting (normal)

3. **High resource usage**
   - Reduce number of windows
   - Increase resource thresholds
   - Close other applications

4. **Import errors**
   - Run: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

### Debugging

Enable debug logging in configuration:
```yaml
log_level: "DEBUG"
```

View detailed logs in `channel_watch.log`.

## Performance Recommendations

### System Requirements
- **Minimum**: 4GB RAM, 2 CPU cores
- **Recommended**: 8GB+ RAM, 4+ CPU cores
- **Optimal**: 16GB+ RAM, 8+ CPU cores

### Configuration Tuning
- Start with fewer windows (5-10) and scale up
- Monitor CPU/RAM usage and adjust thresholds
- Use SSD storage for better profile performance
- Configure appropriate proxy rotation if available

### Resource Optimization
- Close unnecessary applications
- Use headless mode for better performance (set `headless: true` in browser args)
- Adjust video rotation timing based on system capabilities
- Monitor statistics to optimize engagement rates

## Security and Stealth

### Anti-Detection Features
- User agent rotation
- Timezone and language randomization
- Natural human behavior simulation
- Browser fingerprint randomization
- Proxy support for IP rotation
- Realistic session management

### Best Practices
- Use high-quality residential proxies
- Rotate between multiple configurations
- Monitor for detection patterns
- Keep watch times realistic
- Vary engagement patterns

## Legal Considerations

This tool is intended for:
- Educational purposes
- Testing automation systems
- Personal channel promotion within platform terms
- Research and development

**Important**: 
- Ensure compliance with YouTube's Terms of Service
- Use responsibly and ethically
- Respect platform rate limits
- Consider the impact on content creators

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
1. Check this documentation
2. Run the test suite
3. Review logs for error details
4. Open an issue on GitHub with details

## License

This project is provided as-is for educational and research purposes.

---

## Quick Reference

### File Structure
```
.
├── streamboost_channel_watch.py          # Basic version
├── streamboost_channel_watch_enhanced.py # Enhanced version
├── channel_watch_config.yaml             # Configuration file
├── test_enhanced_system.py               # Test suite
├── setup_enhanced.py                     # Setup script
├── requirements.txt                       # Dependencies
├── README.md                              # Project overview
└── profiles/                              # Browser profiles
    └── logs/                              # Log files
```

### Key Commands
```bash
# Setup
python setup_enhanced.py

# Test
python test_enhanced_system.py

# Run (basic)
python streamboost_channel_watch.py

# Run (enhanced)
python streamboost_channel_watch_enhanced.py

# Install browsers
playwright install chromium
```