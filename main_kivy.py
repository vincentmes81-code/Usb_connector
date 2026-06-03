"""
USB Connector Information App - Kivy GUI Version
Detects USB devices and displays detailed information
Compatible with Android and Desktop
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.rst import RstDocument
import threading
import time

# Try to import pyusb for desktop, use fallback for Android
try:
    import usb.core
    import usb.util
    PYUSB_AVAILABLE = True
except ImportError:
    PYUSB_AVAILABLE = False

Window.size = (400, 800)


class USBConnectorLogic:
    """Logic for USB device detection"""
    
    def __init__(self):
        self.previous_devices = set()
        
    def get_usb_devices(self):
        """Get all connected USB devices"""
        if not PYUSB_AVAILABLE:
            return []
            
        devices = []
        try:
            for device in usb.core.find(find_all=True):
                device_info = self.get_device_info(device)
                devices.append(device_info)
        except Exception as e:
            print(f"USB Error: {e}")
            
        return devices
    
    def get_device_info(self, device):
        """Extract detailed information from a USB device"""
        try:
            manufacturer = self.get_string(device, device.iManufacturer)
        except:
            manufacturer = "Unknown"
        
        try:
            product = self.get_string(device, device.iProduct)
        except:
            product = "Unknown Device"
        
        try:
            serial = self.get_string(device, device.iSerialNumber)
        except:
            serial = "N/A"
        
        max_power = "Unknown"
        if device.bMaxPower:
            max_power = f"{device.bMaxPower * 2}mA"
        
        usb_speed = self.get_usb_speed(device)
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
    
    def get_string(self, device, string_index):
        """Get string descriptor from device"""
        if string_index == 0:
            return ""
        try:
            return usb.util.get_string(device, string_index)
        except:
            return "N/A"
    
    def get_usb_speed(self, device):
        """Determine USB speed based on device"""
        bcd_usb = device.bcdUSB
        
        speed_map = {
            0x0100: "USB 1.0 (Low Speed)",
            0x0110: "USB 1.1",
            0x0200: "USB 2.0 (High Speed)",
            0x0300: "USB 3.0 (SuperSpeed)",
            0x0310: "USB 3.1",
        }
        
        return speed_map.get(bcd_usb, f"USB {(bcd_usb >> 8) & 0xFF}.{bcd_usb & 0xFF}")
    
    def get_device_class_name(self, class_code):
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


class USBConnectorApp(App):
    """Main Kivy Application"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.usb_logic = USBConnectorLogic()
        self.monitoring = False
        self.monitor_thread = None
        self.current_devices = []
        
    def build(self):
        """Build the UI"""
        self.title = "USB Connector Info"
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text="[b]USB Connector[/b]\nDevice Information",
            markup=True,
            size_hint_y=0.1,
            font_size='20sp'
        )
        main_layout.add_widget(header)
        
        # Buttons layout
        button_layout = BoxLayout(size_hint_y=0.15, spacing=10)
        
        list_btn = Button(text="List Devices", background_color=(0.2, 0.6, 0.2, 1))
        list_btn.bind(on_press=self.show_devices)
        button_layout.add_widget(list_btn)
        
        monitor_btn = Button(text="Monitor", background_color=(0.2, 0.4, 0.8, 1))
        monitor_btn.bind(on_press=self.toggle_monitor)
        button_layout.add_widget(monitor_btn)
        self.monitor_btn = monitor_btn
        
        main_layout.add_widget(button_layout)
        
        # Devices list display
        scroll = ScrollView()
        self.devices_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.devices_layout.bind(minimum_height=self.devices_layout.setter('height'))
        scroll.add_widget(self.devices_layout)
        main_layout.add_widget(scroll)
        
        # Status label
        self.status_label = Label(
            text="Ready",
            size_hint_y=0.1,
            color=(0.2, 0.8, 0.2, 1)
        )
        main_layout.add_widget(self.status_label)
        
        # Start refresh
        Clock.schedule_interval(self.refresh_ui, 2)
        
        if not PYUSB_AVAILABLE:
            self.status_label.text = "PyUSB not available on Android"
            self.status_label.color = (1, 0.5, 0, 1)
        
        return main_layout
    
    def show_devices(self, instance):
        """Display list of USB devices"""
        self.devices_layout.clear_widgets()
        self.current_devices = self.usb_logic.get_usb_devices()
        
        if not self.current_devices:
            label = Label(
                text="No USB devices found",
                size_hint_y=None,
                height=50,
                color=(1, 0, 0, 1)
            )
            self.devices_layout.add_widget(label)
            self.status_label.text = "No devices found"
            return
        
        self.status_label.text = f"Found {len(self.current_devices)} device(s)"
        
        for device in self.current_devices:
            self.add_device_widget(device)
    
    def add_device_widget(self, device):
        """Add a device to the display"""
        device_btn = Button(
            text=f"[b]{device['product']}[/b]\n{device['manufacturer']}\n{device['vendor_id']}:{device['product_id']}",
            markup=True,
            size_hint_y=None,
            height=100,
            background_color=(0.3, 0.3, 0.3, 1)
        )
        device_btn.bind(on_press=lambda x: self.show_device_details(device))
        self.devices_layout.add_widget(device_btn)
    
    def show_device_details(self, device):
        """Show detailed information about a device in a popup"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        details_text = f"""
