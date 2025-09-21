#!/bin/bash
#
# BitFloppy Board Flashing Script
# ===============================
#
# A shell script wrapper for flashing BitFloppy ESP32-S2 boards.
# This script provides easy command-line access to the Python flasher
# and includes PlatformIO integration.
#
# Usage:
#   ./flash_board.sh [options]
#   ./flash_board.sh --help
#
# Requirements:
#   - Python 3.6+
#   - esptool (pip install esptool)
#   - pyserial (pip install pyserial)
#   - PlatformIO (optional, for building from source)
#
# Author: BitFloppy Project
# License: MIT

set -euo pipefail

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/flash_board.py"
PLATFORMIO_INI="$SCRIPT_DIR/platformio.ini"
BUILD_DIR="$SCRIPT_DIR/.pio/build"
FIRMWARE_DIR="$SCRIPT_DIR/website/binaries"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')] SUCCESS:${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[$(date +'%H:%M:%S')] WARNING:${NC} $1"
}

log_error() {
    echo -e "${RED}[$(date +'%H:%M:%S')] ERROR:${NC} $1"
}

# Help function
show_help() {
    cat << EOF
BitFloppy Board Flashing Script
===============================

A comprehensive script for flashing firmware to BitFloppy ESP32-S2 boards.

USAGE:
    $0 [OPTIONS]

OPTIONS:
    -h, --help              Show this help message
    -i, --interactive       Interactive mode (default)
    -a, --auto              Automatic mode (auto-detect port and firmware)
    -p, --port PORT         Serial port to use (e.g., /dev/ttyUSB0, COM3)
    -f, --firmware ID       Firmware ID to flash
    -b, --baudrate RATE     Baudrate for flashing (default: 115200)
    -l, --list-firmware     List available firmware versions
    -s, --list-ports        List available serial ports
    -v, --verbose           Enable verbose output
    --build                 Build firmware from source using PlatformIO
    --clean                 Clean build directory before building
    --monitor               Open serial monitor after flashing
    --check-deps            Check if all dependencies are installed
    --install-deps          Install required dependencies
    --reset-before          Reset board before flashing (default: no reset)
    --no-reset-after        Don't reset board after flashing (default: reset after)
    --erase                 Erase flash memory only (no flashing)

EXAMPLES:
    $0                                    # Interactive mode
    $0 --auto                            # Auto mode
    $0 --port /dev/ttyUSB0 --firmware lolin_s2_mini_v0.0.1
    $0 --list-firmware                   # List available firmware
    $0 --list-ports                      # List available ports
    $0 --build --flash                   # Build and flash from source
    $0 --check-deps                      # Check dependencies
    $0 --install-deps                    # Install dependencies
    $0 --no-reset-after                  # Don't reset board after flashing
    $0 --erase --port /dev/ttyUSB0       # Erase flash memory

BOOTLOADER MODE INSTRUCTIONS:
    For ESP32-S2 boards, you need to put the board in bootloader mode:
    
    Method 1 (GPIO0 - Most Common):
    1. Hold GPIO0 to GND (ground)
    2. Press and hold RESET while keeping GPIO0 pressed
    3. Release RESET first, then release GPIO0
    4. Keep GPIO0 held for at least 2 seconds after RESET
    
    Method 2 (GPIO45 - Some Boards):
    1. Hold GPIO45 to GND
    2. Press and hold RESET while keeping GPIO45 pressed
    3. Release RESET first, then release GPIO45
    4. Keep GPIO45 held for at least 2 seconds after RESET
    
    Method 3 (BOOT Button - If Available):
    1. Hold the BOOT button
    2. Press and hold RESET while keeping BOOT pressed
    3. Release RESET first, then release BOOT

REQUIREMENTS:
    - Python 3.6+
    - esptool (pip install esptool)
    - pyserial (pip install pyserial)
    - PlatformIO (optional, for building from source)

EOF
}

# Check if Python script exists
check_python_script() {
    if [[ ! -f "$PYTHON_SCRIPT" ]]; then
        log_error "Python flashing script not found: $PYTHON_SCRIPT"
        exit 1
    fi
}

# Check if Python is available
check_python() {
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not installed or not in PATH"
        exit 1
    fi
    
    # Check Python version
    python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    python_major=$(echo "$python_version" | cut -d. -f1)
    python_minor=$(echo "$python_version" | cut -d. -f2)
    
    if [[ $python_major -lt 3 ]] || [[ $python_major -eq 3 && $python_minor -lt 6 ]]; then
        log_error "Python 3.6+ required, found $python_version"
        exit 1
    fi
    
    log "Python $python_version found"
}

