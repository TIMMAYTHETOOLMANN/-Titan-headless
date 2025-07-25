#!/bin/bash
# Single-Click StreamBoost Deployment for Ubuntu 22.04+
# Automatically creates virtual environment, installs dependencies, and launches streamboost

set -e  # Exit on any error

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv_streamboost"
LOG_FILE="$PROJECT_DIR/streamboost_deployment.log"

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
║                 StreamBoost Single-Click Deploy                 ║
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
    
    # Check if running in GUI session or headless mode
    if [ -z "$DISPLAY" ]; then
        log_warning "No display found. StreamBoost will run in headless mode with virtual display."
        # Install Xvfb for virtual display if not present
        if ! command -v Xvfb &> /dev/null; then
            log "Installing Xvfb for virtual display support..."
            sudo apt install -y xvfb
        fi
    else
        log "Display found: $DISPLAY"
        # Check for X11/Xorg only if DISPLAY is set
        if ! pgrep -x "Xorg" >/dev/null && ! pgrep -x "Xwayland" >/dev/null; then
            log_warning "No X11/Xorg session detected, but DISPLAY is set. Will attempt to use virtual display."
        fi
    fi
    
    log "✅ System requirements check passed"
}

function install_system_dependencies() {
    log "Installing system dependencies..."
    
    # Update package list
    sudo apt update
    
    # Install required packages
    sudo apt install -y \
        python3 \
        python3-pip \
        python3-venv \
        chromium-browser \
        firefox \
        curl \
        wget \
        ca-certificates \
        gnupg \
        lsb-release \
        xvfb
    
    # Install additional browsers if needed
    if ! command -v chromium-browser &> /dev/null && ! command -v chromium &> /dev/null; then
        sudo apt install -y chromium
    fi
    
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
    pip install --upgrade pip
    
    log "✅ Virtual environment created and activated"
}

function install_python_dependencies() {
    log "Installing Python dependencies..."
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Install requirements if file exists
    if [ -f "$PROJECT_DIR/requirements.txt" ]; then
        pip install -r "$PROJECT_DIR/requirements.txt"
    fi
    
    # Install playwright and browsers
    pip install playwright playwright-stealth
    playwright install chromium
    
    log "✅ Python dependencies installed"
}

function prepare_streamboost() {
    log "Preparing StreamBoost configuration..."
    
    # Make streamboost.sh executable
    chmod +x "$PROJECT_DIR/streamboost.sh"
    
    # Create profile directories
    mkdir -p "/tmp/streamboost_profiles"
    
    # Clean up any existing browser processes
    pkill -f "remote-debugging-port" 2>/dev/null || true
    sleep 2
    
    log "✅ StreamBoost prepared"
}

function launch_streamboost() {
    log "Launching StreamBoost..."
    
    # Change to project directory
    cd "$PROJECT_DIR"
    
    # Launch streamboost.sh
    bash streamboost.sh
    
    log "✅ StreamBoost launched successfully!"
}

function create_launcher_script() {
    log "Creating launcher script for future use..."
    
    cat > "$PROJECT_DIR/launch_streamboost.sh" << 'EOF'
#!/bin/bash
# Quick launcher for StreamBoost (after initial deployment)

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv_streamboost"

echo "🚀 Launching StreamBoost..."

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "❌ Virtual environment not found. Please run deploy_streamboost.sh first."
    exit 1
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Change to project directory
cd "$PROJECT_DIR"

# Launch streamboost
bash streamboost.sh

echo "✅ StreamBoost session completed."
EOF

    chmod +x "$PROJECT_DIR/launch_streamboost.sh"
    log "✅ Launcher script created: launch_streamboost.sh"
}

function main() {
    banner
    
    log "Starting StreamBoost single-click deployment..."
    log "Project directory: $PROJECT_DIR"
    log "Virtual environment: $VENV_DIR"
    
    check_system
    install_system_dependencies
    create_virtual_environment
    install_python_dependencies
    prepare_streamboost
    create_launcher_script
    
    log "🎉 StreamBoost deployment completed successfully!"
    log ""
    log "To launch StreamBoost now:"
    log "  bash streamboost.sh"
    log ""
    log "For future launches, use:"
    log "  ./launch_streamboost.sh"
    log ""
    
    # Ask user if they want to launch now
    echo -n "Launch StreamBoost now? (y/n): "
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        launch_streamboost
    else
        log "StreamBoost ready to launch when needed."
    fi
}

# Show help if requested
if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
    echo "StreamBoost Single-Click Deployment Script"
    echo ""
    echo "This script will:"
    echo "  1. Check system requirements (Ubuntu 22.04+, supports headless)"
    echo "  2. Install system dependencies (browsers, Python packages, Xvfb)"
    echo "  3. Create isolated virtual environment"
    echo "  4. Install Python dependencies"
    echo "  5. Configure and launch StreamBoost (headless or GUI)"
    echo ""
    echo "Usage:"
    echo "  ./deploy_streamboost.sh     # Full deployment and launch"
    echo "  ./deploy_streamboost.sh -h  # Show this help"
    echo ""
    echo "After deployment, use:"
    echo "  ./launch_streamboost.sh     # Quick launch for future use"
    exit 0
fi

# Run main function
main "$@"