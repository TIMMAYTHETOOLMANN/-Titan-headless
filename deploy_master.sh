#!/bin/bash
# Master Single-Click Deployment for Titan Headless
# Deploys both StreamBoost and YouTube Watcher with one command
# Optimized for Ubuntu 22.04+

set -e  # Exit on any error

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$PROJECT_DIR/master_deployment.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
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

function log_info() {
    echo -e "${CYAN}[$(date '+%Y-%m-%d %H:%M:%S')] INFO: $1${NC}" | tee -a "$LOG_FILE"
}

function banner() {
    echo -e "${PURPLE}"
    cat << 'EOF'
╔══════════════════════════════════════════════════════════════════╗
║                  TITAN HEADLESS MASTER DEPLOY                   ║
║                                                                  ║
║              🚀 StreamBoost + YouTube Watcher 🎥                ║
║                     Single-Click Deployment                     ║
║                      Ubuntu 22.04+ Ready                       ║
╚══════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

function show_menu() {
    echo -e "${BLUE}Select deployment option:${NC}"
    echo "1) Deploy StreamBoost only"
    echo "2) Deploy YouTube Watcher only"  
    echo "3) Deploy both programs (recommended)"
    echo "4) Quick launch existing installations"
    echo "5) Show system information"
    echo "6) Exit"
    echo ""
    echo -n "Enter your choice (1-6): "
}

function show_system_info() {
    log_info "System Information:"
    echo "===================="
    
    # OS Info
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "OS: $PRETTY_NAME"
        echo "Version: $VERSION_ID"
    fi
    
    # Python version
    python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')")
    echo "Python: $python_version"
    
    # Memory info
    memory_info=$(free -h | grep '^Mem:' | awk '{print "Total: " $2 ", Available: " $7}')
    echo "Memory: $memory_info"
    
    # CPU info
    cpu_count=$(nproc)
    echo "CPU Cores: $cpu_count"
    
    # Check GUI session
    if [ -n "$DISPLAY" ]; then
        echo "GUI Session: ✅ Available ($DISPLAY)"
    else
        echo "GUI Session: ❌ Not detected"
    fi
    
    # Check browsers
    echo -n "Browsers: "
    browsers_found=""
    command -v chromium-browser >/dev/null && browsers_found+="chromium-browser "
    command -v chromium >/dev/null && browsers_found+="chromium "
    command -v firefox >/dev/null && browsers_found+="firefox "
    
    if [ -n "$browsers_found" ]; then
        echo "✅ $browsers_found"
    else
        echo "❌ None found (will be installed)"
    fi
    
    # Check existing installations
    echo ""
    echo "Existing Installations:"
    if [ -d "$PROJECT_DIR/venv_streamboost" ]; then
        echo "  StreamBoost: ✅ Installed"
    else
        echo "  StreamBoost: ❌ Not installed"
    fi
    
    if [ -d "$PROJECT_DIR/venv_youtube_watcher" ]; then
        echo "  YouTube Watcher: ✅ Installed"
    else
        echo "  YouTube Watcher: ❌ Not installed"
    fi
    
    echo ""
}

function deploy_streamboost() {
    log "Deploying StreamBoost..."
    
    if [ ! -f "$PROJECT_DIR/deploy_streamboost.sh" ]; then
        log_error "StreamBoost deployment script not found!"
        return 1
    fi
    
    chmod +x "$PROJECT_DIR/deploy_streamboost.sh"
    bash "$PROJECT_DIR/deploy_streamboost.sh"
    
    log "✅ StreamBoost deployment completed"
}

function deploy_youtube_watcher() {
    log "Deploying YouTube Watcher..."
    
    if [ ! -f "$PROJECT_DIR/deploy_youtube_watcher.sh" ]; then
        log_error "YouTube Watcher deployment script not found!"
        return 1
    fi
    
    chmod +x "$PROJECT_DIR/deploy_youtube_watcher.sh"
    bash "$PROJECT_DIR/deploy_youtube_watcher.sh"
    
    log "✅ YouTube Watcher deployment completed"
}

function deploy_both() {
    log "Deploying both StreamBoost and YouTube Watcher..."
    
    # Deploy StreamBoost first
    deploy_streamboost
    
    echo ""
    log_info "StreamBoost deployment completed. Starting YouTube Watcher deployment..."
    echo ""
    
    # Deploy YouTube Watcher
    deploy_youtube_watcher
    
    log "🎉 Both programs deployed successfully!"
    create_master_launchers
}

function create_master_launchers() {
    log "Creating master launcher scripts..."
    
    # Create quick launcher for both programs
    cat > "$PROJECT_DIR/launch_both.sh" << 'EOF'
#!/bin/bash
# Quick launcher for both StreamBoost and YouTube Watcher

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Launching Titan Headless Suite..."

# Launch StreamBoost in background
if [ -f "$PROJECT_DIR/launch_streamboost.sh" ]; then
    echo "Starting StreamBoost..."
    nohup bash "$PROJECT_DIR/launch_streamboost.sh" > /dev/null 2>&1 &
    STREAMBOOST_PID=$!
    echo "StreamBoost started (PID: $STREAMBOOST_PID)"
else
    echo "❌ StreamBoost launcher not found. Run deploy_master.sh first."
fi

# Wait a moment then launch YouTube Watcher
sleep 5

if [ -f "$PROJECT_DIR/launch_youtube_watcher.sh" ]; then
    echo "Starting YouTube Watcher..."
    bash "$PROJECT_DIR/launch_youtube_watcher.sh"
else
    echo "❌ YouTube Watcher launcher not found. Run deploy_master.sh first."
fi

echo "✅ Titan Headless Suite session completed."
EOF

    chmod +x "$PROJECT_DIR/launch_both.sh"
    
    # Create stop script
    cat > "$PROJECT_DIR/stop_all.sh" << 'EOF'
#!/bin/bash
# Stop all Titan Headless processes

echo "🛑 Stopping all Titan Headless processes..."

# Stop browser processes
pkill -f "streamboost" 2>/dev/null || true
pkill -f "remote-debugging-port" 2>/dev/null || true
pkill -f "channel_watch" 2>/dev/null || true

# Stop Python processes
pkill -f "streamboost_channel_watch_enhanced.py" 2>/dev/null || true
pkill -f "streamboost.py" 2>/dev/null || true

echo "✅ All processes stopped."
EOF

    chmod +x "$PROJECT_DIR/stop_all.sh"
    
    log "✅ Master launcher scripts created"
}

function quick_launch() {
    echo -e "${BLUE}Quick Launch Menu:${NC}"
    echo "1) Launch StreamBoost"
    echo "2) Launch YouTube Watcher"
    echo "3) Launch both programs"
    echo "4) Stop all programs"
    echo "5) Back to main menu"
    echo ""
    echo -n "Enter your choice (1-5): "
    
    read -r launch_choice
    case $launch_choice in
        1)
            if [ -f "$PROJECT_DIR/launch_streamboost.sh" ]; then
                bash "$PROJECT_DIR/launch_streamboost.sh"
            else
                log_error "StreamBoost not installed. Please deploy first."
            fi
            ;;
        2)
            if [ -f "$PROJECT_DIR/launch_youtube_watcher.sh" ]; then
                bash "$PROJECT_DIR/launch_youtube_watcher.sh"
            else
                log_error "YouTube Watcher not installed. Please deploy first."
            fi
            ;;
        3)
            if [ -f "$PROJECT_DIR/launch_both.sh" ]; then
                bash "$PROJECT_DIR/launch_both.sh"
            else
                log_error "Programs not installed. Please deploy first."
            fi
            ;;
        4)
            if [ -f "$PROJECT_DIR/stop_all.sh" ]; then
                bash "$PROJECT_DIR/stop_all.sh"
            else
                log_info "No stop script found. Attempting manual cleanup..."
                pkill -f "streamboost" 2>/dev/null || true
                pkill -f "remote-debugging-port" 2>/dev/null || true
                log "Cleanup completed."
            fi
            ;;
        5)
            return
            ;;
        *)
            log_error "Invalid choice!"
            ;;
    esac
}

