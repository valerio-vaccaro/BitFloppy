#!/usr/bin/env python3
"""
BitFloppy PlatformIO Flashing Script
====================================

A PlatformIO-specific flashing script for BitFloppy ESP32-S2 boards.
This script integrates with PlatformIO to build and flash firmware.

Usage:
    python3 flash_pio.py [options]

Requirements:
    - PlatformIO (pip install platformio)
    - Python 3.6+

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

class BitFloppyPIOFlasher:
    """PlatformIO-based flashing class for BitFloppy boards."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.project_root = Path(__file__).parent
        self.platformio_ini = self.project_root / "platformio.ini"
        self.build_dir = self.project_root / ".pio" / "build"
        self.firmware_dir = self.project_root / "website" / "binaries"
        
        # ESP32-S2 specific settings
        self.chip_type = "esp32s2"
        self.default_baudrate = 115200
        self.bootloader_baudrate = 57600
        
        # Flash addresses for ESP32-S2
        self.flash_addresses = {
            "bootloader": "0x1000",
            "partitions": "0x8000", 
            "boot_app0": "0xE000",
            "firmware": "0x10000"
        }

    def log(self, message: str, level: str = "INFO"):
        """Print log message with timestamp."""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")

    def log_verbose(self, message: str):
        """Print verbose log message."""
        if self.verbose:
            self.log(message, "VERBOSE")

    def check_platformio(self) -> bool:
        """Check if PlatformIO is installed and working."""
        self.log("Checking PlatformIO installation...")
        
        try:
            result = subprocess.run([sys.executable, "-m", "platformio", "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.log(f"PlatformIO found: {result.stdout.strip()}")
                return True
            else:
                self.log("PlatformIO not found or not working", "ERROR")
                if result.stderr:
                    self.log(f"Error: {result.stderr.strip()}", "ERROR")
                self.log("Install with: pip install platformio", "INFO")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log("PlatformIO not found. Install with: pip install platformio", "ERROR")
            return False

    def check_project_config(self) -> bool:
        """Check if PlatformIO project is properly configured."""
        if not self.platformio_ini.exists():
            self.log(f"PlatformIO configuration not found: {self.platformio_ini}", "ERROR")
            return False
            
        self.log("PlatformIO project configuration found")
        return True
    
    def install_platformio(self) -> bool:
        """Install PlatformIO."""
        self.log("Installing PlatformIO...")
        
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "install", "platformio"], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                self.log("PlatformIO installed successfully", "SUCCESS")
                return True
            else:
                self.log(f"Failed to install PlatformIO: {result.stderr}", "ERROR")
                return False
        except subprocess.TimeoutExpired:
            self.log("PlatformIO installation timed out", "ERROR")
            return False
        except Exception as e:
            self.log(f"Error installing PlatformIO: {e}", "ERROR")
            return False

    def list_environments(self) -> List[str]:
        """List available PlatformIO environments."""
        self.log("Listing available environments...")
        
        try:
            result = subprocess.run([sys.executable, "-m", "platformio", "run", "--list-targets"], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                # Parse environments from output
                environments = []
                lines = result.stdout.split('\n')
                # Skip header line and process data lines
                for line in lines[1:]:  # Skip the header row
                    if line.strip() and not line.startswith('---'):  # Skip separator lines
                        parts = line.split()
                        if len(parts) > 0:
                            env_name = parts[0].strip()
                            if env_name and env_name not in environments:
                                environments.append(env_name)
                
                self.log(f"Found {len(environments)} environments: {', '.join(environments)}")
                return environments
            else:
                self.log(f"Failed to list environments: {result.stderr}", "ERROR")
                return []
        except subprocess.TimeoutExpired:
            self.log("Timeout listing environments", "ERROR")
            return []
        except Exception as e:
            self.log(f"Error listing environments: {e}", "ERROR")
            return []

    def build_firmware(self, environment: str = None, clean: bool = False) -> bool:
        """Build firmware using PlatformIO."""
        self.log("Building firmware with PlatformIO...")
        
        try:
            cmd = [sys.executable, "-m", "platformio", "run"]
            
            if environment:
                cmd.extend(["-e", environment])
                
            if clean:
                cmd.append("-t")
                cmd.append("clean")
                self.log("Cleaning build directory...")
                
                # Run clean first
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                if result.returncode != 0:
                    self.log(f"Clean failed: {result.stderr}", "WARNING")
                
                # Remove clean from command for build
                cmd = [sys.executable, "-m", "platformio", "run"]
                if environment:
                    cmd.extend(["-e", environment])
            
            self.log(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                self.log("Firmware built successfully!", "SUCCESS")
                self.log_verbose(f"Build output: {result.stdout}")
                return True
            else:
                self.log(f"Build failed: {result.stderr}", "ERROR")
                return False
                
        except subprocess.TimeoutExpired:
            self.log("Build timed out (5 minutes)", "ERROR")
            return False
        except Exception as e:
            self.log(f"Error during build: {e}", "ERROR")
            return False

    def find_built_firmware(self, environment: str = None) -> Dict[str, Path]:
        """Find built firmware files."""
        self.log("Looking for built firmware files...")
        
        # Determine build directory
        if environment:
            build_env_dir = self.build_dir / environment
        else:
            # Find the first available environment directory
            env_dirs = [d for d in self.build_dir.iterdir() if d.is_dir()]
            if not env_dirs:
                self.log("No build directories found", "ERROR")
                return {}
            build_env_dir = env_dirs[0]
            self.log(f"Using build directory: {build_env_dir}")
        
        if not build_env_dir.exists():
            self.log(f"Build directory not found: {build_env_dir}", "ERROR")
            return {}
        
        # Look for firmware files
        firmware_files = {}
        file_patterns = {
            "firmware": "firmware.bin",
            "bootloader": "bootloader.bin", 
            "partitions": "partitions.bin",
            "boot_app0": "boot_app0.bin"
        }
        
        for file_type, pattern in file_patterns.items():
            # Search for the file in the build directory
            found_files = list(build_env_dir.rglob(pattern))
            if found_files:
                firmware_files[file_type] = found_files[0]
                self.log(f"Found {file_type}: {found_files[0]}")
            else:
                self.log(f"Missing {file_type}: {pattern}", "WARNING")
        
        return firmware_files

    def copy_firmware_to_binaries(self, firmware_files: Dict[str, Path], 
                                 version: str = "0.0.1") -> bool:
        """Copy built firmware to binaries directory."""
        self.log(f"Copying firmware to binaries directory (version {version})...")
        
        try:
            # Create version directory
            version_dir = self.firmware_dir / version / "lolin_s2_mini"
            version_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy files
            for file_type, source_path in firmware_files.items():
                dest_path = version_dir / f"{file_type}.bin"
                dest_path.write_bytes(source_path.read_bytes())
                self.log(f"Copied {file_type}: {dest_path}")
            
            # Update firmware list JSON
            self.update_firmware_list(version, firmware_files)
            
            self.log("Firmware copied to binaries directory successfully", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"Error copying firmware: {e}", "ERROR")
            return False

    def update_firmware_list(self, version: str, firmware_files: Dict[str, Path]):
        """Update the firmware list JSON file."""
        firmware_list_file = self.firmware_dir / "firmware-list.json"
        
        try:
            # Load existing data
            if firmware_list_file.exists():
                with open(firmware_list_file, 'r') as f:
                    data = json.load(f)
            else:
                data = {"firmwares": [], "categories": [], "lastUpdated": "", "totalFirmwares": 0}
            
            # Create new firmware entry
            firmware_entry = {
                "id": f"lolin_s2_mini_v{version}",
                "version": f"v{version}",
                "board": "Lolin S2 Mini",
                "size": f"{sum(f.stat().st_size for f in firmware_files.values()) // 1024} KB",
                "date": time.strftime("%Y-%m-%d"),
                "changelog": f"Built from source on {time.strftime('%Y-%m-%d %H:%M:%S')}",
                "category": "Lolin S2 Mini",
                "recommended": True,
                "baudrate": self.default_baudrate,
                "files": {
                    "firmware": {
                        "path": f"{version}/lolin_s2_mini/firmware.bin",
                        "address": self.flash_addresses["firmware"]
                    },
                    "bootloader": {
                        "path": f"{version}/lolin_s2_mini/bootloader.bin",
                        "address": self.flash_addresses["bootloader"]
                    },
                    "partitions": {
                        "path": f"{version}/lolin_s2_mini/partitions.bin",
                        "address": self.flash_addresses["partitions"]
                    },
                    "boot_app0": {
                        "path": f"{version}/lolin_s2_mini/boot_app0.bin",
                        "address": self.flash_addresses["boot_app0"]
                    }
                }
            }
            
            # Remove existing entry with same version
            data["firmwares"] = [fw for fw in data["firmwares"] if fw["version"] != f"v{version}"]
            
            # Add new entry
            data["firmwares"].append(firmware_entry)
            data["lastUpdated"] = time.strftime("%Y-%m-%d")
            data["totalFirmwares"] = len(data["firmwares"])
            
            # Update categories
            if not any(cat["name"] == "Lolin S2 Mini" for cat in data["categories"]):
                data["categories"].append({
                    "name": "Lolin S2 Mini",
                    "description": "Standard BitFloppy board"
                })
            
            # Write updated data
            with open(firmware_list_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            self.log(f"Updated firmware list: {firmware_list_file}")
            
        except Exception as e:
            self.log(f"Error updating firmware list: {e}", "WARNING")

    def update_upload_speed(self, baudrate: int) -> bool:
        """Update upload speed in platformio.ini if different from default."""
        try:
            # Read current platformio.ini
            with open(self.platformio_ini, 'r') as f:
                content = f.read()
            
            # Check if upload_speed is already set
            if 'upload_speed' in content:
                # Update existing upload_speed
                import re
                pattern = r'upload_speed\s*=\s*\d+'
                replacement = f'upload_speed = {baudrate}'
                new_content = re.sub(pattern, replacement, content)
            else:
                # Add upload_speed to the environment section
                lines = content.split('\n')
                new_lines = []
                in_env_section = False
                for line in lines:
                    new_lines.append(line)
                    if line.strip().startswith('[env:') and not in_env_section:
                        in_env_section = True
                    elif in_env_section and line.strip().startswith('[') and not line.strip().startswith('[env:'):
                        # End of environment section, add upload_speed before next section
                        new_lines.insert(-1, f'upload_speed = {baudrate}')
                        in_env_section = False
                    elif in_env_section and line.strip() == '' and new_lines[-2].strip() != '':
                        # Empty line in environment section, add upload_speed
                        new_lines.insert(-1, f'upload_speed = {baudrate}')
                        in_env_section = False
                
                if in_env_section:
                    # Still in environment section, add at the end
                    new_lines.append(f'upload_speed = {baudrate}')
                
                new_content = '\n'.join(new_lines)
            
            # Write updated content
            with open(self.platformio_ini, 'w') as f:
                f.write(new_content)
            
            self.log_verbose(f"Updated upload_speed to {baudrate} in platformio.ini")
            return True
            
        except Exception as e:
            self.log(f"Warning: Could not update upload speed: {e}", "WARNING")
            return False

    def flash_firmware(self, port: str, environment: str = None, 
                      baudrate: int = None) -> bool:
        """Flash firmware using PlatformIO."""
        if baudrate is None:
            baudrate = self.default_baudrate
            
        self.log(f"Flashing firmware to {port} at {baudrate} baud...")
        
        # Update upload speed in platformio.ini if needed
        if baudrate != self.default_baudrate:
            self.update_upload_speed(baudrate)
        
        try:
            cmd = [sys.executable, "-m", "platformio", "run", "--target", "upload"]
            cmd.extend(["--upload-port", port])
            
            if environment:
                cmd.extend(["-e", environment])
            
            self.log_verbose(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                self.log("Firmware flashed successfully!", "SUCCESS")
                self.log_verbose(f"Upload output: {result.stdout}")
                return True
            else:
                self.log(f"Flashing failed: {result.stderr}", "ERROR")
                return False
                
        except subprocess.TimeoutExpired:
            self.log("Flashing timed out (5 minutes)", "ERROR")
            return False
        except Exception as e:
            self.log(f"Error during flashing: {e}", "ERROR")
            return False

    def monitor_serial(self, port: str, baudrate: int = None) -> bool:
        """Open serial monitor."""
        if baudrate is None:
            baudrate = self.default_baudrate
            
        self.log(f"Opening serial monitor on {port} at {baudrate} baud...")
        
        try:
            cmd = [sys.executable, "-m", "platformio", "device", "monitor"]
            cmd.extend(["--port", port])
            cmd.extend(["--baud", str(baudrate)])
            
            self.log_verbose(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, timeout=None)  # No timeout for monitor
            
            return result.returncode == 0
            
        except KeyboardInterrupt:
            self.log("Serial monitor closed by user")
            return True
        except Exception as e:
            self.log(f"Error opening serial monitor: {e}", "ERROR")
            return False

    def interactive_mode(self):
        """Interactive mode for building and flashing."""
        self.log("BitFloppy PlatformIO Interactive Mode")
        self.log("=" * 40)
        
        # Check PlatformIO
        if not self.check_platformio():
            return False
            
        # Check project config
        if not self.check_project_config():
            return False
        
        # List environments
        environments = self.list_environments()
        if not environments:
            self.log("No environments found", "ERROR")
            return False
        
        # Let user select environment
        if len(environments) == 1:
            selected_env = environments[0]
            self.log(f"Using only available environment: {selected_env}")
        else:
            while True:
                try:
                    print("\nAvailable environments:")
                    for i, env in enumerate(environments, 1):
                        print(f"  {i}. {env}")
                    
                    choice = input(f"\nSelect environment (1-{len(environments)}): ").strip()
                    env_index = int(choice) - 1
                    
                    if 0 <= env_index < len(environments):
                        selected_env = environments[env_index]
                        break
                    else:
                        print("Invalid selection. Please try again.")
                except (ValueError, KeyboardInterrupt):
                    print("\nCancelled.")
                    return False
        
        # Ask if user wants to build
        build_choice = input("\nBuild firmware? (y/N): ").strip().lower()
        if build_choice == 'y':
            clean_choice = input("Clean build directory first? (y/N): ").strip().lower()
            clean_build = clean_choice == 'y'
            
            if not self.build_firmware(selected_env, clean_build):
                return False
            
            # Ask if user wants to copy to binaries
            copy_choice = input("Copy built firmware to binaries directory? (y/N): ").strip().lower()
            if copy_choice == 'y':
                firmware_files = self.find_built_firmware(selected_env)
                if firmware_files:
                    version = input("Enter version number (default: 0.0.1): ").strip() or "0.0.1"
                    self.copy_firmware_to_binaries(firmware_files, version)
                else:
                    self.log("No firmware files found to copy", "WARNING")
        
        # Ask if user wants to flash
        flash_choice = input("\nFlash firmware? (y/N): ").strip().lower()
        if flash_choice == 'y':
            # List available ports
            try:
                result = subprocess.run([sys.executable, "-m", "platformio", "device", "list"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"\nAvailable ports:\n{result.stdout}")
                else:
                    print("Could not list ports. Please check your connection.")
            except Exception as e:
                self.log(f"Error listing ports: {e}", "WARNING")
            
            port = input("Enter port (e.g., /dev/ttyUSB0, COM3): ").strip()
            if not port:
                self.log("No port specified", "ERROR")
                return False
            
            baudrate_input = input(f"Enter baudrate (default: {self.default_baudrate}): ").strip()
            baudrate = int(baudrate_input) if baudrate_input else self.default_baudrate
            
            if self.flash_firmware(port, selected_env, baudrate):
                # Ask if user wants to monitor
                monitor_choice = input("Open serial monitor? (y/N): ").strip().lower()
                if monitor_choice == 'y':
                    self.monitor_serial(port, baudrate)
                return True
            else:
                return False
        
        return True

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="BitFloppy PlatformIO Flashing Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 flash_pio.py                    # Interactive mode
  python3 flash_pio.py --build            # Build firmware only
  python3 flash_pio.py --flash --port /dev/ttyUSB0  # Flash only
  python3 flash_pio.py --build --flash --port /dev/ttyUSB0  # Build and flash
  python3 flash_pio.py --list-envs        # List environments
  python3 flash_pio.py --monitor --port /dev/ttyUSB0  # Serial monitor only
  python3 flash_pio.py --install-pio      # Install PlatformIO
        """
    )
    
    parser.add_argument("--build", action="store_true",
                       help="Build firmware")
    parser.add_argument("--flash", action="store_true", 
                       help="Flash firmware")
    parser.add_argument("--monitor", action="store_true",
                       help="Open serial monitor")
    parser.add_argument("--port", "-p",
                       help="Serial port to use")
    parser.add_argument("--environment", "-e",
                       help="PlatformIO environment to use")
    parser.add_argument("--baudrate", "-b", type=int, default=115200,
                       help="Baudrate for flashing/monitoring")
    parser.add_argument("--clean", action="store_true",
                       help="Clean build directory before building")
    parser.add_argument("--list-envs", action="store_true",
                       help="List available environments")
    parser.add_argument("--copy-binaries", action="store_true",
                       help="Copy built firmware to binaries directory")
    parser.add_argument("--version", default="0.0.1",
                       help="Version number for copied firmware")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose output")
    parser.add_argument("--install-pio", action="store_true",
                       help="Install PlatformIO")
    
    args = parser.parse_args()
    
    # Create flasher instance
    flasher = BitFloppyPIOFlasher(verbose=args.verbose)
    
    # Handle install command
    if args.install_pio:
        success = flasher.install_platformio()
        return 0 if success else 1
    
    # Handle list commands
    if args.list_envs:
        flasher.list_environments()
        return 0
    
    # Check PlatformIO
    if not flasher.check_platformio():
        flasher.log("PlatformIO not found. Install with: --install-pio", "ERROR")
        return 1
    
    # Check project config
    if not flasher.check_project_config():
        return 1
    
    # Handle different modes
    if args.build or args.flash or args.monitor:
        # Command mode
        success = True
        
        if args.build:
            success &= flasher.build_firmware(args.environment, args.clean)
            
            if args.copy_binaries and success:
                firmware_files = flasher.find_built_firmware(args.environment)
                if firmware_files:
                    success &= flasher.copy_firmware_to_binaries(firmware_files, args.version)
        
        if args.flash and success:
            if not args.port:
                flasher.log("Port required for flashing", "ERROR")
                return 1
            success &= flasher.flash_firmware(args.port, args.environment, args.baudrate)
        
        if args.monitor and success:
            if not args.port:
                flasher.log("Port required for monitoring", "ERROR")
                return 1
            flasher.monitor_serial(args.port, args.baudrate)
        
        return 0 if success else 1
    else:
        # Interactive mode
        success = flasher.interactive_mode()
        return 0 if success else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
