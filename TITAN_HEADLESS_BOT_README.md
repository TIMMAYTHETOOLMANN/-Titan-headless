# Titan Headless Bot CLI

A user-friendly command-line interface for the Titan Headless multi-platform viewer bot.

## Features

- **Easy Configuration**: Quickly configure viewer counts for YouTube, Twitch, and Kick
- **Real-time Status**: View current bot status and configuration
- **Platform Control**: Enable/disable platforms with viewer count settings
- **URL Management**: Update stream URLs for each platform
- **Validation**: Validate bot setup before running
- **Duration Control**: Run bot for specified time periods
- **Backup & Restore**: Automatic configuration backup and restore

## Quick Start

### View Current Status
```bash
python titan_headless_bot.py --status
```

### Configure Platforms
```bash
# Set viewer counts (0 = disabled)
python titan_headless_bot.py --youtube 25 --twitch 20 --kick 15

# Update URLs
python titan_headless_bot.py --youtube-url "https://youtube.com/live/your-stream"
```

### Run the Bot
```bash
# Run indefinitely
python titan_headless_bot.py --run

# Run for 1 hour (3600 seconds)
python titan_headless_bot.py --run --duration 3600

# Configure and run in one command
python titan_headless_bot.py --youtube 10 --twitch 5 --run
```

### Validate Setup
```bash
python titan_headless_bot.py --validate
```

## Command Reference

### Status Commands
- `--status`: Show current bot configuration and status
- `--validate`: Validate bot setup without running

### Platform Configuration
- `--youtube COUNT`: Set YouTube viewer count (0 to disable)
- `--twitch COUNT`: Set Twitch viewer count (0 to disable)  
- `--kick COUNT`: Set Kick viewer count (0 to disable)

### URL Configuration
- `--youtube-url URL`: Set YouTube stream URL
- `--twitch-url URL`: Set Twitch stream URL
- `--kick-url URL`: Set Kick stream URL

### Runtime Options
- `--run`: Start the bot
- `--duration SECONDS`: Run bot for specified duration

## Examples

### Basic Usage
```bash
# Check current status
python titan_headless_bot.py --status

# Configure 20 YouTube viewers only
python titan_headless_bot.py --youtube 20 --twitch 0 --kick 0

# Run for 30 minutes
python titan_headless_bot.py --run --duration 1800
```

### Advanced Usage
```bash
# Update stream URL and viewer count
python titan_headless_bot.py --youtube 50 --youtube-url "https://youtube.com/live/new-stream"

# Multi-platform configuration
python titan_headless_bot.py --youtube 25 --twitch 20 --kick 15 --run

# Quick validation
python titan_headless_bot.py --validate
```

## Configuration Backup

The bot automatically creates a backup of your configuration when making changes. If the bot is interrupted, it will restore the original configuration on exit.

## Requirements

- All requirements from the main Titan Headless system
- Valid `enhanced_nexus_config.yaml` configuration file
- Working `proxies.txt` file with valid proxies
- `titan_headless.py` in the same directory

## Integration

This CLI tool is a wrapper around the core `titan_headless.py` functionality. All advanced features like:
- AI chat integration
- Stealth features
- Identity persistence
- Proxy rotation
- Error handling

Are automatically inherited from the core system.

## Troubleshooting

### Common Issues

1. **Import Error**: Ensure `titan_headless.py` is in the same directory
2. **Config Not Found**: Ensure `enhanced_nexus_config.yaml` exists
3. **No Proxies**: Ensure `proxies.txt` exists and contains valid proxies
4. **Platform Not Enabled**: Use non-zero viewer counts to enable platforms

### Validation
Always run `--validate` before starting the bot to check for setup issues:

```bash
python titan_headless_bot.py --validate
```

### Status Check
Use `--status` to see current configuration:

```bash
python titan_headless_bot.py --status
```

## Support

For issues with the core Titan Headless functionality, refer to the main project documentation. For CLI-specific issues, check the test suite:

```bash
python test_titan_headless_bot.py
```