# Check dependencies
check_dependencies() {
    log "Checking dependencies..."
    
    # Check Python
    check_python
    
    # Check esptool
    if ! python3 -m esptool --help &> /dev/null; then
        log_error "esptool not found. Install with: pip install esptool"
        return 1
    fi
    
    # Check pyserial
    if ! python3 -c "import serial" &> /dev/null; then
        log_error "pyserial not found. Install with: pip install pyserial"
        return 1
    fi
    
    log_success "All dependencies found"
    return 0
}

# Install dependencies
install_dependencies() {
    log "Installing dependencies..."
    
    # Check if pip is available
    if ! command -v pip3 &> /dev/null; then
        log_error "pip3 is not available. Please install pip first."
        exit 1
    fi
    
    # Install required packages
    log "Installing esptool..."
    pip3 install esptool
    
    log "Installing pyserial..."
    pip3 install pyserial
    
    # Optionally install PlatformIO
    if command -v pio &> /dev/null; then
        log "PlatformIO already installed"
    else
        log "Installing PlatformIO..."
        pip3 install platformio
    fi
    
    log_success "Dependencies installed successfully"
}

# List available ports
list_ports() {
    log "Scanning for serial ports..."
    python3 -c "
try:
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
    if ports:
        print('Available serial ports:')
        for port in ports:
            print(f'  {port.device} - {port.description}')
    else:
        print('No serial ports found.')
except ImportError:
    print('pyserial not available. Install with: pip install pyserial')
except Exception as e:
    print(f'Error listing ports: {e}')
"
}

# List available firmware
list_firmware() {
    log "Loading firmware list..."
    python3 "$PYTHON_SCRIPT" --list-firmware
}

# Build firmware using PlatformIO
build_firmware() {
    log "Building firmware using PlatformIO..."
    
    if [[ ! -f "$PLATFORMIO_INI" ]]; then
        log_error "PlatformIO configuration not found: $PLATFORMIO_INI"
        exit 1
    fi
    
    # Check if PlatformIO is available
    if ! command -v pio &> /dev/null; then
        log_error "PlatformIO not found. Install with: pip install platformio"
        exit 1
    fi
    
    # Clean if requested
    if [[ "$CLEAN_BUILD" == "true" ]]; then
        log "Cleaning build directory..."
        pio run --target clean
    fi
    
    # Build firmware
    log "Building firmware..."
    if pio run; then
        log_success "Firmware built successfully"
        
        # Copy built firmware to binaries directory
        if [[ -d "$BUILD_DIR" ]]; then
            log "Copying built firmware to binaries directory..."
            mkdir -p "$FIRMWARE_DIR/0.0.1/lolin_s2_mini"
            
            # Find the built firmware files
            find "$BUILD_DIR" -name "*.bin" -type f | while read -r file; do
                filename=$(basename "$file")
                case "$filename" in
                    "bootloader.bin")
                        cp "$file" "$FIRMWARE_DIR/0.0.1/lolin_s2_mini/"
                        log "Copied bootloader.bin"
                        ;;
                    "partitions.bin")
                        cp "$file" "$FIRMWARE_DIR/0.0.1/lolin_s2_mini/"
                        log "Copied partitions.bin"
                        ;;
                    "boot_app0.bin")
                        cp "$file" "$FIRMWARE_DIR/0.0.1/lolin_s2_mini/"
                        log "Copied boot_app0.bin"
                        ;;
                    "firmware.bin")
                        cp "$file" "$FIRMWARE_DIR/0.0.1/lolin_s2_mini/"
                        log "Copied firmware.bin"
                        ;;
                esac
            done
            
            log_success "Built firmware copied to binaries directory"
        fi
    else
        log_error "Firmware build failed"
        exit 1
    fi
}

# Flash firmware
flash_firmware() {
    local args=()
    
    # Add common arguments
    if [[ "$VERBOSE" == "true" ]]; then
        args+=("--verbose")
    fi
    
    if [[ "$AUTO_MODE" == "true" ]]; then
        args+=("--auto")
    fi
    
    if [[ -n "$PORT" ]]; then
        args+=("--port" "$PORT")
    fi
    
    if [[ -n "$FIRMWARE" ]]; then
        args+=("--firmware" "$FIRMWARE")
    fi
    
    if [[ -n "$BAUDRATE" ]]; then
        args+=("--baudrate" "$BAUDRATE")
    fi
    
    if [[ "$RESET_BEFORE" == "true" ]]; then
        args+=("--reset-before")
    fi
    
    if [[ "$NO_RESET_AFTER" == "true" ]]; then
        args+=("--no-reset-after")
    fi
    
    # Run Python flashing script
    log "Starting firmware flashing..."
    if python3 "$PYTHON_SCRIPT" "${args[@]}"; then
        log_success "Firmware flashing completed successfully"
        return 0
    else
        log_error "Firmware flashing failed"
        return 1
    fi
}

