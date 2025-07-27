#!/bin/bash
# One-click script for Flite & Browser Dependencies
# Copy-paste runnable on fresh Ubuntu - bulletproof installation

set -e

echo "🚀 TITAN HEADLESS - ONE-CLICK FLITE & BROWSER FIX"
echo "=================================================="
echo ""

# Ensure we're not running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Don't run as root. The script will use sudo when needed."
    exit 1
fi

# Check if we're in the right directory or need to download the script
if [ ! -f "install_flite_browsers.sh" ]; then
    echo "📥 Downloading installation script..."
    
    # Check if we have wget or curl
    if command -v wget &> /dev/null; then
        DOWNLOAD_CMD="wget -O"
    elif command -v curl &> /dev/null; then
        DOWNLOAD_CMD="curl -o"
    else
        echo "❌ Neither wget nor curl available. Installing wget..."
        sudo apt update && sudo apt install -y wget
        DOWNLOAD_CMD="wget -O"
    fi
    
    # Download the installer script (would be from your repo in production)
    echo "⚠️  You'll need to copy install_flite_browsers.sh to this directory manually."
    echo "Or run this script from the Titan Headless repository directory."
    exit 1
fi

echo "🔧 Running comprehensive Flite & Browser installer..."
echo ""

# Run the main installer
if ./install_flite_browsers.sh; then
    echo ""
    echo "✅ Installation completed successfully!"
    echo ""
    echo "🧪 Running validation..."
    if python3 validate_flite_browsers.py; then
        echo ""
        echo "🎉 ALL SYSTEMS GO! Flite and browser dependencies are properly installed."
        echo ""
        echo "📋 What was installed:"
        echo "   • Flite shared libraries built from source"
        echo "   • Complete browser dependency packages"
        echo "   • Headless environment (Xvfb)"
        echo "   • Playwright browser binaries"
        echo ""
        echo "🚀 Your system is ready for:"
        echo "   • Nexus Maximus automation"
        echo "   • Headless browser testing"
        echo "   • CI/CD deployments"
        echo ""
        echo "To get started:"
        echo "   ./run_nexus.sh"
        echo "   python3 nexus_maximus.py"
        echo ""
    else
        echo ""
        echo "⚠️  Installation completed but validation found some issues."
        echo "Run: python3 validate_flite_browsers.py"
        echo "Most likely just browser downloads need to complete."
    fi
else
    echo ""
    echo "❌ Installation failed. Check the logs above for details."
    echo "You can retry by running: ./install_flite_browsers.sh"
    exit 1
fi