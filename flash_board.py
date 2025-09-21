#!/usr/bin/env python3
"""
BitFloppy Board Flashing Script
===============================

A comprehensive script for flashing firmware to BitFloppy ESP32-S2 boards.
Supports multiple flashing methods and provides detailed error handling.

Usage:
    python3 flash_board.py [options]

Requirements:
    - esptool (pip install esptool)
    - Python 3.6+
    - ESP32-S2 board in bootloader mode

Author: BitFloppy Project
License: MIT
"""

import os
import sys
import time
import argparse
import subprocess
import json
from pathlib import Path
from typing import Optional, Dict, List, Tuple

# Try to import serial, handle gracefully if not available
try:
    import serial
    import serial.tools.list_ports
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False

class BitFloppyFlasher:
    """Main flashing class for BitFloppy boards."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.project_root = Path(__file__).parent
        self.firmware_dir = self.project_root / "website" / "binaries"
        self.firmware_list_file = self.firmware_dir / "firmware-list.json"
        
        # ESP32-S2 specific settings
        self.chip_type = "esp32s2"
        self.default_baudrate = 115200
        self.bootloader_baudrate = 57600  # ESP32-S2 often needs lower baudrate for bootloader
        
        # Flash addresses for ESP32-S2
        self.flash_addresses = {
            "bootloader": "0x1000",
            "partitions": "0x8000", 
            "boot_app0": "0xE000",
            "firmware": "0x10000"
        }
        
        # ESP32-S2 bootloader mode instructions
        self.bootloader_instructions = """
ESP32-S2 Bootloader Mode Instructions:
=====================================

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

