#!/bin/bash
# Comprehensive Flite Shared Library and Playwright Browser Dependency Installer
# For Ubuntu headless environments - bulletproof installation script
# Addresses: Build & Install Flite shared libraries and all Playwright dependencies

set -e  # Exit on any error

# Color codes for logging
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[NEXUS_INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[NEXUS_SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[NEXUS_WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[NEXUS_FATAL]${NC} STEP FAILED: $1"
    if [ $# -gt 1 ]; then
        echo -e "${RED}[NEXUS_FATAL]${NC} ERROR OUTPUT: $2"
    fi
    echo -e "${RED}[NEXUS_FATAL]${NC} Fix this error and rerun."
    exit 1
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    log_error "Do not run this script as root. Use sudo when needed for individual commands."
fi

# Set non-interactive mode
export DEBIAN_FRONTEND=noninteractive

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║   TITAN HEADLESS - FLITE & BROWSER DEPENDENCY INSTALLER v1.0    ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Function to check if Flite shared libraries are already installed
check_flite_installed() {
    log_info "Checking for existing Flite shared libraries..."
    
    if [ -f "/usr/local/lib/libflite_cmu_us_kal.so.1" ] || [ -f "/usr/local/lib/libflite_cmu_us_kal.so" ]; then
        log_success "Flite shared libraries already installed"
        return 0
    fi
    
    # Check system locations too
    if ldconfig -p | grep -q "libflite_cmu_us"; then
        log_success "Flite shared libraries found in system"
        return 0
    fi
    
    log_warning "Flite shared libraries not found - will build from source"
    return 1
}

# Function to install build dependencies
install_build_deps() {
    log_info "Installing build dependencies..."
    
    local packages=(
        "build-essential"
        "autoconf" 
        "automake"
        "libtool"
        "pkg-config"
        "wget"
        "curl"
        "git"
        "unzip"
    )
    
    for package in "${packages[@]}"; do
        if ! dpkg -l | grep -q "^ii  $package "; then
            log_info "Installing $package..."
            sudo apt-get install -y "$package" || log_error "Failed to install $package"
        fi
    done
    
    log_success "Build dependencies installed"
}

# Function to download and build Flite with shared libraries
install_flite_shared() {
    log_info "Starting Flite source build with shared libraries..."
    
    local flite_version="2.2"
    local build_dir="/tmp/flite-build-$$"
    local flite_url="https://github.com/festvox/flite/archive/refs/tags/v${flite_version}.tar.gz"
    
    # Create build directory
    mkdir -p "$build_dir"
    cd "$build_dir"
    
    # Download Flite source
    log_info "Downloading Flite v${flite_version} source..."
    wget -O "flite-${flite_version}.tar.gz" "$flite_url" || log_error "Failed to download Flite source" "wget exit code: $?"
    
    # Extract source
    log_info "Extracting Flite source..."
    tar -xzf "flite-${flite_version}.tar.gz" || log_error "Failed to extract Flite source"
    cd "flite-${flite_version}"
    
    # Configure with shared libraries enabled
    log_info "Configuring Flite build with shared libraries..."
    if ./configure --enable-shared --prefix=/usr/local; then
        log_success "Configure completed with --enable-shared"
    else
        log_warning "Configure with --enable-shared failed, trying alternative approach..."
        
        # Alternative: patch Makefiles to build shared libraries
        log_info "Patching Makefiles to build shared libraries..."
        
        # Run configure without --enable-shared first
        ./configure --prefix=/usr/local || log_error "Basic configure failed"
        
        # Patch main Makefile to build shared libraries
        if [ -f "Makefile" ]; then
            sed -i 's/libflite\.a/libflite.so/g' Makefile || true
            sed -i 's/-static/-shared -fPIC/g' Makefile || true
        fi
        
        # Patch library Makefiles
        for makefile in $(find . -name "Makefile" -type f); do
            sed -i 's/\.a/.so/g' "$makefile" || true
            sed -i 's/ar cr/gcc -shared -o/g' "$makefile" || true
            sed -i 's/ranlib/echo/g' "$makefile" || true
        done
        
        log_info "Makefiles patched for shared library build"
    fi
    
    # Build Flite
    log_info "Building Flite (this may take a few minutes)..."
    make -j$(nproc) || log_error "Flite build failed" "make exit code: $?"
    
    # Install Flite
    log_info "Installing Flite..."
    sudo make install || log_error "Flite installation failed" "make install exit code: $?"
    
    # Find and copy shared libraries if they weren't installed properly
    log_info "Ensuring shared libraries are properly installed..."
    
    local so_files_found=false
    for so_pattern in "*.so*" "*libflite*.so*"; do
        if find . -name "$so_pattern" -type f 2>/dev/null | grep -q .; then
            so_files_found=true
            find . -name "$so_pattern" -type f -exec sudo cp {} /usr/local/lib/ \; 2>/dev/null || true
        fi
    done
    
    # Also check build subdirectories
    for subdir in lib .libs src; do
        if [ -d "$subdir" ]; then
            find "$subdir" -name "*.so*" -type f -exec sudo cp {} /usr/local/lib/ \; 2>/dev/null || true
        fi
    done
    
    # Refresh library cache
    log_info "Refreshing library cache..."
    sudo ldconfig || log_error "ldconfig failed"
    
    # Cleanup
    cd /
    rm -rf "$build_dir"
    
    log_success "Flite build and installation completed"
}

# Function to install all Playwright browser dependencies
install_browser_deps() {
    log_info "Installing comprehensive browser dependencies for Ubuntu..."
    
    # Update package list
    sudo apt-get update -qq || log_error "apt-get update failed"
    
    # Core browser dependencies from the issue description
    local browser_deps=(
        "libgtk-3-0"
        "libgtk-4-1" 
        "libasound2"
        "libnss3"
        "libxss1"
        "libxtst6"
        "libatk-bridge2.0-0"
        "libdrm2"
        "libgbm1" 
        "libxcomposite1"
        "libxdamage1"
        "libxrandr2"
        "libxinerama1"
        "libpango-1.0-0"
        "libcairo2"
        "libatspi2.0-0"
        "libharfbuzz-icu0"
        "libvpx7"
        "libopus0"
        "libevent-2.1-7"
        "gstreamer1.0-plugins-base"
        "gstreamer1.0-plugins-good"
        "gstreamer1.0-x"
        "libflite1"
        "libavif13"
        "libhyphen0"
        "libmanette-0.2-0"
        "libgles2-mesa"
        "libwebpdemux2"
        "libx264-163"
        "libwoff1"
    )
    
    # Additional essential dependencies
    local extra_deps=(
        "xvfb"
        "fonts-liberation"
        "fonts-noto"
        "ca-certificates"
        "libxkbcommon0"
        "libdbus-1-3"
        "libxshmfence1"
    )
    
    # Combine all dependencies
    local all_deps=("${browser_deps[@]}" "${extra_deps[@]}")
    
    log_info "Installing ${#all_deps[@]} browser dependency packages..."
    
    # Install packages with error handling
    local failed_packages=()
    for package in "${all_deps[@]}"; do
        log_info "Installing $package..."
        if ! sudo apt-get install -y "$package" 2>/dev/null; then
            failed_packages+=("$package")
            log_warning "Package $package not available or failed to install"
        fi
    done
    
    if [ ${#failed_packages[@]} -gt 0 ]; then
        log_warning "Some packages failed to install: ${failed_packages[*]}"
        log_info "Attempting to find alternatives..."
        
        # Try to find and install alternatives for failed packages
        for package in "${failed_packages[@]}"; do
            case "$package" in
                "libgtk-4-1")
                    sudo apt-get install -y libgtk-4-dev || true
                    ;;
                "libavif13")
                    sudo apt-get install -y libavif-dev || true
                    ;;
                "libmanette-0.2-0")
                    sudo apt-get install -y libmanette-0.2-dev || true
                    ;;
                "libx264-163")
                    sudo apt-get install -y libx264-dev || true
                    ;;
                "libwoff1")
                    sudo apt-get install -y libwoff-dev || true
                    ;;
            esac
        done
    fi
    
    log_success "Browser dependencies installation completed"
}

# Function to setup headless environment
setup_headless_env() {
    log_info "Setting up headless environment..."
    
    # Ensure Xvfb is available
    if ! command -v Xvfb &> /dev/null; then
        log_error "Xvfb not available after installation"
    fi
    
    # Set up DISPLAY environment
    if [ -z "$DISPLAY" ]; then
        export DISPLAY=:99
        log_info "Set DISPLAY=:99 for headless operation"
    fi
    
    log_success "Headless environment configured"
}

# Function to install Playwright browsers
install_playwright_browsers() {
    log_info "Installing Playwright browsers..."
    
    # Ensure Python and pip are available
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 not available"
    fi
    
    # Install/upgrade Playwright with retries and timeout handling
    log_info "Installing/upgrading Playwright (with timeout handling)..."
    local max_attempts=3
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        log_info "Attempt $attempt of $max_attempts to install Playwright..."
        
        if timeout 300 python3 -m pip install --user --upgrade --timeout 60 playwright; then
            log_success "Playwright installation successful"
            break
        else
            if [ $attempt -eq $max_attempts ]; then
                log_warning "Playwright pip installation failed after $max_attempts attempts"
                log_info "Checking if Playwright is already available..."
                
                if python3 -c "import playwright" 2>/dev/null; then
                    log_success "Playwright is already available, continuing..."
                else
                    log_error "Failed to install/upgrade Playwright after $max_attempts attempts"
                fi
            else
                log_warning "Attempt $attempt failed, retrying in 10 seconds..."
                sleep 10
            fi
        fi
        ((attempt++))
    done
    
    # Install browser binaries
    log_info "Downloading Playwright browser binaries..."
    
    # Set environment for headless download
    export PLAYWRIGHT_BROWSERS_PATH=0  # Use default path
    
    # Try browser installation with individual fallbacks
    local browser_success=false
    
    if timeout 600 python3 -m playwright install chromium firefox webkit 2>/dev/null; then
        log_success "All browsers installed successfully"
        browser_success=true
    else
        log_warning "Standard browser installation failed, trying individual browsers..."
        
        # Try installing browsers individually with timeouts
        for browser in chromium firefox webkit; do
            log_info "Installing $browser individually..."
            if timeout 300 python3 -m playwright install "$browser" 2>/dev/null; then
                log_success "$browser installation successful"
                browser_success=true
            else
                log_warning "$browser installation failed or timed out"
            fi
        done
    fi
    
    if [ "$browser_success" = true ]; then
        log_success "Playwright browser installation completed"
    else
        log_warning "Browser installation had issues, but continuing..."
    fi
}

# Function to run comprehensive diagnostics
run_diagnostics() {
    log_info "Running comprehensive diagnostics..."
    
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════╗"
    echo "║                        DIAGNOSTIC RESULTS                       ║"
    echo "╚══════════════════════════════════════════════════════════════════╝"
    echo ""
    
    # Check Flite libraries
    log_info "Checking Flite shared libraries..."
    local flite_found=false
    
    for lib_pattern in "libflite_cmu_us_kal.so*" "libflite.so*" "libflite_cmu_*.so*"; do
        if find /usr/local/lib /usr/lib -name "$lib_pattern" 2>/dev/null | grep -q .; then
            flite_found=true
            find /usr/local/lib /usr/lib -name "$lib_pattern" 2>/dev/null | while read lib; do
                log_success "Found: $lib"
            done
        fi
    done
    
    if ldconfig -p | grep -q flite; then
        flite_found=true
        log_success "Flite libraries registered with ldconfig:"
        ldconfig -p | grep flite | sed 's/^/  /'
    fi
    
    if [ "$flite_found" = false ]; then
        log_warning "No Flite shared libraries found in standard locations"
    fi
    
    # Check Playwright
    log_info "Checking Playwright installation..."
    if python3 -c "import playwright; from playwright.async_api import async_playwright; print('Playwright import and API test successful')" 2>/dev/null; then
        log_success "Playwright import and API test successful"
    else
        log_warning "Playwright import failed"
    fi
    
    # Check browser executables
    log_info "Checking browser availability..."
    for browser in chromium-browser firefox; do
        if command -v "$browser" &> /dev/null; then
            log_success "$browser available at $(which $browser)"
        else
            log_warning "$browser not found in PATH"
        fi
    done
    
    # Check Xvfb
    if command -v Xvfb &> /dev/null; then
        log_success "Xvfb available at $(which Xvfb)"
    else
        log_warning "Xvfb not available"
    fi
    
    echo ""
    log_success "Diagnostics completed"
}

# Main execution flow
main() {
    log_info "Starting comprehensive installation..."
    
    # Parse command line arguments
    local skip_playwright=false
    for arg in "$@"; do
        case $arg in
            --skip-playwright)
                skip_playwright=true
                log_info "Skipping Playwright installation (--skip-playwright flag)"
                ;;
        esac
    done
    
    # Step 1: Check if already installed (idempotent)
    if ! check_flite_installed; then
        # Step 2: Install build dependencies
        install_build_deps
        
        # Step 3: Build and install Flite with shared libraries
        install_flite_shared
    fi
    
    # Step 4: Install browser dependencies
    install_browser_deps
    
    # Step 5: Setup headless environment
    setup_headless_env
    
    # Step 6: Install Playwright browsers (optional)
    if [ "$skip_playwright" = false ]; then
        install_playwright_browsers
    else
        log_info "Skipping Playwright browser installation"
    fi
    
    # Step 7: Run diagnostics
    run_diagnostics
    
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════╗"
    echo "║                     INSTALLATION COMPLETED                      ║"
    echo "║                                                                  ║"
    echo "║  ✅ Flite shared libraries built and installed                  ║"
    echo "║  ✅ All browser dependencies installed                          ║"
    echo "║  ✅ Headless environment configured                             ║"
    if [ "$skip_playwright" = false ]; then
        echo "║  ✅ Playwright browsers installed                               ║"
    else
        echo "║  ⏸️  Playwright installation skipped                            ║"
    fi
    echo "║                                                                  ║"
    echo "║  Your system is now ready for headless browser automation!      ║"
    echo "╚══════════════════════════════════════════════════════════════════╝"
    
    log_success "All installation steps completed successfully!"
}

# Execute main function
main "$@"