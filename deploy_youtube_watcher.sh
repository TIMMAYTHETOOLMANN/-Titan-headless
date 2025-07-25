#!/bin/bash
# Single-Click YouTube Watcher Deployment for Ubuntu 22.04+
# Automatically creates virtual environment, installs dependencies, and launches YouTube watcher

set -e  # Exit on any error

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv_youtube_watcher"
LOG_FILE="$PROJECT_DIR/youtube_watcher_deployment.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

function log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a "$LOG_FILE"
}

function log_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}" | tee -a "$LOG_FILE"
}

function log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}" | tee -a "$LOG_FILE"
}

function banner() {
    echo -e "${BLUE}"
    cat << 'EOF'
╔══════════════════════════════════════════════════════════════════╗
║              YouTube Watcher Single-Click Deploy               ║
║                 Enhanced Channel Watch Monolith                ║
║                    Ubuntu 22.04+ Optimized                     ║
╚══════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

function check_system() {
    log "Checking system requirements..."
    
    # Check Ubuntu version
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        if [[ "$VERSION_ID" < "22.04" ]]; then
            log_warning "Ubuntu version $VERSION_ID detected. This script is optimized for 22.04+"
        else
            log "Ubuntu $VERSION_ID detected - compatible!"
        fi
    fi
    
    # Check Python version
    python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    log "Python version: $python_version"
    
    # Simple version check without bc dependency
    major=$(python3 -c "import sys; print(sys.version_info.major)")
    minor=$(python3 -c "import sys; print(sys.version_info.minor)")
    
    if [ "$major" -lt 3 ] || ([ "$major" -eq 3 ] && [ "$minor" -lt 8 ]); then
        log_error "Python 3.8+ is required"
        exit 1
    fi
    
    log "✅ System requirements check passed"
}

function install_system_dependencies() {
    log "Installing system dependencies..."
    
    # Update package list
    sudo apt update
    
    # Install required packages for Ubuntu 22.04+
    sudo apt install -y \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        build-essential \
        chromium-browser \
        firefox \
        curl \
        wget \
        ca-certificates \
        gnupg \
        lsb-release \
        libnss3-dev \
        libatk-bridge2.0-dev \
        libdrm2 \
        libxcomposite1 \
        libxdamage1 \
        libxrandr2 \
        libgbm1 \
        libxss1 \
        libasound2
    
    # Install additional dependencies for Playwright
    sudo apt install -y \
        fonts-liberation \
        libappindicator3-1 \
        libasound2 \
        libatk-bridge2.0-0 \
        libatspi2.0-0 \
        libdrm2 \
        libgtk-3-0 \
        libnspr4 \
        libnss3 \
        libx11-xcb1 \
        libxcomposite1 \
        libxdamage1 \
        libxrandr2 \
        xdg-utils
    
    log "✅ System dependencies installed"
}

function create_virtual_environment() {
    log "Creating virtual environment..."
    
    # Remove existing venv if it exists
    if [ -d "$VENV_DIR" ]; then
        log "Removing existing virtual environment..."
        rm -rf "$VENV_DIR"
    fi
    
    # Create new virtual environment
    python3 -m venv "$VENV_DIR"
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Upgrade pip
    pip install --upgrade pip setuptools wheel
    
    log "✅ Virtual environment created and activated"
}

function install_python_dependencies() {
    log "Installing Python dependencies..."
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Install requirements from file
    if [ -f "$PROJECT_DIR/requirements.txt" ]; then
        pip install -r "$PROJECT_DIR/requirements.txt"
    else
        # Install core dependencies manually
        pip install \
            playwright>=1.40.0 \
            playwright-stealth>=1.0.6 \
            psutil>=5.9.0 \
            py-cpuinfo>=9.0.0 \
            requests>=2.31.0 \
            beautifulsoup4>=4.12.0 \
            pyyaml>=6.0 \
            aiofiles>=23.2.0
    fi
    
    # Install Playwright browsers
    log "Installing Playwright browsers..."
    playwright install chromium
    playwright install-deps chromium
    
    log "✅ Python dependencies installed"
}

function prepare_youtube_watcher() {
    log "Preparing YouTube Watcher configuration..."
    
    # Create necessary directories
    mkdir -p "$PROJECT_DIR/profiles"
    mkdir -p "$PROJECT_DIR/logs"
    
    # Set proper permissions
    chmod 755 "$PROJECT_DIR/profiles"
    chmod 755 "$PROJECT_DIR/logs"
    
    # Ensure config file exists
    if [ ! -f "$PROJECT_DIR/channel_watch_config.yaml" ]; then
        log "Creating default configuration file..."
        cat > "$PROJECT_DIR/channel_watch_config.yaml" << 'EOF'
base_port: 9333
channel_url: https://www.youtube.com/@TimmayTheToolMan
cpu_threshold: 85
engagement_rate: 0.3
log_level: INFO
max_video_duration: 3600
max_videos: 25
min_video_duration: 60
profile_base: ./profiles
proxy_list: []
ram_threshold: 85
rotate_video_every:
- 180
- 320
statistics_enabled: true
windows: 27
EOF
    fi
    
    # Make Python scripts executable
    chmod +x "$PROJECT_DIR/streamboost_channel_watch_enhanced.py"
    chmod +x "$PROJECT_DIR/setup_enhanced.py"
    
    log "✅ YouTube Watcher prepared"
}

function test_installation() {
    log "Testing installation..."
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Change to project directory
    cd "$PROJECT_DIR"
    
    # Run system test if available
    if [ -f "$PROJECT_DIR/test_enhanced_system.py" ]; then
        python3 test_enhanced_system.py
    else
        # Basic import test
        python3 -c "
import asyncio
import playwright
import yaml
print('✅ All required modules can be imported')
"
    fi
    
    log "✅ Installation test passed"
}

function launch_youtube_watcher() {
    log "Launching YouTube Watcher..."
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Change to project directory
    cd "$PROJECT_DIR"
    
    # Launch enhanced channel watch
    python3 streamboost_channel_watch_enhanced.py
    
    log "✅ YouTube Watcher launched successfully!"
}

function create_launcher_script() {
    log "Creating launcher script for future use..."
    
    cat > "$PROJECT_DIR/launch_youtube_watcher.sh" << 'EOF'
#!/bin/bash
# Quick launcher for YouTube Watcher (after initial deployment)

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv_youtube_watcher"

echo "🎥 Launching YouTube Watcher..."

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "❌ Virtual environment not found. Please run deploy_youtube_watcher.sh first."
    exit 1
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Change to project directory
cd "$PROJECT_DIR"

# Launch YouTube watcher
python3 streamboost_channel_watch_enhanced.py

echo "✅ YouTube Watcher session completed."
EOF

    chmod +x "$PROJECT_DIR/launch_youtube_watcher.sh"
    log "✅ Launcher script created: launch_youtube_watcher.sh"
}

function show_configuration_help() {
    log "Configuration options:"
    log ""
    log "Edit channel_watch_config.yaml to customize:"
    log "  - channel_url: Target YouTube channel"
    log "  - windows: Number of browser windows"
    log "  - engagement_rate: Rate of video interactions"
    log "  - cpu_threshold: CPU usage limit"
    log "  - ram_threshold: RAM usage limit"
    log ""
}

function main() {
    banner
    
    log "Starting YouTube Watcher single-click deployment..."
    log "Project directory: $PROJECT_DIR"
    log "Virtual environment: $VENV_DIR"
    
    check_system
    install_system_dependencies
    create_virtual_environment
    install_python_dependencies
    prepare_youtube_watcher
    test_installation
    create_launcher_script
    
    log "🎉 YouTube Watcher deployment completed successfully!"
    log ""
    show_configuration_help
    log ""
    log "To launch YouTube Watcher now:"
    log "  python3 streamboost_channel_watch_enhanced.py"
    log ""
    log "For future launches, use:"
    log "  ./launch_youtube_watcher.sh"
    log ""
    
    # Ask user if they want to edit config
    echo -n "Edit configuration before launching? (y/n): "
    read -r config_response
    if [[ "$config_response" =~ ^[Yy]$ ]]; then
        if command -v nano &> /dev/null; then
            nano "$PROJECT_DIR/channel_watch_config.yaml"
        elif command -v vi &> /dev/null; then
            vi "$PROJECT_DIR/channel_watch_config.yaml"
        else
            log "Please edit channel_watch_config.yaml manually"
        fi
    fi
    
    # Ask user if they want to launch now
    echo -n "Launch YouTube Watcher now? (y/n): "
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        launch_youtube_watcher
    else
        log "YouTube Watcher ready to launch when needed."
    fi
}

# Show help if requested
if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
    echo "YouTube Watcher Single-Click Deployment Script"
    echo ""
    echo "This script will:"
    echo "  1. Check system requirements (Ubuntu 22.04+, Python 3.8+)"
    echo "  2. Install system dependencies (browsers, Python packages)"
    echo "  3. Create isolated virtual environment"
    echo "  4. Install Python dependencies and Playwright browsers"
    echo "  5. Configure and test YouTube Watcher"
    echo "  6. Create launcher script for future use"
    echo ""
    echo "Usage:"
    echo "  ./deploy_youtube_watcher.sh     # Full deployment and launch"
    echo "  ./deploy_youtube_watcher.sh -h  # Show this help"
    echo ""
    echo "After deployment, use:"
    echo "  ./launch_youtube_watcher.sh     # Quick launch for future use"
    exit 0
fi

# Run main function
main "$@"