# Open serial monitor
open_monitor() {
    local port="$1"
    local baudrate="${2:-115200}"
    
    log "Opening serial monitor on $port at $baudrate baud..."
    
    if command -v pio &> /dev/null; then
        pio device monitor --port "$port" --baud "$baudrate"
    elif command -v screen &> /dev/null; then
        screen "$port" "$baudrate"
    elif command -v minicom &> /dev/null; then
        minicom -D "$port" -b "$baudrate"
    else
        log_warning "No serial monitor found. Install screen, minicom, or use PlatformIO"
        log "You can manually open a serial monitor on $port at $baudrate baud"
    fi
}

# Main function
main() {
    # Default values
    INTERACTIVE_MODE="true"
    AUTO_MODE="false"
    PORT=""
    FIRMWARE=""
    BAUDRATE="115200"
    VERBOSE="false"
    BUILD_FIRMWARE="false"
    CLEAN_BUILD="false"
    MONITOR_AFTER="false"
    CHECK_DEPS="false"
    INSTALL_DEPS="false"
    RESET_BEFORE="false"
    NO_RESET_AFTER="false"
    ERASE_FLASH="false"
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -i|--interactive)
                INTERACTIVE_MODE="true"
                AUTO_MODE="false"
                shift
                ;;
            -a|--auto)
                AUTO_MODE="true"
                INTERACTIVE_MODE="false"
                shift
                ;;
            -p|--port)
                PORT="$2"
                shift 2
                ;;
            -f|--firmware)
                FIRMWARE="$2"
                shift 2
                ;;
            -b|--baudrate)
                BAUDRATE="$2"
                shift 2
                ;;
            -l|--list-firmware)
                list_firmware
                exit 0
                ;;
            -s|--list-ports)
                list_ports
                exit 0
                ;;
            -v|--verbose)
                VERBOSE="true"
                shift
                ;;
            --build)
                BUILD_FIRMWARE="true"
                shift
                ;;
            --clean)
                CLEAN_BUILD="true"
                shift
                ;;
            --monitor)
                MONITOR_AFTER="true"
                shift
                ;;
            --check-deps)
                CHECK_DEPS="true"
                shift
                ;;
    --install-deps)
        INSTALL_DEPS="true"
        shift
        ;;
    --reset-before)
        RESET_BEFORE="true"
        shift
        ;;
    --erase)
        ERASE_FLASH="true"
        shift
        ;;
    --no-reset-after)
        NO_RESET_AFTER="true"
        shift
        ;;
    *)
        log_error "Unknown option: $1"
        show_help
        exit 1
        ;;
        esac
    done
    
    # Handle special commands
    if [[ "$CHECK_DEPS" == "true" ]]; then
        check_dependencies
        exit $?
    fi
    
    if [[ "$INSTALL_DEPS" == "true" ]]; then
        install_dependencies
        exit $?
    fi
    
    # Handle erase command
    if [[ "$ERASE_FLASH" == "true" ]]; then
        if [[ -z "$PORT" ]]; then
            log_error "Port required for erase operation. Use --port option."
            exit 1
        fi
        
        # Check dependencies
        if ! check_dependencies; then
            log_error "Dependencies check failed. Run with --install-deps to install them."
            exit 1
        fi
        
        # Run erase command
        log "Starting flash erase..."
        if python3 "$PYTHON_SCRIPT" --erase --port "$PORT" --baudrate "$BAUDRATE" ${RESET_BEFORE:+--reset-before} ${NO_RESET_AFTER:+--no-reset-after} ${VERBOSE:+--verbose}; then
            log_success "Flash erase completed successfully"
            exit 0
        else
            log_error "Flash erase failed"
            exit 1
        fi
    fi
    
    # Check Python script
    check_python_script
    
    # Build firmware if requested
    if [[ "$BUILD_FIRMWARE" == "true" ]]; then
        build_firmware
    fi
    
    # Check dependencies
    if ! check_dependencies; then
        log_error "Dependencies check failed. Run with --install-deps to install them."
        exit 1
    fi
    
    # Flash firmware
    if flash_firmware; then
        # Open monitor if requested
        if [[ "$MONITOR_AFTER" == "true" && -n "$PORT" ]]; then
            open_monitor "$PORT" "$BAUDRATE"
        fi
        exit 0
    else
        exit 1
    fi
}

# Run main function
main "$@"
