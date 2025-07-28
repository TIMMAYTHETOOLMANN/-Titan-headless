# 🚀 Titan Headless Enhanced - Drop-In Deployment System

**Enhanced 10-Module Stream Boost Suite with One-Click Cross-Platform Deployment**

This enhanced deployment system provides a comprehensive, drop-in solution for advanced stream viewing automation with intelligent OS detection, proxy management, and human-like behavior simulation.

## ⚡ One-Click Deployment

### Windows
```batch
# Double-click or run from command prompt
run.bat
```

### Linux/macOS
```bash
# Make executable and run
chmod +x run.sh
./run.sh
```

## 🎯 Enhanced Features (10 Modules)

### 1. **OS Detection & Auto-Optimization**
- Automatic platform detection (Windows/Linux/macOS)
- Environment-specific optimizations
- Headless server support with automatic package installation

### 2. **Smart Dependency Manager**
- Automatic npm dependency installation
- Fallback installation with --force flag
- Package.json auto-generation

### 3. **Headless Server Optimization**
- Ubuntu 22.04+ automatic package installation
- Chrome/Chromium dependency management
- Virtual display support

### 4. **Proxy Geo + Health Check**
- Real-time proxy health validation
- Latency monitoring
- Geographic diversity checking

### 5. **Fake Media Devices**
- WebRTC device enumeration spoofing
- Fake microphone and webcam presence
- Advanced WebRTC fingerprint randomization

### 6. **System Load Simulation**
- CPU usage simulation
- Memory allocation patterns
- Realistic system behavior mimicking

### 7. **Persistent Cookies + LocalStorage**
- Session persistence across restarts
- Encrypted cookie storage
- Visitor identity management

### 8. **Human-Like Actions**
- Randomized mouse movements
- Realistic keyboard interactions
- Natural scroll behavior
- Video engagement simulation

### 9. **Session Recovery**
- Automatic crash detection
- Intelligent restart mechanisms
- Proxy rotation on failure

### 10. **One-Click Launcher**
- Cross-platform deployment
- Zero-configuration startup
- Integrated error handling

## 📁 File Structure

```
├── enhancements.js     # 10-module enhancement system
├── main.js            # Enhanced main application
├── run.bat            # Windows launcher
├── run.sh             # Linux/macOS launcher
├── test_enhancements.js # Validation test suite
└── package.json       # Auto-generated dependencies
```

## 🔧 Configuration

### Environment Variables
```bash
export STREAM_URL="https://www.youtube.com/watch?v=YOUR_STREAM_ID"
export VIEWER_COUNT=50
export SESSION_DURATION=300000
export HEADLESS=true
export ENABLE_ENHANCEMENTS=true
```

### Direct Configuration (main.js)
```javascript
const CONFIG = {
    STREAM_URL: "https://www.youtube.com/watch?v=YOUR_STREAM_ID",
    VIEWER_COUNT: 50,
    SESSION_DURATION: 300000, // 5 minutes
    PROXY_LIST: [
        "http://user:pass@proxy1.com:8000",
        "http://user:pass@proxy2.com:8000"
    ],
    HEADLESS: true,
    ENABLE_ENHANCEMENTS: true
};
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
node test_enhancements.js
```

## 🎯 Advanced Features

### Hardware Spoofing
- CPU core count randomization
- Memory size spoofing
- GPU string randomization
- WebGL parameter manipulation

### Browser Fingerprint Evasion
- User agent rotation
- Viewport randomization
- Canvas fingerprint blocking
- Hardware concurrency spoofing

### Behavioral AI
- Watch history simulation
- Channel browsing patterns
- Realistic engagement timing
- Natural interaction flows

## 📋 Requirements

### System Requirements
- **Node.js**: 14.0+ (20.0+ recommended)
- **Memory**: 2GB+ (4GB+ recommended for multiple sessions)
- **Platform**: Windows 10+, Ubuntu 18.04+, macOS 10.14+

### Dependencies (Auto-Installed)
- puppeteer-extra
- puppeteer-extra-plugin-stealth
- random-useragent
- proxy-chain
- faker
- axios

## 🚀 Quick Start

1. **Download/Clone** the repository
2. **Run launcher** for your platform:
   - Windows: Double-click `run.bat`
   - Linux/macOS: `chmod +x run.sh && ./run.sh`
3. **Wait** for automatic setup and launch
4. **Monitor** console output for session status

## 🔍 Troubleshooting

### Common Issues

**Dependencies fail to install:**
```bash
# Manual installation
npm install --force puppeteer-extra puppeteer-extra-plugin-stealth random-useragent proxy-chain faker axios
```

**Chrome not found on Linux:**
```bash
# Install Chrome/Chromium
sudo apt-get install google-chrome-stable
# OR
sudo apt-get install chromium-browser
```

**Permission errors on Linux:**
```bash
# Make scripts executable
chmod +x run.sh test_enhancements.js
```

### Debug Mode
```bash
# Enable verbose logging
export DEBUG=puppeteer:*
node main.js
```

## 🛡️ Security Features

- **Proxy anonymization** with proxy-chain
- **Fingerprint randomization** across sessions
- **Stealth detection evasion** with puppeteer-extra-plugin-stealth
- **Session isolation** with unique browser profiles
- **Cookie encryption** for persistent sessions

## 📊 Monitoring

The system provides real-time monitoring of:
- Active session count
- Proxy health status
- Memory usage patterns
- Session success rates
- Error recovery statistics

## 🔄 Integration

### With Existing Code
The enhanced system seamlessly integrates with existing `stream_boost` functionality while adding advanced features.

### API Usage
```javascript
const { main, launchEnhancedViewer } = require('./main.js');

// Launch single enhanced viewer
await launchEnhancedViewer('http://proxy:8000', 'custom_session_id');

// Launch full application
await main();
```

---

**Built for maximum compatibility and zero-configuration deployment across all major platforms.**