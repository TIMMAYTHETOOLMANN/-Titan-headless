#!/bin/bash
# Quick Start Script for Enhanced Channel Watch Monolith

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║         Enhanced Channel Watch Monolith - Quick Start           ║"
echo "╚══════════════════════════════════════════════════════════════════╝"

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "🐍 Python version: $python_version"

if [ "$(echo "$python_version >= 3.8" | bc)" -eq 0 ]; then
    echo "❌ Python 3.8+ is required"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install chromium

# Create directories
echo "📁 Creating directory structure..."
mkdir -p profiles logs

# Test the system
echo "🧪 Running system tests..."
python3 test_enhanced_system.py

# Ask user if they want to edit config
echo ""
echo "⚙️  Do you want to edit the configuration file? (y/n)"
read -r edit_config
if [ "$edit_config" = "y" ]; then
    if command -v nano &> /dev/null; then
        nano channel_watch_config.yaml
    elif command -v vi &> /dev/null; then
        vi channel_watch_config.yaml
    else
        echo "Please edit channel_watch_config.yaml manually"
    fi
fi

echo ""
echo "✅ Setup complete! Ready to run:"
echo "   python3 streamboost_channel_watch_enhanced.py"
echo ""
echo "📖 For detailed documentation, see ENHANCED_DOCS.md"