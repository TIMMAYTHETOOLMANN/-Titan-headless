#!/bin/bash
"""
Virtual Environment Setup Script for StreamBoost
Addresses issue #2: No virtual environment isolation
"""

set -e

echo "🔧 Setting up virtual environment for StreamBoost..."

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📋 Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright browser
echo "🌐 Installing Playwright Chromium browser..."
playwright install chromium

echo "✅ Virtual environment setup complete!"
echo ""
echo "To use the virtual environment:"
echo "  source venv/bin/activate"
echo ""
echo "To run StreamBoost in headless mode:"
echo "  xvfb-run -a python3 streamboost.py"
echo ""
echo "To deactivate the virtual environment:"
echo "  deactivate"