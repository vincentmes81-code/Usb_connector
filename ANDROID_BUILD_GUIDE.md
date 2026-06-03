# Building USB Connector APK - Complete Guide

## Prerequisites

### System Requirements
- **OS**: Linux, macOS, or Windows (with WSL2)
- **Python**: 3.9 or higher
- **Java**: JDK 11 or later
- **Android SDK**: API level 31
- **Android NDK**: Version 25b or compatible

### Important Notes
- **Linux is recommended** for building APKs
- Windows users should use WSL2 (Windows Subsystem for Linux)
- macOS users need to install Java and Android tools

## Installation Steps

### 1. Install Python Dependencies

```bash
# Install buildozer and required tools
pip install -r requirements_android.txt

# Verify installation
buildozer --version
```

### 2. Install Java Development Kit (JDK)

**On Linux (Debian/Ubuntu):**
```bash
sudo apt-get update
sudo apt-get install openjdk-11-jdk
java -version
```

**On macOS:**
```bash
brew install openjdk@11
sudo ln -sfn /usr/local/opt/openjdk@11/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-11.jdk
```

**On Windows (WSL2):**
```bash
sudo apt-get install openjdk-11-jdk
```

### 3. Download and Setup Android SDK/NDK

**Automated (Recommended):**
Buildozer can download these automatically on first build.

**Manual Setup (Optional):**
```bash
# Set environment variables (add to ~/.bashrc or ~/.zshrc)
export ANDROID_SDK_ROOT=$HOME/Android/Sdk
export ANDROID_NDK_ROOT=$HOME/Android/Sdk/ndk/25.1.8937393

# Create directories if needed
mkdir -p $ANDROID_SDK_ROOT
```

## Building the APK

### Step 1: Prepare the Project

```bash
# Navigate to project directory
cd Usb_connector

# Verify buildozer.spec exists
ls buildozer.spec
```

### Step 2: Build APK (Debug Mode)

```bash
# First build (will download SDK/NDK)
buildozer android debug

# Subsequent builds
buildozer android debug --no-update
```

**First build may take 15-45 minutes** depending on internet speed and system.

### Step 3: Build APK (Release Mode)

```bash
buildozer android release
```

## Output Location

After successful build, the APK will be located at:
```
bin/usbconnector-1.0-debug.apk      # Debug version
bin/usbconnector-1.0-release.apk    # Release version
```

## Troubleshooting

### Issue: "Java not found"
```bash
# Find Java installation
which java
# Set JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

### Issue: "Android SDK not found"
```bash
# Buildozer will download automatically
# Or set manually:
export ANDROID_SDK_ROOT=$HOME/Android/Sdk
```

### Issue: "NDK not found"
```bash
# Update buildozer.spec:
android.ndk = 25.1.8937393
# Buildozer will download this version
```

### Issue: Build fails with "Out of memory"
```bash
# Increase Java heap size
export JAVA_TOOL_OPTIONS="-Xmx4096m"
buildozer android debug
```

### Issue: "Permission denied" on Linux
```bash
# Give execute permissions
chmod +x buildozer
```

### Clearing Build Cache

```bash
# Clean old builds
buildozer android clean

# Remove all artifacts
rm -rf .buildozer bin/
```

## Installing on Android Device

### Via USB (Debugging)

```bash
# Enable USB debugging on your Android device
# Connect device via USB

# Install APK
adb install bin/usbconnector-1.0-debug.apk

# Launch app
adb shell am start -n org.vincentmes.usbconnector/.USBConnectorApp
```

### Via APK File

1. Transfer `bin/usbconnector-1.0-debug.apk` to your Android device
2. Open file manager
3. Tap the APK file
4. Allow installation from unknown sources if prompted
5. Tap "Install"

## Features Available on Android

✅ **List USB Devices** - View all connected USB peripherals  
✅ **Device Details** - See detailed specs for each device  
✅ **Real-time Monitoring** - Monitor device connections/disconnections  
⚠️ **USB Access** - Limited on Android (requires OTG cable and compatible device)

## Limitations on Android

- Direct USB device access requires **USB Host OTG (On-The-Go)** support
- Not all Android devices support USB Host mode
- Some USB information may not be accessible due to Android security restrictions
- `pyusb` availability depends on device and Python runtime

## Next Steps

1. **For Testing**: Use debug APK first
2. **For Release**: Build release APK after testing
3. **Code Signing**: Release APK needs signing (see Google Play docs)
4. **App Optimization**: Consider reducing APK size by removing unused features

## Additional Resources

- [Kivy Documentation](https://kivy.org/doc/current/)
- [Buildozer Documentation](https://buildozer.readthedocs.io/)
- [Android USB Host API](https://developer.android.com/guide/topics/connectivity/usb/host)
- [Python for Android](https://github.com/kivy/python-for-android)

## Support

If you encounter issues:
1. Check the build log: `buildozer android debug 2>&1 | tee build.log`
2. Ensure all prerequisites are installed
3. Try cleaning and rebuilding: `buildozer android clean`
4. Check Kivy and Buildozer GitHub issues for similar problems
