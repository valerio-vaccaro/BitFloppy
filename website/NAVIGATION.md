# BitFloppy Website Navigation

This document provides an overview of all available documentation and tools in the BitFloppy project.

## 🏠 Main Documentation

### Project Overview
- **[Main README](../README.md)** - Complete project overview, features, and development information
- **[User Guide](index.md)** - Step-by-step user manual for operating BitFloppy
- **[Sparrow Integration](sparrow.md)** - How to use BitFloppy with Sparrow Wallet

### Firmware Flashing
- **[Firmware Flashing Guide](flashing.md)** - Comprehensive guide for command-line flashing
- **[Python Scripts](../flash_board.py)** - Python-based flashing tools
- **[Shell Scripts](../flash_board.sh)** - Shell script wrappers
- **[PlatformIO Integration](../flash_pio.py)** - PlatformIO build and flash tools

### Firmware & Binaries
- **[Firmware Binaries](binaries/)** - Download pre-built firmware
- **[Firmware List](binaries/firmware-list.json)** - JSON metadata for available firmware

## 🎯 Quick Start Paths

### For End Users
1. **[User Guide](index.md)** - Learn how to use BitFloppy
2. **[Firmware Flashing Guide](flashing.md)** - How to flash firmware
3. **[Firmware Binaries](binaries/)** - Download pre-built firmware
4. **[Sparrow Integration](sparrow.md)** - Use with Sparrow Wallet

### For Developers
1. **[Main README](../README.md)** - Project overview and development setup
2. **[Firmware Flashing Guide](flashing.md)** - Advanced flashing options
3. **[Source Code](../src/)** - C++ source code

### For Troubleshooting
1. **[User Guide](index.md)** - Basic operations and common issues
2. **[Firmware Flashing Guide](flashing.md)** - Command-line troubleshooting

## 📁 File Structure

```
BitFloppy/
├── README.md                    # Main project documentation
├── flash_board.py              # Python flashing script
├── flash_board.sh              # Shell flashing script
├── flash_pio.py                # PlatformIO integration
└── website/
    ├── index.md                 # User guide (main entry point)
    ├── flashing.md             # Firmware flashing guide
    ├── sparrow.md              # Sparrow wallet integration
    ├── NAVIGATION.md           # This navigation guide
    └── binaries/
        ├── README.md           # Firmware binaries documentation
        ├── firmware-list.json  # Firmware metadata
        └── [versions]/         # Pre-built firmware files
```

## 🔗 Cross-References

All documentation files include navigation sections that link to related content, ensuring users can easily find the information they need regardless of where they start.

## 📞 Getting Help

If you can't find what you're looking for:

1. **Check the navigation sections** in any documentation file
2. **Start with the [Main README](../README.md)** for project overview
3. **Use the [User Guide](index.md)** for operational questions
4. **Review the [Firmware Flashing Guide](flashing.md)** for technical issues