Important Notes:
- Use a data USB cable, not a charging-only cable
- Ensure CP210x drivers are installed
- Board should have power (LED should be on)
- Try different USB ports if connection fails
- Close Arduino IDE, PlatformIO, or other serial monitors
        """

    def log(self, message: str, level: str = "INFO"):
        """Print log message with timestamp."""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")

    def log_verbose(self, message: str):
        """Print verbose log message."""
        if self.verbose:
            self.log(message, "VERBOSE")

    def check_dependencies(self) -> bool:
        """Check if required dependencies are installed."""
        self.log("Checking dependencies...")
        
        # Check Python version
        if sys.version_info < (3, 6):
            self.log("Python 3.6+ required", "ERROR")
            return False
            
        # Check esptool
        try:
            result = subprocess.run([sys.executable, "-m", "esptool", "--help"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.log("esptool found and working")
            else:
                self.log("esptool not found or not working", "ERROR")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log("esptool not found. Install with: pip install esptool", "ERROR")
            return False
            
        # Check pyserial
        if SERIAL_AVAILABLE:
            self.log(f"pyserial found: {serial.__version__}")
        else:
            self.log("pyserial not found. Install with: pip install pyserial", "ERROR")
            return False
            
        return True

    def list_serial_ports(self) -> List[str]:
        """List available serial ports."""
        if not SERIAL_AVAILABLE:
            self.log("pyserial not available, cannot list ports", "WARNING")
            self.log("Install pyserial with: pip install pyserial", "INFO")
            return []
            
        ports = []
        try:
            for port in serial.tools.list_ports.comports():
                ports.append(port.device)
                self.log_verbose(f"Found port: {port.device} - {port.description}")
        except Exception as e:
            self.log(f"Error listing ports: {e}", "WARNING")
            
        return ports

    def detect_board(self, port: str) -> bool:
        """Detect if board is connected and in bootloader mode."""
        self.log(f"Detecting board on {port}...")
        
        try:
            # Try to connect with esptool to detect chip without resetting
            cmd = [
                sys.executable, "-m", "esptool", 
                "--port", port,
                "--baud", str(self.bootloader_baudrate),
                "--before", "no-reset",
                "--after", "no-reset",
                "chip_id"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.log(f"Board detected on {port}")
                self.log_verbose(f"esptool output: {result.stdout}")
                return True
            else:
                self.log(f"Board not detected on {port}: {result.stderr}", "WARNING")
                return False
                
        except subprocess.TimeoutExpired:
            self.log(f"Timeout detecting board on {port}", "WARNING")
            return False
        except Exception as e:
            self.log(f"Error detecting board on {port}: {e}", "WARNING")
            return False

    def load_firmware_list(self) -> Dict:
        """Load firmware list from JSON file."""
        try:
            with open(self.firmware_list_file, 'r') as f:
                data = json.load(f)
            self.log(f"Loaded {len(data.get('firmwares', []))} firmware versions")
            return data
        except FileNotFoundError:
            self.log(f"Firmware list not found: {self.firmware_list_file}", "ERROR")
            self.log("Please ensure the firmware-list.json file exists in the binaries directory", "ERROR")
            return {}
        except json.JSONDecodeError as e:
            self.log(f"Invalid JSON in firmware list: {e}", "ERROR")
            return {}
    
    def validate_firmware_directory(self) -> bool:
        """Validate that the firmware directory structure is correct."""
        if not self.firmware_dir.exists():
            self.log(f"Firmware directory not found: {self.firmware_dir}", "ERROR")
            return False
            
        if not self.firmware_list_file.exists():
            self.log(f"Firmware list file not found: {self.firmware_list_file}", "ERROR")
            return False
            
        return True

    def list_firmware_versions(self) -> List[Dict]:
        """List available firmware versions."""
        if not self.validate_firmware_directory():
            return []
            
        data = self.load_firmware_list()
        firmwares = data.get('firmwares', [])
        
        if not firmwares:
            self.log("No firmware versions found", "WARNING")
            return []
            
        self.log("Available firmware versions:")
        for i, fw in enumerate(firmwares, 1):
            status = " (recommended)" if fw.get('recommended', False) else ""
            self.log(f"  {i}. {fw['version']} - {fw['board']}{status}")
            
        return firmwares

    def get_firmware_files(self, firmware_id: str) -> Optional[Dict[str, str]]:
        """Get firmware file paths for a specific version."""
        data = self.load_firmware_list()
        firmwares = data.get('firmwares', [])
        
        firmware = next((fw for fw in firmwares if fw['id'] == firmware_id), None)
        if not firmware:
            self.log(f"Firmware {firmware_id} not found", "ERROR")
            self.log("Available firmware versions:", "INFO")
            for fw in firmwares:
                self.log(f"  - {fw['id']} ({fw['version']})", "INFO")
            return None
            
        files = {}
        missing_files = []
        for file_type, file_info in firmware.get('files', {}).items():
            file_path = self.firmware_dir / file_info['path']
            if file_path.exists():
                files[file_type] = str(file_path)
                self.log_verbose(f"Found {file_type}: {file_path}")
            else:
                missing_files.append(f"{file_type} ({file_path})")
                
        if missing_files:
            self.log("Missing firmware files:", "ERROR")
            for missing in missing_files:
                self.log(f"  - {missing}", "ERROR")
            self.log("Please ensure all firmware files are present in the binaries directory", "ERROR")
            return None
                
        return files

    def erase_flash(self, port: str, baudrate: int = None, reset_before: bool = False, reset_after: bool = True) -> bool:
        """Erase the entire flash memory."""
        if baudrate is None:
            baudrate = self.default_baudrate
            
        self.log(f"Erasing flash memory on {port} at {baudrate} baud...")
        
        try:
            # Build esptool command for erase
            before_reset = "default-reset" if reset_before else "no-reset"
            after_reset = "hard-reset" if reset_after else "no-reset"
            cmd = [
                sys.executable, "-m", "esptool",
                "--chip", self.chip_type,
                "--port", port,
                "--baud", str(baudrate),
                "--before", before_reset,
                "--after", after_reset,
                "erase-flash"
            ]
            
            self.log_verbose(f"Running command: {' '.join(cmd)}")
            
            # Run esptool
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                self.log("Flash memory erased successfully!", "SUCCESS")
                self.log_verbose(f"esptool output: {result.stdout}")
                return True
            else:
                self.log(f"Erase failed with return code {result.returncode}", "ERROR")
                if result.stderr:
                    self.log(f"Error output: {result.stderr}", "ERROR")
                if result.stdout:
                    self.log(f"Standard output: {result.stdout}", "INFO")
                return False
                
        except subprocess.TimeoutExpired:
            self.log("Erase timed out (5 minutes)", "ERROR")
            return False
        except Exception as e:
            self.log(f"Error during erase: {e}", "ERROR")
            return False

    def flash_firmware(self, port: str, firmware_files: Dict[str, str], 
                      baudrate: int = None, reset_before: bool = False, reset_after: bool = True) -> bool:
        """Flash firmware to the board."""
        if baudrate is None:
            baudrate = self.default_baudrate
            
        self.log(f"Starting firmware flash on {port} at {baudrate} baud...")
        
        try:
            # Build esptool command
            before_reset = "default-reset" if reset_before else "no-reset"
            after_reset = "hard-reset" if reset_after else "no-reset"
            cmd = [
                sys.executable, "-m", "esptool",
                "--chip", self.chip_type,
                "--port", port,
                "--baud", str(baudrate),
                "--before", before_reset,
                "--after", after_reset,
                "write-flash"
            ]
            
            # Add flash addresses and files
            for file_type, file_path in firmware_files.items():
                if file_type in self.flash_addresses:
                    address = self.flash_addresses[file_type]
                    cmd.extend([address, file_path])
                    self.log(f"Will flash {file_type} to {address}")
            
            self.log_verbose(f"Running command: {' '.join(cmd)}")
            
            # Run esptool
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                self.log("Firmware flashed successfully!", "SUCCESS")
                self.log_verbose(f"esptool output: {result.stdout}")
                return True
            else:
                self.log(f"Flashing failed with return code {result.returncode}", "ERROR")
                if result.stderr:
                    self.log(f"Error output: {result.stderr}", "ERROR")
                if result.stdout:
                    self.log(f"Standard output: {result.stdout}", "INFO")
                return False
                
        except subprocess.TimeoutExpired:
            self.log("Flashing timed out (5 minutes)", "ERROR")
            return False
        except Exception as e:
            self.log(f"Error during flashing: {e}", "ERROR")
            return False

    def interactive_flash(self, reset_before: bool = False, reset_after: bool = True):
        """Interactive flashing mode."""
        self.log("BitFloppy Interactive Flashing Mode")
        self.log("=" * 40)
        
        # Check dependencies
        if not self.check_dependencies():
            return False
            
        # Validate firmware directory
        if not self.validate_firmware_directory():
            return False
            
        # List available ports
        ports = self.list_serial_ports()
        if not ports:
            if not SERIAL_AVAILABLE:
                self.log("pyserial not available. Please install it first:", "ERROR")
                self.log("  pip install pyserial", "INFO")
                return False
            else:
                self.log("No serial ports found. Please connect your board.", "ERROR")
                return False
            
        self.log(f"Found {len(ports)} serial port(s): {', '.join(ports)}")
        
        # Let user select port
        if len(ports) == 1:
            selected_port = ports[0]
            self.log(f"Using only available port: {selected_port}")
        else:
            while True:
                try:
                    print("\nAvailable ports:")
                    for i, port in enumerate(ports, 1):
                        print(f"  {i}. {port}")
                    
                    choice = input(f"\nSelect port (1-{len(ports)}): ").strip()
                    port_index = int(choice) - 1
                    
                    if 0 <= port_index < len(ports):
                        selected_port = ports[port_index]
                        break
                    else:
                        print("Invalid selection. Please try again.")
                except (ValueError, KeyboardInterrupt):
                    print("\nCancelled.")
                    return False
        
        # Check if board is in bootloader mode
        if not self.detect_board(selected_port):
            self.log("Board not detected or not in bootloader mode.", "WARNING")
            print(self.bootloader_instructions)
            
            retry = input("\nPut board in bootloader mode and press Enter to retry (or 'q' to quit): ").strip().lower()
            if retry == 'q':
                return False
                
            if not self.detect_board(selected_port):
                self.log("Board still not detected. Please check connections and try again.", "ERROR")
                return False
        
        # List firmware versions
        firmwares = self.list_firmware_versions()
        if not firmwares:
            return False
            
        # Let user select firmware
        while True:
            try:
                print(f"\nAvailable firmware versions:")
                for i, fw in enumerate(firmwares, 1):
                    status = " (recommended)" if fw.get('recommended', False) else ""
                    print(f"  {i}. {fw['version']} - {fw['board']}{status}")
                
                choice = input(f"\nSelect firmware (1-{len(firmwares)}): ").strip()
                fw_index = int(choice) - 1
                
                if 0 <= fw_index < len(firmwares):
                    selected_firmware = firmwares[fw_index]
                    break
                else:
                    print("Invalid selection. Please try again.")
            except (ValueError, KeyboardInterrupt):
                print("\nCancelled.")
                return False
        
        # Get firmware files
        firmware_files = self.get_firmware_files(selected_firmware['id'])
        if not firmware_files:
            return False
            
        # Confirm flashing
        print(f"\nReady to flash:")
        print(f"  Board: {selected_firmware['board']}")
        print(f"  Version: {selected_firmware['version']}")
        print(f"  Port: {selected_port}")
        print(f"  Baudrate: {self.default_baudrate}")
        
        confirm = input("\nProceed with flashing? (y/N): ").strip().lower()
        if confirm != 'y':
            self.log("Flashing cancelled by user.")
            return False
            
        # Flash the firmware
        success = self.flash_firmware(selected_port, firmware_files, reset_before=reset_before, reset_after=reset_after)
        
        if success:
            self.log("Flashing completed successfully!")
            self.log("You can now disconnect and reconnect your board.")
        else:
            self.log("Flashing failed. Please check the error messages above.", "ERROR")
            
        return success

    def auto_flash(self, port: str = None, firmware_id: str = None, 
                  baudrate: int = None, reset_before: bool = False, reset_after: bool = True) -> bool:
        """Automatic flashing mode."""
        self.log("BitFloppy Automatic Flashing Mode")
        self.log("=" * 40)
        
        # Check dependencies
        if not self.check_dependencies():
            return False
            
        # Validate firmware directory
        if not self.validate_firmware_directory():
            return False
            
        # Auto-detect port if not specified
        if not port:
            ports = self.list_serial_ports()
            if not ports:
                if not SERIAL_AVAILABLE:
                    self.log("pyserial not available. Please install it first:", "ERROR")
                    self.log("  pip install pyserial", "INFO")
                    return False
                else:
                    self.log("No serial ports found. Please connect your board.", "ERROR")
                    return False
            port = ports[0]
            self.log(f"Auto-selected port: {port}")
            
        # Auto-select firmware if not specified
        if not firmware_id:
            firmwares = self.list_firmware_versions()
            if not firmwares:
                return False
            # Select recommended firmware or first available
            selected_firmware = next((fw for fw in firmwares if fw.get('recommended', False)), firmwares[0])
            firmware_id = selected_firmware['id']
            self.log(f"Auto-selected firmware: {selected_firmware['version']}")
            
        # Get firmware files
        firmware_files = self.get_firmware_files(firmware_id)
        if not firmware_files:
            return False
            
        # Check if board is in bootloader mode
        if not self.detect_board(port):
            self.log("Board not detected or not in bootloader mode.", "ERROR")
            print(self.bootloader_instructions)
            return False
            
        # Flash the firmware
        return self.flash_firmware(port, firmware_files, baudrate, reset_before, reset_after)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="BitFloppy Board Flashing Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 flash_board.py                    # Interactive mode
  python3 flash_board.py --auto             # Auto mode
  python3 flash_board.py --port /dev/ttyUSB0 --firmware lolin_s2_mini_v0.0.1
  python3 flash_board.py --list-firmware    # List available firmware
  python3 flash_board.py --list-ports       # List available ports
  python3 flash_board.py --reset-before     # Reset board before flashing
  python3 flash_board.py --no-reset-after   # Don't reset board after flashing
  python3 flash_board.py --erase --port /dev/ttyUSB0  # Erase flash memory
        """
    )
    
    parser.add_argument("--auto", action="store_true", 
                       help="Use automatic mode (auto-detect port and firmware)")
    parser.add_argument("--port", "-p", 
                       help="Serial port to use (e.g., /dev/ttyUSB0, COM3)")
    parser.add_argument("--firmware", "-f", 
                       help="Firmware ID to flash")
    parser.add_argument("--baudrate", "-b", type=int, default=115200,
                       help="Baudrate for flashing (default: 115200)")
    parser.add_argument("--list-firmware", action="store_true",
                       help="List available firmware versions")
    parser.add_argument("--list-ports", action="store_true",
                       help="List available serial ports")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose output")
    parser.add_argument("--reset-before", action="store_true",
                       help="Reset board before flashing (default: no reset)")
    parser.add_argument("--erase", action="store_true",
                       help="Erase flash memory only (no flashing)")
    parser.add_argument("--no-reset-after", action="store_true",
                       help="Don't reset board after flashing (default: reset after)")
    
    args = parser.parse_args()
    
    # Create flasher instance
    flasher = BitFloppyFlasher(verbose=args.verbose)
    
    # Handle list commands
    if args.list_firmware:
        flasher.list_firmware_versions()
        return 0
        
    if args.list_ports:
        ports = flasher.list_serial_ports()
        if ports:
            print("Available serial ports:")
            for port in ports:
                print(f"  {port}")
        else:
            if not SERIAL_AVAILABLE:
                print("pyserial not available. Install with: pip install pyserial")
            else:
                print("No serial ports found.")
        return 0
    
    # Check dependencies
    if not flasher.check_dependencies():
        return 1
    
    # Handle erase command
    if args.erase:
        if not args.port:
            flasher.log("Port required for erase operation. Use --port option.", "ERROR")
            return 1
        reset_after = not args.no_reset_after
        success = flasher.erase_flash(args.port, args.baudrate, args.reset_before, reset_after)
        return 0 if success else 1
    
    # Run flashing
    reset_after = not args.no_reset_after
    if args.auto or (args.port and args.firmware):
        success = flasher.auto_flash(args.port, args.firmware, args.baudrate, args.reset_before, reset_after)
    else:
        success = flasher.interactive_flash(args.reset_before, reset_after)
    
    return 0 if success else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nFlashing cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
