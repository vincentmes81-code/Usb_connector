"""
USB Connector Information App
Detects USB devices and displays detailed information
"""

import usb.core
import usb.util
import sys
import time
from typing import List, Dict, Optional


class USBConnectorApp:
    """Main application for monitoring and displaying USB device information"""
    
    def __init__(self):
        self.previous_devices = set()
        
    def get_usb_devices(self) -> List[Dict]:
        """Get all connected USB devices"""
        devices = []
        
        try:
            for device in usb.core.find(find_all=True):
                device_info = self.get_device_info(device)
                devices.append(device_info)
        except usb.core.USBError as e:
            print(f"USB Error: {e}")
            
        return devices
    
    def get_device_info(self, device) -> Dict:
        """Extract detailed information from a USB device"""
        try:
            # Get manufacturer string
            manufacturer = self.get_string(device, device.iManufacturer)
        except (usb.core.USBError, IndexError):
            manufacturer = "Unknown"
        
        try:
            # Get product string
            product = self.get_string(device, device.iProduct)
        except (usb.core.USBError, IndexError):
            product = "Unknown Device"
        
        try:
            # Get serial number
            serial = self.get_string(device, device.iSerialNumber)
        except (usb.core.USBError, IndexError):
            serial = "N/A"
        
        # Calculate max power
        max_power = "Unknown"
        if device.bMaxPower:
            max_power = f"{device.bMaxPower * 2}mA"
        
        # Determine USB speed
        usb_speed = self.get_usb_speed(device)
        
        # Get device class info
        device_class = self.get_device_class_name(device.bDeviceClass)
        
        return {
            'vendor_id': hex(device.idVendor),
            'product_id': hex(device.idProduct),
            'manufacturer': manufacturer,
            'product': product,
            'serial_number': serial,
            'bus_number': device.bus,
            'device_number': device.address,
            'device_class': f"{device.bDeviceClass} ({device_class})",
            'device_subclass': device.bDeviceSubClass,
            'device_protocol': device.bDeviceProtocol,
            'max_power': max_power,
            'usb_speed': usb_speed,
            'bcd_device': device.bcdDevice,
            'bcd_usb': device.bcdUSB,
            'num_configurations': device.bNumConfigurations,
            'unique_id': f"{device.idVendor}:{device.idProduct}:{serial}"
        }
    
    def get_string(self, device, string_index: int) -> str:
        """Get string descriptor from device"""
        if string_index == 0:
            return ""
        try:
            return usb.util.get_string(device, string_index)
        except (usb.core.USBError, ValueError):
            return "N/A"
    
    def get_usb_speed(self, device) -> str:
        """Determine USB speed based on device"""
        bcd_usb = device.bcdUSB
        major_version = (bcd_usb >> 8) & 0xFF
        minor_version = bcd_usb & 0xFF
        
        speed_map = {
            0x01: "USB 1.0 (Low Speed)",
            0x10: "USB 1.1",
            0x20: "USB 2.0 (High Speed)",
            0x30: "USB 3.0 (SuperSpeed)",
            0x31: "USB 3.1",
        }
        
        return speed_map.get(bcd_usb, f"USB {major_version}.{minor_version}")
    
    def get_device_class_name(self, class_code: int) -> str:
        """Convert device class code to human readable name"""
        class_names = {
            0x00: "Miscellaneous",
            0x01: "Audio",
            0x02: "Communications",
            0x03: "HID (Human Interface Device)",
            0x04: "Reserved",
            0x05: "Physical",
            0x06: "Still Image",
            0x07: "Printer",
            0x08: "Mass Storage",
            0x09: "Hub",
            0x0A: "CDC Data",
            0x0B: "Chip/Smart Card",
            0x0D: "Content Security",
            0x0E: "Video",
            0x0F: "Personal Healthcare",
            0x10: "Audio/Video",
            0xDC: "Diagnostic Device",
            0xE0: "Wireless Controller",
            0xEF: "Miscellaneous",
            0xFE: "Application Specific",
            0xFF: "Vendor Specific"
        }
        return class_names.get(class_code, "Unknown")
    
    def print_device_info(self, device_info: Dict):
        """Pretty print device information"""
        print("\n" + "="*60)
        print("USB DEVICE DETECTED")
        print("="*60)
        print(f"Product:              {device_info['product']}")
        print(f"Manufacturer:         {device_info['manufacturer']}")
        print(f"Serial Number:        {device_info['serial_number']}")
        print("-"*60)
        print(f"Vendor ID:            {device_info['vendor_id']}")
        print(f"Product ID:           {device_info['product_id']}")
        print(f"Bus Number:           {device_info['bus_number']}")
        print(f"Device Number:        {device_info['device_number']}")
        print("-"*60)
        print(f"Device Class:         {device_info['device_class']}")
        print(f"Device Subclass:      0x{device_info['device_subclass']:02X}")
        print(f"Device Protocol:      0x{device_info['device_protocol']:02X}")
        print(f"USB Spec Version:     0x{device_info['bcd_usb']:04X}")
        print(f"Device Version:       0x{device_info['bcd_device']:04X}")
        print("-"*60)
        print(f"USB Speed:            {device_info['usb_speed']}")
        print(f"Max Power:            {device_info['max_power']}")
        print(f"Configurations:       {device_info['num_configurations']}")
        print("="*60 + "\n")
    
    def list_all_devices(self):
        """List all connected USB devices"""
        devices = self.get_usb_devices()
        
        if not devices:
            print("\nNo USB devices found.\n")
            return
        
        print(f"\n{len(devices)} USB device(s) found:\n")
        for i, device in enumerate(devices, 1):
            print(f"{i}. {device['product']} ({device['manufacturer']})")
            print(f"   Vendor ID: {device['vendor_id']}, Product ID: {device['product_id']}")
            print()
    
    def monitor_devices(self):
        """Monitor USB devices for connections/disconnections"""
        print("\nMonitoring USB devices (Press Ctrl+C to stop)...\n")
        
        try:
            while True:
                devices = self.get_usb_devices()
                current_devices = {d['unique_id'] for d in devices}
                
                # Check for new devices
                new_devices = current_devices - self.previous_devices
                if new_devices:
                    for device in devices:
                        if device['unique_id'] in new_devices:
                            print("\n[NEW DEVICE CONNECTED]")
                            self.print_device_info(device)
                
                # Check for disconnected devices
                disconnected = self.previous_devices - current_devices
                if disconnected:
                    print("[DEVICE DISCONNECTED]")
                    for device_id in disconnected:
                        print(f"Device: {device_id}\n")
                
                self.previous_devices = current_devices
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped.")
    
    def run(self):
        """Main application loop"""
        print("\n" + "="*60)
        print("USB CONNECTOR INFORMATION APP")
        print("="*60)
        print("Commands:")
        print("  l - List all USB devices")
        print("  m - Monitor USB devices (real-time)")
        print("  q - Quit")
        print("="*60 + "\n")
        
        while True:
            try:
                cmd = input("Enter command (l/m/q): ").lower().strip()
                
                if cmd == 'l':
                    self.list_all_devices()
                elif cmd == 'm':
                    self.monitor_devices()
                elif cmd == 'q':
                    print("\nGoodbye!\n")
                    break
                else:
                    print("Invalid command. Please enter l, m, or q.\n")
                    
            except KeyboardInterrupt:
                print("\n\nGoodbye!\n")
                break
            except Exception as e:
                print(f"Error: {e}\n")


if __name__ == "__main__":
    app = USBConnectorApp()
    app.run()
