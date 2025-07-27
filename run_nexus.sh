#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║               Launching Nexus Maximus v2.0                      ║"
echo "╚══════════════════════════════════════════════════════════════════╝"

# Activate virtual environment
if [ -f ".nexusvenv/bin/activate" ]; then
    source .nexusvenv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found. Run enhance.sh first."
    exit 1
fi

# Check configuration
if [ ! -f "nexus_config.yaml" ]; then
    echo "❌ Configuration file not found. Run enhance.sh first."
    exit 1
fi

# Setup virtual display for headless operation
if [ -z "$DISPLAY" ] && command -v Xvfb &> /dev/null; then
    echo "🖥️  Setting up virtual display..."
    export DISPLAY=:99
    Xvfb :99 -screen 0 1920x1080x24 &
    XVFB_PID=$!
    sleep 2
    echo "✅ Virtual display ready"
fi

# Launch Nexus Maximus
echo "🚀 Starting Nexus Maximus..."
python3 nexus_maximus.py

# Cleanup
if [ ! -z "$XVFB_PID" ]; then
    kill $XVFB_PID 2>/dev/null
    echo "✅ Virtual display cleaned up"
fi

echo "✅ Nexus Maximus session completed"