# BitFloppy with Sparrow Wallet

This guide explains how to use BitFloppy with Sparrow Wallet for Bitcoin transactions.

## 📋 Quick Navigation

- **[🏠 Main Project](../README.md)** - Project overview and development information
- **[👤 User Guide](index.md)** - Complete user manual and operations
- **[🔧 Firmware Flashing](flashing.md)** - Command-line firmware flashing tools
- **[💾 Firmware Binaries](binaries/)** - Download pre-built firmware

## 🔗 Integration with Sparrow Wallet

### Setup BitFloppy with Sparrow

1. **Flash Firmware**: Use the [firmware flashing guide](flashing.md) to flash your BitFloppy board
2. **Connect Board**: Plug in your BitFloppy board via USB
3. **Access Files**: The board appears as a 1.44 MB mass storage device
4. **Get Descriptor**: Copy the descriptor from the appropriate BIP directory

### Using with Sparrow Wallet

#### Receive Funds

1. **Get Address**: Copy an address from `bip84/addresses.txt` (or bip44/bip49)
2. **Import to Sparrow**: Use the address in Sparrow for receiving funds
3. **Monitor**: Check the address on a block explorer

#### Spend Funds

1. **Create PSBT**: In Sparrow, create a Partially Signed Bitcoin Transaction
2. **Export PSBT**: Save the PSBT as base64
3. **Sign with BitFloppy**:
   - Create a file named `PSBT.txt` on the BitFloppy mass storage
   - Paste the base64 PSBT into the file
   - Unmount the volume
   - Restart the board
   - The board will generate `PSBT_signed.txt` with the signed PSBT
4. **Import Signed PSBT**: Load the signed PSBT back into Sparrow
5. **Broadcast**: Send the transaction to the network

### Supported BIP Standards

- **BIP44** - Legacy Bitcoin addresses (P2PKH)
- **BIP49** - SegWit wrapped addresses (P2SH-P2WPKH)  
- **BIP84** - Native SegWit addresses (Bech32)

### Security Notes

- **Testnet Only**: This is a proof-of-concept, use only with testnet funds
- **Unlock Required**: Signing transactions will unlock the board temporarily
- **Backup**: Always backup your mnemonic seed phrase securely

## 🔧 Troubleshooting

### Common Issues

1. **Board Not Recognized**: Ensure firmware is properly flashed
2. **PSBT Signing Failed**: Check that the board is in the correct state
3. **Address Mismatch**: Verify you're using the correct BIP standard

### Getting Help

- Check the [User Guide](index.md) for detailed operations
- Review the [Firmware Flashing Guide](flashing.md) for technical details
- See the [Main Project](README.md) for development information
