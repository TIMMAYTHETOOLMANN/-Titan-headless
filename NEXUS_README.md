# Nexus Maximus v2.0 - Enhanced Titan Headless System

## Overview

Nexus Maximus v2.0 is a comprehensive enhancement to the Titan Headless streaming system, providing advanced multi-platform automation with sophisticated stealth features, human behavior simulation, and resource management.

## 🚀 Key Features

### Advanced Automation
- **Multi-Platform Support**: YouTube, Twitch, and Kick streaming platforms
- **Intelligent Browser Management**: Chromium and Firefox support with stealth configuration
- **Resource Monitoring**: CPU and memory threshold management
- **Proxy Management**: Advanced proxy rotation with geo-filtering capabilities

### Human Behavior Simulation
- **Mouse Movement Simulation**: Natural cursor movement patterns
- **Scroll Behavior**: Realistic scrolling simulation
- **Interaction Patterns**: Safe click simulation on video elements
- **Heartbeat System**: Regular activity to maintain session validity

### Stealth & Security
- **User Agent Rotation**: Dynamic user agent switching
- **Fingerprint Randomization**: Browser fingerprinting protection
- **Headless Operation**: Full support for headless environments
- **Virtual Display**: Automatic Xvfb setup for GUI-less systems

## 📁 File Structure

```
nexus_maximus.py      - Main application with enhanced features
nexus_config.yaml     - Configuration file with all settings
enhance.sh            - Complete setup and installation script
run_nexus.sh          - Launch script with environment setup
validate_nexus.py     - Validation and health check script
test_nexus.py         - Comprehensive test suite
proxies.txt           - Proxy list for rotation
```

## ⚡ Quick Start

### 1. Enhanced Setup
```bash
# Run the complete enhancement setup
./enhance.sh
```

### 2. Validation
```bash
# Validate the installation
python3 validate_nexus.py

# Run comprehensive tests
python3 test_nexus.py
```

### 3. Configuration
Edit `nexus_config.yaml` to customize:
- Platform URLs and viewer counts
- Proxy settings and geo-filtering
- Behavior simulation parameters
- Resource thresholds
- Advanced features (AI chat, CAPTCHA handling)

### 4. Launch
```bash
# Launch Nexus Maximus
./run_nexus.sh
```

## 🔧 Configuration Options

### Streaming Platforms
```yaml
streaming:
  youtube:
    url: "https://www.youtube.com/@timmaythetoolman/live"
    count: 15
    enabled: true
  twitch:
    url: "https://www.twitch.tv/timmaythetoolman"
    count: 15
    enabled: true
  kick:
    url: "https://kick.com/timmaythetoolman"
    count: 15
    enabled: true
```

### Proxy Configuration
```yaml
proxy:
  file: "proxies.txt"
  enabled: true
  rotation_interval: 300
  geo_filtering:
    enabled: false
    countries: ["US", "CA", "GB", "DE", "FR", "AU", "SG"]
```

### Behavior Simulation
```yaml
behavior:
  human_simulation: true
  mouse_movements: true
  scroll_simulation: true
  click_simulation: true
  heartbeat:
    enabled: true
    interval_min: 30
    interval_max: 120
```

### System Resources
```yaml
system:
  resource_monitoring: true
  cpu_threshold: 85
  memory_threshold: 85
  max_concurrent_windows: 50
```

## 🛠️ Advanced Features

### AI Chat Integration (Optional)
- Support for OpenAI API integration
- Configurable chat message generation
- Natural conversation patterns

### CAPTCHA Handling (Optional)
- AntiCaptcha service integration
- Automatic CAPTCHA detection and solving
- Seamless automation continuation

### Proxy Management
- Automatic proxy rotation
- Geographical filtering
- Health checking and validation
- Fallback to direct connection

## 🧪 Testing

### Unit Tests
```bash
python3 test_nexus.py
```

### Validation
```bash
python3 validate_nexus.py
```

### Configuration Testing
Use `nexus_config_test.yaml` for reduced-scale testing with minimal resource usage.

## 📊 Monitoring

### Resource Monitoring
- Real-time CPU and memory usage tracking
- Automatic throttling when thresholds exceeded
- Graceful degradation and recovery

### Logging
- Comprehensive logging with timestamps
- Different log levels for debugging
- Error tracking and reporting

## 🔒 Security & Stealth

### Anti-Detection Features
- User agent rotation
- Fingerprint randomization
- Natural timing variations
- Human-like interaction patterns

### Privacy Protection
- No personal data storage
- Minimal footprint
- Clean session management

## 📈 Performance

### Optimizations
- Efficient resource usage
- Parallel window management
- Smart scheduling and throttling
- Memory leak prevention

### Scalability
- Configurable concurrent windows
- Dynamic resource adjustment
- Platform-specific optimization

## 🚨 Important Notes

### Ethical Usage
- This tool is designed for legitimate testing and monitoring purposes
- Users are responsible for compliance with platform terms of service
- Respect rate limits and platform guidelines

### System Requirements
- Ubuntu 22.04+ (headless supported)
- Python 3.8+
- 4GB+ RAM recommended
- Internet connection for proxy updates

## 🔧 Troubleshooting

### Common Issues

1. **Browser Installation Failures**
   ```bash
   # Manual playwright browser installation
   source .nexusvenv/bin/activate
   python3 -m playwright install chromium
   ```

2. **Virtual Display Issues**
   ```bash
   # Install Xvfb if missing
   sudo apt-get install xvfb
   ```

3. **Permission Errors**
   ```bash
   # Fix script permissions
   chmod +x enhance.sh run_nexus.sh
   ```

### Debug Mode
Enable verbose logging by editing the configuration:
```yaml
system:
  debug_mode: true
  log_level: "DEBUG"
```

## 📝 License

This project is intended for educational and testing purposes. Users must comply with all applicable terms of service and legal requirements.

## 🤝 Contributing

Contributions are welcome! Please ensure all changes include appropriate tests and documentation.

---

**Nexus Maximus v2.0** - Advanced Streaming Automation with Intelligence