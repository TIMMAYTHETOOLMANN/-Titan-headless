#!/bin/bash
# Titan Headless - Live Stream Deployment Launcher
# Quick launcher for live stream deployment mode

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                    Titan Headless Live Stream                       ║"
echo "║                      Deployment Launcher                            ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ to continue."
    exit 1
fi

# Check if config file exists, create if not
if [ ! -f "deployment_config.yaml" ]; then
    echo "📝 No configuration file found. Creating default configuration..."
    python3 titan_deployment.py --create-configs
    
    # Set default to live stream mode
    sed -i 's/deployment_mode: .*/deployment_mode: "live_stream"/' deployment_config.yaml
    echo "✅ Configuration file created: deployment_config.yaml"
    echo "📝 You can edit this file to customize your deployment settings."
    echo ""
fi

# Validate configuration
echo "🔍 Validating configuration..."
if ! python3 titan_deployment.py --mode live_stream --validate-only; then
    echo "❌ Configuration validation failed. Please check your configuration file."
    exit 1
fi

echo "✅ Configuration is valid"
echo ""

# Show configuration summary
echo "📊 Live Stream Deployment Configuration:"
echo "   Target Account: $(grep 'target_account:' deployment_config.yaml | awk '{print $2}' | tr -d '"')"
echo "   Base Port: $(grep 'base_port:' deployment_config.yaml | awk '{print $2}')"
echo "   Profile Directory: $(grep 'profile_base:' deployment_config.yaml | awk '{print $2}' | tr -d '"')"
echo ""

# Check system resources
echo "🖥️  System Resources:"
echo "   CPU Usage: $(python3 -c "import psutil; print(f'{psutil.cpu_percent():.1f}%')")"
echo "   RAM Usage: $(python3 -c "import psutil; print(f'{psutil.virtual_memory().percent:.1f}%')")"
echo ""

# Ask for confirmation
read -p "🚀 Start live stream deployment? [Y/n]: " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo "Deployment cancelled."
    exit 0
fi

# Create necessary directories
mkdir -p profiles logs

# Start deployment
echo "🎮 Starting live stream deployment..."
echo "💡 Tip: Press Ctrl+C to stop all windows"
echo ""

python3 titan_deployment.py --mode live_stream

echo ""
echo "✅ Live stream deployment completed."