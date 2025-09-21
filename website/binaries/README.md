# BitFloppy Firmware Binaries

This folder contains pre-built firmware binaries for BitFloppy boards.

## 📋 Quick Navigation

- **[🏠 Main Project](../../README.md)** - Project overview and development information
- **[👤 User Guide](../index.md)** - Complete user manual and operations
- **[🔧 Firmware Flashing](../flashing.md)** - Command-line firmware flashing tools

## Available Versions

### Lolin S2 Mini
- **v1.0.0** - Initial release with basic functionality
- **v1.1.0** - Added WiFi manager and improved stability
- **v1.2.0** - Enhanced security features and bug fixes
- **v1.3.0** - Latest stable release with all features

### Custom ESP32 Boards
- **Generic ESP32** - Compatible with most ESP32 development boards
- **ESP32-S2** - Optimized for ESP32-S2 series
- **ESP32-C3** - Optimized for ESP32-C3 series

## File Structure

Each firmware version is composed of 4 essential files:

- **`firmware.bin`** - Main application firmware (largest file)
- **`bootloader.bin`** - ESP32 bootloader
- **`partitions.bin`** - Partition table configuration
- **`boot_app0.bin`** - Boot application

## Directory Structure

Firmware files are organized by version and board:
```
binaries/
├── 0.0.1/
│   └── lolin_s2_mini/
│       ├── firmware.bin
│       ├── bootloader.bin
│       ├── partitions.bin
│       └── boot_app0.bin
├── 1.3.0/
│   ├── lolin_s2_mini/
│   │   ├── firmware.bin
│   │   ├── bootloader.bin
│   │   ├── partitions.bin
│   │   └── boot_app0.bin
│   └── generic_esp32/
│       ├── firmware.bin
│       ├── bootloader.bin
│       ├── partitions.bin
│       └── boot_app0.bin
└── firmware-list.json
```

## Download Links

The latest firmware binaries are automatically built and available from:
- GitHub Releases: https://github.com/your-repo/BitFloppy/releases
- CI/CD Artifacts: Built on every commit to main branch

## Verification

All firmware binaries are built from source code and can be verified using:
- SHA256 checksums provided with each release
- GPG signatures from the development team
- Source code available in the main repository

## Installation

Use the [Firmware Flashing Guide](../flashing.md) to install these binaries on your BitFloppy board.

## Firmware List

The flasher automatically loads the list of available firmware from `firmware-list.json` in this folder. This file contains:

- **Firmware metadata** - Version, board compatibility, size, release date
- **Changelog information** - What's new in each version
- **File paths** - Links to the actual binary files
- **Categories** - Organized by board type
- **Recommendations** - Which versions are recommended for production use

To add new firmware versions, simply:
1. Add the new `.bin` file to this folder
2. Update `firmware-list.json` with the new firmware information
3. The flasher will automatically detect and display the new option
