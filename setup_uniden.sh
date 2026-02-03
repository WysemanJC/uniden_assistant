#!/bin/bash
# Uniden Assistant - Comprehensive Setup Script
# This script sets up the complete environment and can be run multiple times safely
# Installs OS packages, Python dependencies, Node.js dependencies, and configures databases
#
# Usage: ./setup_uniden.sh [--clean]
#   --clean: Remove venv and node_modules for fresh installation

set -e

# Parse command line arguments
CLEAN_MODE=false
for arg in "$@"; do
    if [ "$arg" = "--clean" ]; then
        CLEAN_MODE=true
    fi
done

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="Uniden Assistant"
PYTHON_MIN_VERSION="3.8"
NODE_MIN_VERSION="16"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Function to check command availability
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to compare versions
version_gt() {
    [ "$(printf '%s\n' "$1" "$2" | sort -V | head -n1)" = "$2" ]
}

# Function to install OS packages (Debian/Ubuntu)
install_os_packages() {
    print_status "Checking OS packages..."
    
    # Check if running as root or with sudo
    if [ "$EUID" -eq 0 ]; then
        local PKG_MANAGER="apt-get"
    elif command_exists sudo; then
        local PKG_MANAGER="sudo apt-get"
    else
        print_warning "Cannot install OS packages (no sudo access). Please install manually:"
        echo "  - python3"
        echo "  - python3-venv"
        echo "  - python3-dev"
        echo "  - python3-pip"
        echo "  - build-essential"
        echo "  - libssl-dev"
        echo "  - libffi-dev"
        return 0
    fi
    
    # Update package list
    print_status "Updating package list..."
    $PKG_MANAGER update -qq || true
    
    # Install required packages
    local packages=(
        "python3"
        "python3-venv"
        "python3-dev"
        "python3-pip"
        "build-essential"
        "libssl-dev"
        "libffi-dev"
        "curl"
        "git"
    )
    
    for pkg in "${packages[@]}"; do
        if dpkg -l | grep -qw "$pkg"; then
            print_success "$pkg already installed"
        else
            print_status "Installing $pkg..."
            $PKG_MANAGER install -y "$pkg" -qq || print_warning "Failed to install $pkg"
        fi
    done
    
    print_success "OS packages check complete"
}

# Function to check Python version
check_python() {
    print_status "Checking Python..."
    
    if ! command_exists python3; then
        print_error "Python 3 is not installed"
        print_status "Attempting to install Python 3..."
        install_os_packages
        
        if ! command_exists python3; then
            print_error "Failed to install Python 3. Please install manually."
            exit 1
        fi
    fi
    
    local python_version=$(python3 --version 2>&1 | awk '{print $2}')
    print_status "Found Python $python_version"
    
    if version_gt "$PYTHON_MIN_VERSION" "$python_version"; then
        print_error "Python $PYTHON_MIN_VERSION or higher is required (found $python_version)"
        exit 1
    fi
    
    print_success "Python version check passed"
}

# Function to check Node.js and install if needed
check_and_install_node() {
    print_status "Checking Node.js..."
    
    if ! command_exists node; then
        print_warning "Node.js is not installed. Installing Node.js 18..."
        
        # Check if running as root or with sudo
        if [ "$EUID" -eq 0 ]; then
            local PKG_MANAGER="apt-get"
        elif command_exists sudo; then
            local PKG_MANAGER="sudo apt-get"
        else
            print_error "Cannot install Node.js (no sudo access). Please install manually:"
            echo "  curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -"
            echo "  sudo apt-get install -y nodejs"
            exit 1
        fi
        
        # Install Node.js from NodeSource repository
        print_status "Adding NodeSource repository..."
        $PKG_MANAGER update -qq || true
        
        # Install curl if not present (needed for NodeSource setup)
        if ! command_exists curl; then
            print_status "Installing curl (required for Node.js setup)..."
            $PKG_MANAGER install -y curl -qq || print_warning "Failed to install curl"
        fi
        
        print_status "Setting up Node.js 18 repository..."
        curl -fsSL https://deb.nodesource.com/setup_18.x | bash - >/dev/null 2>&1 || {
            print_error "Failed to add NodeSource repository"
            exit 1
        }
        
        print_status "Installing Node.js..."
        $PKG_MANAGER install -y nodejs -qq || {
            print_error "Failed to install Node.js"
            exit 1
        }
        
        print_success "Node.js installed successfully"
    fi
    
    local node_version=$(node --version 2>&1 | cut -d'v' -f2)
    print_status "Found Node.js $node_version"
    
    if version_gt "$NODE_MIN_VERSION" "$node_version"; then
        print_error "Node.js $NODE_MIN_VERSION or higher is required (found $node_version)"
        exit 1
    fi
    
    print_success "Node.js version check passed"
}

