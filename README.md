# USB Connector Info App

A Python application that detects USB devices (particularly USB-C cables) and displays detailed information about them when plugged in.

## Features

- **Real-time USB device detection** - Automatically detects when USB devices are connected/disconnected
- **USB-C specific information** - Displays cable specifications, power delivery capabilities, data transfer speeds
- **Comprehensive device details** - Vendor ID, Product ID, Serial Number, Manufacturer, Product description
- **Monitor Mode** - Continuous monitoring of USB bus for device changes
- **Multi-platform support** - Works on Windows, macOS, and Linux

## Requirements

- Python 3.7+
- `pyusb` - PyUSB library for USB device access
- `libusb` - Native USB library

## Installation

1. Clone the repository:
```bash
git clone https://github.com/vincentmes81-code/Usb_connector.git
cd Usb_connector
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install libusb (platform-specific):
   - **Windows**: Download from https://github.com/libusb/libusb/releases
   - **macOS**: `brew install libusb`
   - **Linux**: `sudo apt-get install libusb-1.0-0` (Debian/Ubuntu)

## Usage

### Run the app:
```bash
python main.py
```

### Options:
- **`l`** - List all connected USB devices
- **`m`** - Enter monitoring mode (real-time USB change detection)
- **`q`** - Quit the application

## How it Works

The app uses the PyUSB library to:
1. Enumerate all USB devices connected to the system
2. Extract detailed information from USB descriptors
3. Monitor for device connection/disconnection events
4. Display comprehensive cable and device specifications

## Output Example

When a USB device is detected, you'll see:

```
============================================================
USB DEVICE DETECTED
============================================================
Product:              USB-C Cable
Manufacturer:         Example Corp
Serial Number:        ABC123XYZ
────────────────────────────────────────────────────────────
Vendor ID:            0x1234
Product ID:           0x5678
Bus Number:           1
Device Number:        2
────────────────────────────────────────────────────────────
Device Class:         0 (Miscellaneous)
Device Subclass:      0x00
Device Protocol:      0x00
USB Spec Version:     0x0200
Device Version:       0x0100
────────────────────────────────────────────────────────────
USB Speed:            USB 2.0 (High Speed)
Max Power:            500mA
Configurations:       1
============================================================
```

## Supported Information

The app displays the following information for each USB device:

- **Basic Info**: Product name, manufacturer, serial number
- **Identifiers**: Vendor ID, Product ID, Bus number, Device number
- **Specifications**: Device class, subclass, protocol
- **Power**: Maximum power consumption
- **Speed**: USB version and speed rating
- **Configuration**: Number of configurations available

## License

MIT

## Author

vincentmes81-code
