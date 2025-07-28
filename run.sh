#!/bin/bash

# ===================================================
#    Titan Headless Enhanced - Linux/macOS Launcher
# ===================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================================${NC}"
echo -e "${GREEN}   Titan Headless Enhanced - Linux/macOS Launcher${NC}"
echo -e "${BLUE}====================================================${NC}"
echo

# Function to print colored messages
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check Node.js installation
log_info "Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    log_error "Node.js is not installed or not in PATH."
    log_info "Please install Node.js from https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node --version)
log_info "Node.js found: $NODE_VERSION"

# Check npm installation
if ! command -v npm &> /dev/null; then
    log_error "npm is not installed or not in PATH."
    exit 1
fi

echo

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    log_info "Installing dependencies..."
    log_info "This may take a few minutes on first run..."
    
    if ! npm install puppeteer-extra puppeteer-extra-plugin-stealth random-useragent proxy-chain faker axios; then
        log_warn "Standard install failed, trying with --force..."
        npm install --force puppeteer-extra puppeteer-extra-plugin-stealth random-useragent proxy-chain faker axios
    fi
else
    log_info "Dependencies already present."
fi

echo

# OS-specific optimizations
log_info "Optimizing for headless environment..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    log_info "Detected Linux - installing headless packages..."
    
    # Check if we can run sudo commands
    if command -v sudo &> /dev/null && sudo -n true 2>/dev/null; then
        log_info "Installing system dependencies for headless Chrome..."
        sudo apt-get update -qq || log_warn "Could not update package list"
        sudo apt-get install -y \
            libnss3 \
            libatk1.0-0 \
            libatk-bridge2.0-0 \
            libx11-xcb1 \
            fonts-liberation \
            libappindicator3-1 \
            xdg-utils \
            libxss1 \
            libgconf-2-4 \
            libxtst6 \
            libxrandr2 \
            libasound2 \
            libpangocairo-1.0-0 \
            libdrm2 \
            libxcomposite1 \
            libxdamage1 \
            libxfixes3 \
            libxkbcommon0 \
            libgtk-3-0 2>/dev/null || log_warn "Some packages could not be installed"
    else
        log_warn "Cannot install system packages (no sudo access)"
        log_info "If Chrome fails to start, please install headless dependencies manually"
    fi
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    log_info "Detected macOS - checking for Homebrew..."
    if command -v brew &> /dev/null; then
        log_info "Homebrew found - ensuring Chrome is available..."
        brew list google-chrome &> /dev/null || log_info "Chrome not installed via Homebrew, using system Chrome"
    else
        log_info "Homebrew not found - using system Chrome"
    fi
fi

echo

# Set environment variables
export HEADLESS=true
export ENABLE_ENHANCEMENTS=true

# Make script executable (if not already)
chmod +x "$0" 2>/dev/null || true

log_info "Starting Titan Headless Enhanced..."
log_info "Press Ctrl+C to stop the application"
echo

# Launch the application
if node main.js; then
    echo
    log_info "Application finished successfully."
else
    EXIT_CODE=$?
    echo
    log_error "Application failed to start. Exit code: $EXIT_CODE"
    log_info "Please check the error messages above."
    exit $EXIT_CODE
fi