# Stream Boost - Enhanced 16-Module Stream Viewer Emulation

**Node.js + Puppeteer Implementation**

This is a comprehensive stream viewer emulation system using Node.js and Puppeteer, featuring 16 advanced modules for realistic viewer simulation.

## Setup Instructions

The project has already been initialized and dependencies installed. To get started:

```bash
cd stream_boost
npm start
```

## Dependencies

All required dependencies are already installed:
- `puppeteer-extra` - Enhanced Puppeteer with plugin support
- `puppeteer-extra-plugin-stealth` - Stealth detection evasion
- `random-useragent` - Randomized user agents
- `proxy-chain` - Proxy management and anonymization
- `@faker-js/faker` - Fake data generation

## Configuration

Edit the configuration section in `stream_boost.js`:

```javascript
const STREAM_URL = "https://www.youtube.com/watch?v=YOUR_STREAM_ID";
const VIEWER_COUNT = 50;             // Number of viewers
const SESSION_DURATION = 300000;     // Each viewer session length in ms (5 min default)
const PROXY_LIST = [
  "http://user:pass@proxy1.com:8000",
  "http://user:pass@proxy2.com:8000"
  // Add more proxies for scale
];
```

## 16 Advanced Modules

### Core Modules (1-8)
1. **Proxy & Browser Setup** - Automated proxy configuration and browser launching
2. **Hardware Fingerprint Randomization** - CPU cores, memory, and hardware spoofing
3. **OS & Device Profile Emulation** - Dynamic viewport and device characteristics
4. **Human-Like Mouse Interaction** - Realistic mouse movement patterns
5. **Random Scroll Behavior** - Natural scrolling simulation
6. **Random Engagement Actions** - Play/pause, volume, quality changes
7. **Simulate Bandwidth Throttling** - Dynamic network condition emulation
8. **Cookie Persistence** - Encrypted local cache for session continuity

### Stealth Modules (9-14)
9. **Decentralized Viewer Identity** - Unique viewer identification
10. **Random Referrer** - Spoofed traffic sources
11. **Behavioral AI Mimic** - Advanced human behavior simulation
12. **Tab Activity Simulation** - Multi-tab browsing patterns
13. **Stream Quality Auto-Adjust Reaction** - Intelligent quality management
14. **Anti-Fingerprint Layer** - Canvas and WebGL fingerprint protection

### Enhanced Modules (15-16)
15. **Core Viewer Launch** - Orchestrated viewer session management
16. **Account Watch History & Channel Browsing** - Pre-stream browsing to establish realistic watch history

## Key Features

### Historical Browsing Patterns
- Browses random YouTube channels before viewing target stream
- Watches 1-3 videos per channel to build fake watch history
- Makes sessions appear as established users, not empty bot profiles

### Advanced Stealth
- Hardware fingerprinting randomization
- Network bandwidth simulation  
- Cookie and session management
- Anti-detection layers

### Human Emulation
- Realistic mouse movements and scrolls
- Random engagement actions (pause/play, volume, quality)
- Natural viewing behaviors and patterns

## Usage

### Quick Start
```bash
npm test    # Run validation tests
npm start   # Launch stream viewer emulation
```

### Testing
```bash
node test_stream_boost.js
```

The test suite validates:
- All dependencies are correctly installed
- All 16 modules are present in the main script
- Browser setup works with available Chrome installations

## Integration with Titan Headless

This Node.js implementation works alongside the existing Python-based tools in the Titan Headless suite:

- **Python Version**: Advanced Playwright automation (`streamboost.py`)
- **Node.js Version**: Enhanced Puppeteer emulation (`stream_boost.js`)
- **Shell Version**: Original bash script (`streamboost.sh`)

Choose the implementation that best fits your needs and environment.

## Security & Privacy

- All browser sessions are isolated with unique profiles
- Proxy rotation prevents IP detection
- Hardware fingerprinting makes each session unique
- No persistent data storage outside session scope

## Requirements

- Node.js 16+ 
- Chrome/Chromium browser (automatically detected)
- 4GB+ RAM recommended for multiple viewers
- Optional: Proxy servers for enhanced anonymity

## Architecture

Each viewer session:
1. Establishes unique proxy connection
2. Randomizes hardware fingerprints
3. Builds fake watch history on popular channels
4. Navigates to target stream with realistic behavior
5. Simulates human interactions throughout session
6. Automatically closes after configured duration

This creates highly realistic viewer sessions that are virtually indistinguishable from genuine users.