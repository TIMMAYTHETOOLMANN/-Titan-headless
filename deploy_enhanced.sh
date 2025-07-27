#!/bin/bash
# Enhanced Nexus Deployment Script
echo "🚀 Deploying Enhanced Nexus with JARVIS Protocol..."

# Install enhanced requirements
pip install -r requirements_enhanced.txt

# Install Playwright browsers
python -m playwright install chromium

# Setup enhanced configuration
if [ ! -f "enhanced_nexus_config.yaml" ]; then
    echo "⚠️  Enhanced config not found, using default..."
    cp nexus_config.yaml enhanced_nexus_config.yaml 2>/dev/null || echo "Creating minimal config..."
fi

# Run enhanced system
echo "✅ Starting Enhanced Nexus..."
python3 streamboost_enhanced.py

echo "🎯 Enhanced Nexus deployment complete!"
