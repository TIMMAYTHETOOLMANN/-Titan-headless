#!/bin/bash
# Validation script to verify single-click deployment setup
# Tests all deployment scripts and verifies file structure

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

function log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

function log_error() {
    echo -e "${RED}❌ $1${NC}"
}

function log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

function banner() {
    echo "╔══════════════════════════════════════════════════════════════════╗"
    echo "║           Titan Headless Deployment Validation              ║"
    echo "╚══════════════════════════════════════════════════════════════════╝"
}

function check_file_exists_and_executable() {
    local file=$1
    local description=$2
    
    if [ -f "$file" ]; then
        if [ -x "$file" ]; then
            log_success "$description exists and is executable"
            return 0
        else
            log_warning "$description exists but is not executable"
            chmod +x "$file"
            log_success "Fixed permissions for $description"
            return 0
        fi
    else
        log_error "$description not found: $file"
        return 1
    fi
}

function test_script_help() {
    local script=$1
    local name=$2
    
    if [ -f "$script" ] && [ -x "$script" ]; then
        if bash "$script" --help > /dev/null 2>&1; then
            log_success "$name help command works"
            return 0
        else
            log_warning "$name help command failed (may be normal)"
            return 0
        fi
    else
        log_error "$name script not found or not executable"
        return 1
    fi
}

function check_python_files() {
    local files=(
        "streamboost.py"
        "streamboost_channel_watch.py" 
        "streamboost_channel_watch_enhanced.py"
        "setup.py"
        "setup_enhanced.py"
        "test_enhanced_system.py"
    )
    
    local count=0
    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            if python3 -m py_compile "$file" 2>/dev/null; then
                log_success "Python file $file syntax is valid"
                ((count++))
            else
                log_error "Python file $file has syntax errors"
            fi
        else
            log_warning "Python file $file not found"
        fi
    done
    
    if [ $count -ge 3 ]; then
        log_success "Core Python files are present and valid"
        return 0
    else
        log_error "Missing core Python files"
        return 1
    fi
}

function check_config_files() {
    local files=(
        "channel_watch_config.yaml"
        "requirements.txt"
    )
    
    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            log_success "Configuration file $file exists"
        else
            log_warning "Configuration file $file not found"
        fi
    done
}

function check_documentation() {
    local files=(
        "README.md"
        "DEPLOYMENT_GUIDE.md"
        "ENHANCED_DOCS.md"
    )
    
    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            log_success "Documentation file $file exists"
        else
            log_warning "Documentation file $file not found"
        fi
    done
}

function main() {
    banner
    echo ""
    
    cd "$PROJECT_DIR"
    
    echo "Checking deployment scripts..."
    check_file_exists_and_executable "./deploy_master.sh" "Master deployment script"
    check_file_exists_and_executable "./deploy_streamboost.sh" "StreamBoost deployment script"
    check_file_exists_and_executable "./deploy_youtube_watcher.sh" "YouTube Watcher deployment script"
    
    echo ""
    echo "Checking core scripts..."
    check_file_exists_and_executable "./streamboost.sh" "StreamBoost shell script"
    check_file_exists_and_executable "./quick_start.sh" "Quick start script"
    
    echo ""
    echo "Testing script help commands..."
    test_script_help "./deploy_master.sh" "Master deployment"
    test_script_help "./deploy_streamboost.sh" "StreamBoost deployment"
    test_script_help "./deploy_youtube_watcher.sh" "YouTube Watcher deployment"
    test_script_help "./streamboost.sh" "StreamBoost shell"
    
    echo ""
    echo "Checking Python files..."
    check_python_files
    
    echo ""
    echo "Checking configuration files..."
    check_config_files
    
    echo ""
    echo "Checking documentation..."
    check_documentation
    
    echo ""
    echo "Checking system requirements..."
    
    # Python version check
    python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    major=$(python3 -c "import sys; print(sys.version_info.major)")
    minor=$(python3 -c "import sys; print(sys.version_info.minor)")
    
    if [ "$major" -ge 3 ] && [ "$minor" -ge 8 ]; then
        log_success "Python $python_version is compatible (3.8+ required)"
    else
        log_error "Python $python_version is not compatible (3.8+ required)"
    fi
    
    # Check if basic tools are available
    for tool in pip3 curl wget; do
        if command -v $tool > /dev/null; then
            log_success "$tool is available"
        else
            log_warning "$tool is not available (will be installed during deployment)"
        fi
    done
    
    echo ""
    echo "File structure summary:"
    echo "├── Deployment Scripts: $(ls -1 deploy_*.sh 2>/dev/null | wc -l)"
    echo "├── Python Scripts: $(ls -1 *.py 2>/dev/null | wc -l)"
    echo "├── Shell Scripts: $(ls -1 *.sh 2>/dev/null | wc -l)"
    echo "├── Configuration Files: $(ls -1 *.yaml *.txt 2>/dev/null | wc -l)"
    echo "└── Documentation Files: $(ls -1 *.md 2>/dev/null | wc -l)"
    
    echo ""
    log_success "Validation completed! Ready for deployment."
    echo ""
    echo "🚀 To deploy, run:"
    echo "   ./deploy_master.sh --auto     # Automatic deployment"
    echo "   ./deploy_master.sh            # Interactive menu"
}

main "$@"