[b]Device Details[/b]

Product: {device['product']}
Manufacturer: {device['manufacturer']}
Serial: {device['serial_number']}

Vendor ID: {device['vendor_id']}
Product ID: {device['product_id']}
Bus: {device['bus_number']}
Address: {device['device_number']}

Class: {device['device_class']}
Subclass: 0x{device['device_subclass']:02X}
Protocol: 0x{device['device_protocol']:02X}

USB Speed: {device['usb_speed']}
Max Power: {device['max_power']}
Configurations: {device['num_configurations']}
        """
        
        scroll = ScrollView()
        label = Label(
            text=details_text,
            markup=True,
            size_hint_y=None
        )
        label.bind(texture_size=label.setter('size'))
        scroll.add_widget(label)
        content.add_widget(scroll)
        
        close_btn = Button(text="Close", size_hint_y=0.2, background_color=(0.8, 0.2, 0.2, 1))
        content.add_widget(close_btn)
        
        popup = Popup(title='Device Information', content=content, size_hint=(0.9, 0.9))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def toggle_monitor(self, instance):
        """Toggle monitoring mode"""
        if self.monitoring:
            self.monitoring = False
            instance.background_color = (0.2, 0.4, 0.8, 1)
            instance.text = "Monitor"
            self.status_label.text = "Monitoring stopped"
        else:
            self.monitoring = True
            instance.background_color = (0.8, 0.2, 0.2, 1)
            instance.text = "Stop Monitor"
            self.status_label.text = "Monitoring..."
            self.monitor_thread = threading.Thread(target=self.monitor_devices_thread, daemon=True)
            self.monitor_thread.start()
    
    def monitor_devices_thread(self):
        """Monitor devices in background thread"""
        previous_devices = set()
        
        while self.monitoring:
            try:
                devices = self.usb_logic.get_usb_devices()
                current_devices = {d['unique_id'] for d in devices}
                
                new_devices = current_devices - previous_devices
                if new_devices:
                    Clock.schedule_once(lambda dt: self.on_device_connected(devices, new_devices), 0)
                
                disconnected = previous_devices - current_devices
                if disconnected:
                    Clock.schedule_once(lambda dt: self.on_device_disconnected(disconnected), 0)
                
                previous_devices = current_devices
                time.sleep(1)
            except Exception as e:
                print(f"Monitor error: {e}")
                time.sleep(1)
    
    def on_device_connected(self, devices, new_device_ids):
        """Handle device connection"""
        for device in devices:
            if device['unique_id'] in new_device_ids:
                self.status_label.text = f"[b]NEW: {device['product']}[/b]"
                self.status_label.color = (0, 1, 0, 1)
    
    def on_device_disconnected(self, device_ids):
        """Handle device disconnection"""
        self.status_label.text = "[b]Device disconnected[/b]"
        self.status_label.color = (1, 1, 0, 1)
    
    def refresh_ui(self, dt):
        """Refresh UI periodically"""
        if not self.monitoring:
            return


if __name__ == '__main__':
    app = USBConnectorApp()
    app.run()
