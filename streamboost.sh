#!/bin/bash
# === StreamBoost: Nexus Edition ===
# All-in-one deploy: opens multiple streaming windows on Ubuntu 22.04+
# Usage: bash streamboost.sh

# --- CONFIGURATION ---
TARGET_ACCOUNT="timmaythetoolman"

YOUTUBE_URL="https://www.youtube.com/@${TARGET_ACCOUNT}/live"
KIK_URL="https://www.kick.com/${TARGET_ACCOUNT}"
TWITCH_URL="https://www.twitch.tv/${TARGET_ACCOUNT}"

YOUTUBE_COUNT=10
KIK_COUNT=11
TWITCH_COUNT=15

BROWSER="chromium-browser"  # fallback: chromium, firefox

# --- FUNCTIONS ---
function log {
    echo -e "\033[1;32m[$(date +%H:%M:%S)] $1\033[0m"
}

function ensure_browser_installed {
    log "Checking for chromium-browser..."
    if ! command -v chromium-browser &>/dev/null; then
        log "chromium-browser not found. Installing..."
        sudo apt-get update
        sudo apt-get install -y chromium-browser || sudo apt-get install -y chromium
    fi

    if command -v chromium-browser &>/dev/null; then
        BROWSER="chromium-browser"
    elif command -v chromium &>/dev/null; then
        BROWSER="chromium"
    elif command -v firefox &>/dev/null; then
        BROWSER="firefox"
    else
        log "No supported browser found. Installing firefox as last resort..."
        sudo apt-get install -y firefox
        BROWSER="firefox"
    fi

    log "Using browser: $BROWSER"
}

function check_xorg {
    if ! pgrep -x "Xorg" >/dev/null; then
        log "No Xorg session detected. You must run this inside a GUI/X11 session."
        exit 1
    fi
}

function open_windows {
    local url=$1
    local count=$2
    local label=$3

    log "Opening $count windows for $label ($url)..."
    for ((i=1; i<=count; i++)); do
        nohup $BROWSER --new-window "$url" >/dev/null 2>&1 &
        sleep 1
    done
    log "$label complete."
}

function selfdoc {
    cat <<EOF
# === StreamBoost Nexus Edition ===

Boost your stream numbers—no drama, no overhead.

## How it Works

- Installs Chromium/Firefox if missing.
- Opens 10x YouTube, 11x Kik, 15x Twitch stream windows.
- Everything is hardcoded. Change config at the top for your needs.

## Usage

\`\`\`bash
bash streamboost.sh
\`\`\`

## Requirements

- Ubuntu 22.04+ with Xorg running (needs a GUI session).
- Sudo privileges for package install.

## Config

Edit variables at the top of this script to change account, stream URLs, or counts.
EOF
}

# --- MAIN EXECUTION ---
if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
    selfdoc
    exit 0
fi

log "===== StreamBoost (JARVIS NEXUS) LAUNCH ====="
check_xorg
ensure_browser_installed

open_windows "$YOUTUBE_URL" "$YOUTUBE_COUNT" "YouTube"
open_windows "$KIK_URL" "$KIK_COUNT" "Kik"
open_windows "$TWITCH_URL" "$TWITCH_COUNT" "Twitch"

log "All streams launched. Mission complete."