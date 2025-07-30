# Titan Headless Bot - Usage Guide

## Overview

Titan Headless is a sophisticated multi-platform viewer/engagement bot that supports Twitch, YouTube, and Kick streaming platforms. It's fully configuration-driven and includes advanced features like AI chat, proxy rotation, stealth browsing, and identity persistence.

## Features

- **Multi-Platform Support**: Twitch, YouTube, Kick
- **Configuration-Driven**: All settings in `enhanced_nexus_config.yaml`
- **Proxy Support**: Built-in proxy validation and rotation
- **AI Chat** (Optional): Context-aware chat responses using OpenAI API
- **Advanced Stealth**: Playwright-based browser automation with anti-detection
- **Identity Persistence**: Maintains viewer identities across sessions
- **Error Handling**: Comprehensive error logging and recovery

## Quick Start

### 1. Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 2. Configuration

Edit `enhanced_nexus_config.yaml` to configure:

- **Platform URLs**: Set your target streams
- **Viewer Counts**: Number of viewers per platform
- **Proxy Settings**: Configure proxy usage
- **AI Chat**: Enable/disable AI responses (requires OpenAI API key)

```yaml
streaming:
  youtube:
    url: "https://www.youtube.com/@your-channel/live"
    channel: "your-channel"
    count: 25
    enabled: true
  twitch:
    url: "https://www.twitch.tv/your-channel"
    channel: "your-channel"
    count: 20
    enabled: true
  kick:
    url: "https://kick.com/your-channel"
    channel: "your-channel"
    count: 15
    enabled: true

# Optional: AI Chat Configuration
advanced:
  ai_chat:
    enabled: false  # Set to true to enable
    provider: "openai"
    api_key: ""     # Add your OpenAI API key
```

### 3. Proxy Setup

The bot uses `proxies.txt` by default. The file should contain one proxy per line in format:
```
ip:port
```

Example:
```
45.159.219.183:80
31.12.75.210:80
104.25.28.146:80
```

### 4. Running the Bot

```bash
python3 titan_headless.py
```

## Advanced Configuration

### AI Chat Settings

To enable AI-powered chat responses:

1. Get an OpenAI API key from https://platform.openai.com/
2. Update `enhanced_nexus_config.yaml`:

```yaml
advanced:
  ai_chat:
    enabled: true
    provider: "openai"
    api_key: "your-openai-api-key-here"
```

The AI will generate contextual chat messages based on recent chat history.

### Proxy Configuration

```yaml
proxy:
  file: "proxies.txt"
  enabled: true
  rotation_interval: 180  # Rotate every 3 minutes
  health_check_interval: 300
```

### Behavior Simulation

```yaml
behavior:
  human_simulation: true
  mouse_movements: true
  scroll_simulation: true
  click_simulation: true
  engagement_simulation: true
```

### Watch Patterns

```yaml
watch_patterns:
  live_stream:
    min: 300    # 5 minutes minimum
    max: 3600   # 1 hour maximum
    avg: 1200   # 20 minutes average
```

## Output and Monitoring

The bot provides detailed console output:

```
[INFO] Validating 38609 proxies...
[INFO] 1250 proxies validated.
[TWITCH][0] Proxy 45.159.219.183:80
[TWITCH][0] Watch 15 min
[YOUTUBE][0] Proxy 31.12.75.210:80
[YOUTUBE][0] Sent AI chat: Nice stream!
[KICK][0] Proxy 104.25.28.146:80
```

## Identity Persistence

The bot maintains viewer identities in the `viewer_identities/` directory:
- Cookies are preserved between sessions
- Each viewer slot has a unique identity
- Random usernames are generated automatically

## Error Handling

- Automatic proxy rotation on failure
- Screenshot capture on errors
- Graceful handling of missing elements
- Retry mechanisms for failed connections

## Testing

Run the test suite to validate your setup:

```bash
python3 test_titan_basic.py
```

This validates:
- Configuration loading
- Proxy file format
- Script syntax
- Identity system
- Platform configurations

## Troubleshooting

### Common Issues

1. **No valid proxies found**
   - Check proxy file format
   - Verify proxies are working
   - Reduce proxy validation timeout

2. **Playwright browser not found**
   - Run: `playwright install chromium`

3. **Import errors**
   - Install requirements: `pip install -r requirements.txt`

4. **AI chat not working**
   - Verify OpenAI API key is valid
   - Check internet connectivity
   - Ensure AI chat is enabled in config

### Debug Mode

Add debug logging by modifying the script or checking error screenshots in the working directory.

## Security Notes

- Use high-quality proxies for best results
- Rotate identities regularly
- Monitor for platform detection
- Respect platform terms of service
- Use reasonable viewer counts

## Performance Tips

- Start with lower viewer counts
- Monitor CPU/RAM usage
- Use headless mode for better performance
- Distribute load across multiple proxies
- Consider running on multiple machines for scale

## Support

For issues or questions:
1. Check the test suite output
2. Verify configuration format
3. Check proxy quality
4. Review console output for errors