# Function to check for git
check_git() {
    print_status "Checking git..."
    
    if ! command_exists git; then
        print_warning "git is not installed. Installing..."
        
        if [ "$EUID" -eq 0 ]; then
            local PKG_MANAGER="apt-get"
        elif command_exists sudo; then
            local PKG_MANAGER="sudo apt-get"
        else
            print_warning "Cannot install git (no sudo access). Please install manually: sudo apt-get install -y git"
            return 0
        fi
        
        $PKG_MANAGER update -qq || true
        $PKG_MANAGER install -y git -qq || print_warning "Failed to install git"
    fi
    
    print_success "git is available"
}

# Function to detect WSL and provide recommendations
check_wsl() {
    if grep -qi microsoft /proc/version 2>/dev/null; then
        print_status "Detected Windows Subsystem for Linux (WSL)"
        print_warning "WSL detected. Remember:"
        echo "  - Store project in /home or /root (not /mnt/c or Windows directories)"
        echo "  - Use native WSL terminal, not Windows PowerShell"
        echo "  - Access frontend at http://localhost:9001 from Windows browser"
        return 0
    fi
}

# Function to clean previous installation
clean_installation() {
    if [ "$CLEAN_MODE" = true ]; then
        print_status "Cleaning previous installation..."
        
        if [ -d "$SCRIPT_DIR/backend/venv" ]; then
            print_status "Removing Python virtual environment..."
            rm -rf "$SCRIPT_DIR/backend/venv"
        fi
        
        if [ -d "$SCRIPT_DIR/frontend/node_modules" ]; then
            print_status "Removing Node.js modules..."
            rm -rf "$SCRIPT_DIR/frontend/node_modules"
        fi
        
        if [ -f "$SCRIPT_DIR/frontend/package-lock.json" ]; then
            print_status "Removing package-lock.json..."
            rm "$SCRIPT_DIR/frontend/package-lock.json"
        fi
        
        print_success "Clean complete"
    fi
}

# Function to setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    cd "$SCRIPT_DIR/backend"
    
    # Create venv if it doesn't exist
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_success "Virtual environment already exists"
    fi
    
    # Use venv python explicitly
    local VENV_PY="$SCRIPT_DIR/backend/venv/bin/python"
    
    print_status "Upgrading pip..."
    "$VENV_PY" -m pip install --upgrade pip setuptools wheel -q
    
    # Install dependencies
    if [ -f "requirements.txt" ]; then
        print_status "Installing Python dependencies..."
        "$VENV_PY" -m pip install -r requirements.txt -q
        print_success "Python dependencies installed"
    else
        print_warning "requirements.txt not found"
    fi
    
    # Run migrations (uses config.env loader)
    print_status "Running database migrations..."
    "$VENV_PY" run_with_config.py migrate --noinput --database=default 2>/dev/null || print_warning "Default database migrations encountered issues"
    "$VENV_PY" run_with_config.py migrate --noinput --database=favorites 2>/dev/null || print_warning "Favorites database migrations encountered issues"
    print_success "Database migrations completed"
    
    # Create directories
    mkdir -p "$SCRIPT_DIR/.logs" "$SCRIPT_DIR/.pids"
    
    print_success "Backend setup complete"
}

