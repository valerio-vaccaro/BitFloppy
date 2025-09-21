# BitFloppy Board Flashing Guide

This guide provides comprehensive instructions for flashing firmware to BitFloppy ESP32-S2 boards using multiple methods.

## 📋 Quick Navigation

- **[🏠 Main Project](../README.md)** - Project overview and development information
- **[👤 User Guide](index.md)** - Complete user manual and operations
- **[💾 Firmware Binaries](binaries/)** - Download pre-built firmware
- **[🕊️ Sparrow Wallet Integration](sparrow.md)** - Use with Sparrow Wallet

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Available Scripts](#available-scripts)
- [Prerequisites](#prerequisites)
- [ESP32-S2 Bootloader Mode](#esp32-s2-bootloader-mode)
- [Flashing Methods](#flashing-methods)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)
- [Error Codes](#error-codes)

## 🚀 Quick Start

### Method 1: Interactive Shell Script (Recommended)
```bash
./flash_board.sh
```

### Method 2: Python Script
```bash
python3 flash_board.py
```

### Method 3: PlatformIO Integration
```bash
python3 flash_pio.py
```

### Prerequisites Check
Before flashing, ensure all dependencies are installed:
```bash
# Check dependencies
./flash_board.sh --check-deps

# Install missing dependencies
./flash_board.sh --install-deps

# For PlatformIO (optional)
python3 flash_pio.py --install-pio
```

## 📜 Available Scripts

### 1. `flash_board.sh` - Shell Script Wrapper
**Best for**: Quick flashing, dependency management, PlatformIO integration

**Features**:
- Interactive and automatic modes
- Dependency checking and installation
- PlatformIO build integration
- Serial monitor support
- Comprehensive error handling

**Usage**:
```bash
# Interactive mode
./flash_board.sh

# Auto mode
./flash_board.sh --auto

# Specific port and firmware
./flash_board.sh --port /dev/ttyUSB0 --firmware lolin_s2_mini_v0.0.1

# Build and flash from source
./flash_board.sh --build --flash --port /dev/ttyUSB0

# Check dependencies
./flash_board.sh --check-deps

# Install dependencies
./flash_board.sh --install-deps
```

### 2. `flash_board.py` - Python Script
**Best for**: Programmatic use, detailed control, esptool integration

**Features**:
- Direct esptool integration
- Automatic port detection
- Firmware version management
- Comprehensive error handling
- ESP32-S2 specific optimizations

**Usage**:
```bash
# Interactive mode
python3 flash_board.py

# Auto mode
python3 flash_board.py --auto

# Specific parameters
python3 flash_board.py --port /dev/ttyUSB0 --firmware lolin_s2_mini_v0.0.1 --baudrate 115200

# List available firmware
python3 flash_board.py --list-firmware

# List available ports
python3 flash_board.py --list-ports
```

### 3. `flash_pio.py` - PlatformIO Script
**Best for**: Building from source, PlatformIO workflows, development

**Features**:
- PlatformIO build integration
- Environment management
- Source code compilation
- Binary management
- Development workflow

**Usage**:
```bash
# Interactive mode
python3 flash_pio.py

# Build only
python3 flash_pio.py --build

# Flash only
python3 flash_pio.py --flash --port /dev/ttyUSB0

# Build and flash
python3 flash_pio.py --build --flash --port /dev/ttyUSB0

# Serial monitor
python3 flash_pio.py --monitor --port /dev/ttyUSB0
```

## 🔧 Prerequisites

### Required Software

1. **Python 3.6+**
   ```bash
   python3 --version
   ```

2. **esptool**
   ```bash
   pip install esptool
   ```

3. **pyserial**
   ```bash
   pip install pyserial
   ```

4. **PlatformIO** (optional, for building from source)
   ```bash
   pip install platformio
   ```

### Automatic Dependency Management

The flashing scripts now include automatic dependency checking and installation:

- **Check Dependencies**: `./flash_board.sh --check-deps`
- **Install Dependencies**: `./flash_board.sh --install-deps`
- **Install PlatformIO**: `python3 flash_pio.py --install-pio`

### Improved Error Handling

The scripts now provide:
- Better error messages for missing dependencies
- Detailed troubleshooting information
- Automatic validation of firmware files
- Enhanced port detection and board detection

### Hardware Requirements

- BitFloppy ESP32-S2 board
- USB data cable (not charging-only)
- Computer with USB port
- Proper USB drivers installed

### Driver Installation

#### Windows
- **CP210x**: Download from [Silicon Labs](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers)
- **CH340**: Download from [CH340 Drivers](https://sparks.gogo.co.nz/ch340.html)

#### macOS
- Drivers usually install automatically
- If needed, install CP210x drivers from Silicon Labs

#### Linux
- Usually works out of the box
- May need to add user to dialout group:
  ```bash
  sudo usermod -a -G dialout $USER
  ```

## 🔌 ESP32-S2 Bootloader Mode

**CRITICAL**: The board must be in bootloader mode before flashing!

### Method 1: GPIO0 (Most Common)
1. **Hold GPIO0 to GND** (ground)
2. **Press and hold RESET** while keeping GPIO0 pressed
3. **Release RESET first**, then release GPIO0
4. **Keep GPIO0 held** for at least 2 seconds after RESET

### Method 2: GPIO45 (Some Boards)
Some ESP32-S2 boards use GPIO45 instead of GPIO0:
1. **Hold GPIO45 to GND**
2. **Press and hold RESET** while keeping GPIO45 pressed
3. **Release RESET first**, then release GPIO45
4. **Keep GPIO45 held** for at least 2 seconds after RESET

### Method 3: BOOT Button (If Available)
1. **Hold the BOOT button**
2. **Press and hold RESET** while keeping BOOT pressed
3. **Release RESET first**, then release BOOT

### Visual Indicators
- **Power LED**: Should be on (indicates board has power)
- **Bootloader Mode**: Usually no specific LED indication
- **Success**: Board should respond to flashing commands

## 🔄 Flashing Methods

### Method 1: Pre-built Firmware
Use existing firmware from the `website/binaries/` directory:

```bash
# Interactive selection
./flash_board.sh

# Specific firmware
./flash_board.sh --firmware lolin_s2_mini_v0.0.1 --port /dev/ttyUSB0
```

### Method 2: Build from Source
Compile and flash from source code:

```bash
# Build and flash
./flash_board.sh --build --flash --port /dev/ttyUSB0

# Or using PlatformIO directly
python3 flash_pio.py --build --flash --port /dev/ttyUSB0
```

### Method 3: Flash Erase
Completely erase flash memory before flashing:

```bash
# Erase flash memory
./flash_board.sh --erase --port /dev/ttyUSB0
python3 flash_board.py --erase --port /dev/ttyUSB0

# Erase with reset before
./flash_board.sh --erase --port /dev/ttyUSB0 --reset-before
python3 flash_board.py --erase --port /dev/ttyUSB0 --reset-before
```

### Method 4: PlatformIO Commands
Direct PlatformIO usage:

```bash
# Build
pio run

# Flash
pio run --target upload --upload-port /dev/ttyUSB0

# Monitor
pio device monitor --port /dev/ttyUSB0
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. "No serial ports found"
**Causes**:
- Board not connected
- Wrong USB cable (charging-only)
- Drivers not installed
- Board not powered

**Solutions**:
- Check USB connection
- Use data cable, not charging cable
- Install proper drivers
- Ensure board has power (LED on)

#### 2. "Failed to open serial port"
**Causes**:
- Board not in bootloader mode
- Port already in use
- Permission issues
- Wrong port selected

**Solutions**:
- Put board in bootloader mode (see instructions above)
- Close Arduino IDE, PlatformIO, or other serial monitors
- Check port permissions
- Try different USB port

#### 3. "Board not detected"
**Causes**:
- Board not in bootloader mode
- Wrong baudrate
- Hardware issues
- Driver problems

**Solutions**:
- Ensure proper bootloader mode entry
- Try different baudrates (115200, 57600, 921600)
- Check hardware connections
- Reinstall drivers

#### 4. "Flashing failed"
**Causes**:
- Board not in bootloader mode
- USB connection issues
- Firmware file problems
- Hardware issues

**Solutions**:
- Re-enter bootloader mode
- Try different USB cable/port
- Check firmware file integrity
- Verify board functionality

### ESP32-S2 Specific Issues

#### 1. GPIO0 vs GPIO45
Some boards use GPIO45 instead of GPIO0:
- Try GPIO45 if GPIO0 doesn't work
- Check board documentation
- Some clones may have different pinouts

#### 2. USB-CDC Issues
ESP32-S2 may have USB-CDC configuration issues:
- Try different baudrates
- Check USB port power
- Use powered USB hub if available

#### 3. Driver Conflicts
Multiple drivers can cause conflicts:
- Uninstall and reinstall CP210x drivers
- Check Device Manager for conflicts
- Restart computer after driver installation

### Diagnostic Steps

#### 1. Check Port Detection
```bash
# List available ports
./flash_board.sh --list-ports

# Or with Python
python3 flash_board.py --list-ports
```

#### 2. Test Board Detection
```bash
# Test with esptool directly
python3 -m esptool --port /dev/ttyUSB0 --baud 115200 chip_id
```

#### 3. Check Dependencies
```bash
# Check all dependencies
./flash_board.sh --check-deps

# Install missing dependencies
./flash_board.sh --install-deps
```

#### 4. Verify Firmware Files
```bash
# List available firmware
./flash_board.sh --list-firmware

# Check firmware file integrity
ls -la website/binaries/*/lolin_s2_mini/*.bin
```

## 🔧 Advanced Usage

### Reset Behavior Control
By default, the board is NOT reset before flashing and IS reset after flashing:

```bash
# Default behavior (no reset before, reset after)
./flash_board.sh --port /dev/ttyUSB0 --firmware lolin_s2_mini_v0.0.1
python3 flash_board.py --port /dev/ttyUSB0 --firmware lolin_s2_mini_v0.0.1

# Force reset before flashing (if needed)
./flash_board.sh --reset-before --port /dev/ttyUSB0 --firmware lolin_s2_mini_v0.0.1
python3 flash_board.py --reset-before --port /dev/ttyUSB0 --firmware lolin_s2_mini_v0.0.1

# Don't reset after flashing (keep in bootloader mode)
./flash_board.sh --no-reset-after --port /dev/ttyUSB0 --firmware lolin_s2_mini_v0.0.1
python3 flash_board.py --no-reset-after --port /dev/ttyUSB0 --firmware lolin_s2_mini_v0.0.1

# Both options combined
./flash_board.sh --reset-before --no-reset-after --port /dev/ttyUSB0 --firmware lolin_s2_mini_v0.0.1
python3 flash_board.py --reset-before --no-reset-after --port /dev/ttyUSB0 --firmware lolin_s2_mini_v0.0.1
```

**When to use `--no-reset-after`:**
- **Multiple operations**: Keep board in bootloader mode for multiple flashes
- **Debugging**: Keep board accessible for debugging after flashing
- **Development**: Avoid repeated bootloader mode entry during development
- **Batch operations**: Flash multiple firmware versions without re-entering bootloader mode
- **Port checking**: Avoid resetting board when checking available ports
- **Erase operations**: Keep board in bootloader mode after erasing flash

### Flash Erase Operations
Completely erase flash memory before flashing:

```bash
# Erase only
./flash_board.sh --erase --port /dev/ttyUSB0
python3 flash_board.py --erase --port /dev/ttyUSB0

# Erase with custom baudrate
./flash_board.sh --erase --port /dev/ttyUSB0 --baudrate 57600
python3 flash_board.py --erase --port /dev/ttyUSB0 --baudrate 57600

# Erase with reset before
./flash_board.sh --erase --port /dev/ttyUSB0 --reset-before
python3 flash_board.py --erase --port /dev/ttyUSB0 --reset-before

# Erase without reset after (keep in bootloader mode)
./flash_board.sh --erase --port /dev/ttyUSB0 --no-reset-after
python3 flash_board.py --erase --port /dev/ttyUSB0 --no-reset-after
```

### Port Detection Improvements
The port detection and board checking now avoids resetting the board:

- **Port listing**: `--list-ports` only lists available ports without board interaction
- **Board detection**: Uses `--before no-reset --after no-reset` to avoid resetting during detection
- **Bootloader mode preservation**: Board stays in bootloader mode during port checking operations

### Custom Baudrates
```bash
# Use custom baudrate
./flash_board.sh --baudrate 921600 --port /dev/ttyUSB0
python3 flash_board.py --baudrate 57600 --port /dev/ttyUSB0
```

### Environment Selection (PlatformIO)
```bash
# Use specific environment
python3 flash_pio.py --environment lolin_s2_mini --build --flash --port /dev/ttyUSB0
```

### Clean Builds
```bash
# Clean build directory
./flash_board.sh --clean --build --flash --port /dev/ttyUSB0
python3 flash_pio.py --clean --build --flash --port /dev/ttyUSB0
```

### Serial Monitoring
```bash
# Open serial monitor after flashing
./flash_board.sh --monitor --port /dev/ttyUSB0

# Monitor only
python3 flash_pio.py --monitor --port /dev/ttyUSB0
```

### Batch Operations
```bash
# Build, copy to binaries, and flash
python3 flash_pio.py --build --copy-binaries --version 0.0.2 --flash --port /dev/ttyUSB0
```

## 📊 Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 1 | General error | Check error message and try troubleshooting steps |
| 2 | Dependencies missing | Run `./flash_board.sh --install-deps` |
| 3 | Port not found | Check USB connection and drivers |
| 4 | Board not detected | Ensure board is in bootloader mode |
| 5 | Flashing failed | Check connections and try different baudrate |
| 6 | Build failed | Check source code and PlatformIO configuration |
| 7 | Permission denied | Check port permissions or run with sudo |

## 🔍 Debug Mode

Enable verbose output for detailed debugging:

```bash
# Shell script
./flash_board.sh --verbose

# Python scripts
python3 flash_board.py --verbose
python3 flash_pio.py --verbose
```

## 📝 Log Files

Scripts create detailed logs in the console. For persistent logging:

```bash
# Save output to file
./flash_board.sh --verbose 2>&1 | tee flash_log.txt
python3 flash_board.py --verbose 2>&1 | tee flash_log.txt
```

## 🤝 Support

If you encounter issues:

1. **Check this guide** for common solutions
2. **Enable verbose mode** for detailed output
3. **Check hardware connections** and bootloader mode
4. **Verify dependencies** are installed correctly
5. **Try different USB cables/ports**
6. **Check board documentation** for specific requirements

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Note**: This guide is specifically designed for BitFloppy ESP32-S2 boards. For other ESP32 variants, some features may not work as expected.