function main() {
    banner
    
    log "Titan Headless Master Deployment System"
    log "Project directory: $PROJECT_DIR"
    log "Log file: $LOG_FILE"
    
    while true; do
        echo ""
        show_menu
        read -r choice
        
        case $choice in
            1)
                deploy_streamboost
                ;;
            2)
                deploy_youtube_watcher
                ;;
            3)
                deploy_both
                ;;
            4)
                quick_launch
                ;;
            5)
                show_system_info
                ;;
            6)
                log "Exiting Titan Headless Master Deploy"
                exit 0
                ;;
            *)
                log_error "Invalid choice! Please select 1-6."
                ;;
        esac
        
        echo ""
        echo "Press Enter to continue..."
        read -r
    done
}

# Show help if requested
if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
    cat << 'EOF'
Titan Headless Master Deployment Script

This script provides a unified interface to deploy and manage:
  1. StreamBoost - Multi-platform stream boosting
  2. YouTube Watcher - Enhanced channel view simulation

Features:
  ✅ Automatic virtual environment creation
  ✅ System dependency installation
  ✅ Ubuntu 22.04+ optimization
  ✅ Single-click deployment
  ✅ Quick launch capabilities
  ✅ System monitoring and cleanup

Usage:
  ./deploy_master.sh         # Interactive menu
  ./deploy_master.sh -h      # Show this help

After deployment, use:
  ./launch_streamboost.sh    # Launch StreamBoost only
  ./launch_youtube_watcher.sh # Launch YouTube Watcher only
  ./launch_both.sh           # Launch both programs
  ./stop_all.sh              # Stop all programs

System Requirements:
  - Ubuntu 22.04+ (recommended)
  - Python 3.8+
  - 4GB+ RAM recommended
  - GUI session (X11/Wayland)
  - Internet connection
EOF
    exit 0
fi

# Auto-deploy mode
if [[ "$1" == "--auto" ]] || [[ "$1" == "--deploy-all" ]]; then
    banner
    log "Running automatic deployment of both programs..."
    deploy_both
    exit 0
fi

# Run main interactive menu
main "$@"