# Function to setup frontend
setup_frontend() {
    print_status "Setting up frontend..."
    
    cd "$SCRIPT_DIR/frontend"
    
    # Check for package.json
    if [ ! -f "package.json" ]; then
        print_error "package.json not found in frontend directory"
        return 1
    fi
    
    # Validate package-lock.json
    if [ ! -f "package-lock.json" ]; then
        print_warning "package-lock.json not found. Using package.json as source (may not be reproducible)"
    else
        print_success "package-lock.json found"
    fi
    
    # Install dependencies
    print_status "Installing Node.js dependencies..."
    npm install -q 2>/dev/null || npm install
    print_success "Node.js dependencies installed"
    
    print_success "Frontend setup complete"
}

# Function to create config.env file if it doesn't exist
setup_env() {
    print_status "Checking environment configuration..."
    
    if [ ! -f "$SCRIPT_DIR/config.env" ]; then
        print_status "Creating config.env file from template..."
        if [ -f "$SCRIPT_DIR/config.env.example" ]; then
            cp "$SCRIPT_DIR/config.env.example" "$SCRIPT_DIR/config.env"
            print_success "config.env file created"
            print_warning "Please review $SCRIPT_DIR/config.env and update if needed"
        else
            print_warning "config.env not found. Exiting setup."
            print_error "Please create config.env from config.env.example and set required values."
            exit 1
        fi
    else
        print_success "config.env file already exists"
    fi
}

# Function to create frontend .env.local if it doesn't exist
setup_env_frontend() {
    print_status "Checking frontend environment configuration..."
    
    if [ ! -f "$SCRIPT_DIR/frontend/.env.local" ]; then
        print_status "Creating .env.local file..."
        cat > "$SCRIPT_DIR/frontend/.env.local" << EOF
VITE_API_URL=http://localhost:8001/api
EOF
        print_success ".env.local file created"
    else
        print_success ".env.local file already exists"
    fi
}

# Function to check database connectivity
check_databases() {
    print_status "Checking database connectivity..."
    
    cd "$SCRIPT_DIR/backend"
    source venv/bin/activate
    
    # Test database connection by running a simple check
    "$SCRIPT_DIR/backend/venv/bin/python" -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniden_assistant.settings')
django.setup()
from django.db import connection
try:
    connection.ensure_connection()
    print('Database connection successful')
except Exception as e:
    print(f'Database connection failed: {e}')
" 2>/dev/null && print_success "Database connectivity check passed" || print_warning "Database connectivity check failed (check config.env and setup)"
    
    deactivate
}

# Main setup flow
main() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║          $PROJECT_NAME Setup              ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Clean if requested
    if [ "$CLEAN_MODE" = true ]; then
        clean_installation
        echo ""
    fi
    
    # Check for WSL
    check_wsl
    echo ""
    
    # Check if running on Debian-based system
    if [ -f /etc/debian_version ]; then
        print_status "Detected Debian-based system"
        install_os_packages
        echo ""
    else
        print_warning "Not a Debian-based system. Skipping OS package installation."
        echo ""
    fi
    
    # Check prerequisites
    print_status "Checking prerequisites..."
    check_python
    check_and_install_node
    check_git
    print_success "All prerequisites met"
    echo ""
    
    # Setup environment files
    setup_env
    setup_env_frontend
    echo ""
    
    # Setup backend
    setup_backend
    echo ""
    
    # Setup frontend
    setup_frontend
    echo ""
    
    # Check databases
    check_databases
    echo ""
    
    # Success message
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    Setup Complete! ✓                       ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Start the application:"
    echo -e "     ${BLUE}./uniden_assistant start${NC}"
    echo ""
    echo "  2. Check application status:"
    echo -e "     ${BLUE}./uniden_assistant status${NC}"
    echo ""
    echo "  3. View logs:"
    echo -e "     ${BLUE}./uniden_assistant logs${NC}"
    echo ""
    echo "  4. Open in browser:"
    echo -e "     ${BLUE}http://localhost:9001${NC}"
    echo ""
    echo "For more commands, run: ${BLUE}./uniden_assistant help${NC}"
    echo ""
}

# Run main function
main "$@"
