# -Titan-headless

StreamBoost: Nexus Edition - A tool to boost your stream numbers across multiple platforms.

## StreamBoost Script

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
