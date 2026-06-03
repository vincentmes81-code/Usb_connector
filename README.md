# USB-C Cable Inspector — Android App

Detects and displays capabilities of any USB-C cable plugged into your Android phone.

## What It Shows

| Category | Details |
|---|---|
| **Device Identity** | Manufacturer, product name, vendor/product ID, serial |
| **USB Standard** | USB 2.0 / 3.0 / 3.1 / USB4, max speed |
| **Interfaces** | Function classes (audio, storage, HID, etc.) |
| **Power & Charging** | Current (mA), voltage (mV), estimated wattage, charge type |
| **Sysfs Data** | Kernel-level speed, bcdUSB version, bMaxPower |
| **Alternate Modes** | DisplayPort, USB4/Thunderbolt, MHL detection |
| **Cable Analysis** | Grade inference, e-marker detection, quality notes |

## ⚠️ Important Limitation

**Plugging into a charger only** = limited info (charging data only).  
**Plug into a computer or USB OTG hub** = full USB device info.

This is a fundamental Android/USB limitation — cable e-marker chips are only 
readable during USB PD negotiation at the hardware level, not by apps.

## Setup

### Requirements
- Android Studio Hedgehog or newer
- Android phone running API 26+ (Android 8.0+)
- A USB-C OTG cable or adapter (to connect to a PC/hub for full data)

### Steps

1. **Open in Android Studio:**
   File → Open → select the `USBCableInspector` folder

2. **Sync Gradle** (Android Studio will prompt automatically)

3. **Run on your device:**
   - Enable Developer Options on your phone
   - Enable USB Debugging
   - Connect phone to PC, select "Run" in Android Studio

4. **Test it:**
   - Plug in any USB-C cable (to a hub, accessory, or computer via OTG adapter)
   - The app auto-launches and displays all detected info
   - Or tap "SCAN NOW" at any time

## How It Works

- **`UsbManager`** — Android's USB host API, enumerates connected devices
- **`BatteryManager`** — reads real-time current, voltage, charge status
- **`/sys/class/typec`** — Linux sysfs, checks for alt mode entries (DP, USB4)
- **`/sys/bus/usb/devices/`** — sysfs USB device tree for speed, version, power
- **Broadcast receivers** — auto-detects plug/unplug events in real time

## File Structure

```
app/src/main/
├── java/com/usbinspector/
│   └── MainActivity.kt       ← All logic here
├── res/
│   ├── layout/activity_main.xml
│   ├── values/{colors, strings, themes}.xml
│   ├── drawable/card_bg.xml
│   └── xml/device_filter.xml
└── AndroidManifest.xml
```
