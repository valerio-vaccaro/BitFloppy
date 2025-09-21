# BitFloppy

A Bitcoin hardware wallet disguised as a 1.44 MB floppy disk using ESP32-S2 technology.

## 🎯 Overview

BitFloppy is a unique Bitcoin hardware wallet that presents itself as a 1.44 MB mass storage device. When connected to a computer, it appears as a floppy disk containing Bitcoin wallet files, making it inconspicuous and portable.

## 🚀 Quick Start

1. **Flash Firmware**: Use our [command-line tools](website/flashing.md)
2. **Connect Board**: Plug in your BitFloppy board via USB
3. **Access Wallet**: The board appears as a 1.44 MB mass storage device
4. **Use Wallet**: Interact with Bitcoin addresses and sign transactions

## 📁 Documentation

- **[User Guide](website/index.md)** - Complete user manual and operations
- **[Firmware Flashing](website/flashing.md)** - How to flash firmware to your board
- **[Firmware Binaries](website/binaries/)** - Download pre-built firmware

## 🔧 How It Works

Every time you restart the board, the software updates its status and performs needed actions. When complete, the board shows a 1.44 MB Mass Storage interface with various Bitcoin wallet files.

## 📊 Board Status

A board can be in one of the following states:

- **UNKNOWN** → Board is new and never used (auto-changes to EMPTY)
- **EMPTY** → No secret material, will generate and change to LOCKED
- **LOCKED** → Derives all files and waits (secure state)
- **UNLOCKED** → Derives all files including secrets and waits
- **CUSTOM_EMPTY** → Custom configuration, no secrets yet
- **CUSTOM_LOCKED** → Custom configuration with locked secrets
- **CUSTOM_UNLOCKED** → Custom configuration with unlocked secrets
- **FORMAT** → Will delete all data and reset to EMPTY or CUSTOM_EMPTY

## 📄 Generated Files

The board creates the following files in the mass storage:

### Core Files
- `mnemonic.txt` - The mnemonic seed (only in unlocked status)
- `network.txt` - The network used (mainnet/testnet/signet)
- `passphrase.txt` - The passphrase used (only in unlocked status)
- `log.txt` - Complete log of all actions performed
- `README.txt` - Brief explanation of the wallet

### BIP Derivation Directories
- **bip44/** - Legacy Bitcoin addresses
- **bip49/** - SegWit wrapped addresses (P2SH-P2WPKH)
- **bip84/** - Native SegWit addresses (Bech32)

Each directory contains:
- `addresses.txt` - List of derived addresses (0/*)
- `changes.txt` - List of change addresses (1/*)
- `xpub.txt` - Extended public key
- `xpriv.txt` - Extended private key (*** if locked)

## ⚡ Operations

### 🔄 Initialization
Automatic - no action required. Files are generated every time you turn on the board, so deleted files will be restored on reboot.

### 🔓 Unlock
To reveal secrets (mnemonic, passphrase, private keys):
1. Create a file named `UNLOCK.txt`
2. Unmount the volume
3. Restart the board
4. New files with secrets will be generated

### ✍️ Sign PSBT
To sign a Partially Signed Bitcoin Transaction:
1. Write the PSBT (base64) in a file named `PSBT.txt`
2. Unmount the volume
3. Restart the board
4. The board will generate `PSBT_signed.txt` with the signed PSBT
5. **Note**: This action will UNLOCK the board!

### 🔄 Format
To change the mnemonic or reset the wallet:
1. Create a file named `FORMAT.txt`
2. Optionally create `MNEMONIC.txt` with custom mnemonic
3. Optionally create `PASSPHRASE.txt` with custom passphrase
4. Optionally create `NETWORK.txt` with custom network
5. Unmount the volume
6. Restart the board

## 🔧 Hardware Support

- **Lolin S2 Mini** - Primary supported board
- **ESP32-S2** - Compatible with other ESP32-S2 boards

## ⚠️ Security Notice

**This project is a Proof-of-Concept. Use only with testnet or signet funds!**

**Are my funds safe? NO, PLEASE DON'T USE WITH REAL FUNDS.**

## 🛠️ Development

### Building from Source
```bash
# Install PlatformIO
pip install platformio

# Build firmware
pio run

# Flash firmware
pio run --target upload --upload-port /dev/ttyUSB0
```

### Flashing Scripts
- `flash_board.sh` - Interactive shell script
- `flash_board.py` - Python command-line tool
- `flash_pio.py` - PlatformIO integration

See [website/flashing.md](website/flashing.md) for detailed instructions.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the [User Guide](website/index.md)
- Review the [Firmware Flashing Guide](website/flashing.md)
