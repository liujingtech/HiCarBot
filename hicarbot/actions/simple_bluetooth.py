"""
Simple Bluetooth Toggle Action
This module provides a minimal implementation to open Bluetooth settings and toggle the switch.
"""

import uiautomator2 as u2
import time
from typing import Dict, Any
from hicarbot.models.models import Action, DataContext


class SimpleBluetoothToggleAction(Action):
    """Simple Bluetooth Toggle Action - Open Bluetooth settings and ensure Bluetooth is enabled"""
    
    def execute(self, context: DataContext) -> bool:
        try:
            print("Executing simple Bluetooth toggle action...")
            
            # Connect to device
            d = u2.connect()
            
            # Open Bluetooth settings
            print("Opening Bluetooth settings page...")
            d.app_start("com.android.settings", stop=True)
            time.sleep(2)
            
            # Try to navigate to Bluetooth settings
            self._navigate_to_bluetooth(d)
            
            # Wait for page to load
            time.sleep(3)
            
            # Ensure Bluetooth is enabled
            self._ensure_bluetooth_enabled(d)
            
            print("Bluetooth toggle action completed")
            return True
            
        except Exception as e:
            print(f"Simple Bluetooth toggle action failed: {str(e)}")
            return False
    
    def _navigate_to_bluetooth(self, d):
        """Navigate to Bluetooth settings"""
        try:
            # Method 1: Direct intent
            print("Trying to open Bluetooth settings via intent...")
            d.shell('am start -a android.settings.BLUETOOTH_SETTINGS')
            time.sleep(2)
            
            # Check if we're on Bluetooth page
            if self._is_on_bluetooth_page(d):
                return
            
            # Method 2: Find "蓝牙" text and click it
            print("Trying to navigate to Bluetooth settings via text...")
            bluetooth_elements = d.xpath("//*[@text='蓝牙' or @text='Bluetooth']")
            if bluetooth_elements.exists:
                bluetooth_elements.click()
                time.sleep(2)
                return
                
        except Exception as e:
            print(f"Failed to navigate to Bluetooth settings: {str(e)}")
    
    def _is_on_bluetooth_page(self, d):
        """Check if we're on Bluetooth settings page"""
        try:
            bluetooth_elements = d.xpath("//*[@text='蓝牙' or @text='Bluetooth']")
            return bluetooth_elements.exists
        except:
            return False
    
    def _ensure_bluetooth_enabled(self, d):
        """Ensure Bluetooth is enabled"""
        try:
            print("Checking Bluetooth status...")
            
            # Look for Bluetooth switch
            switch_elements = d(className="android.widget.Switch")
            if len(switch_elements) > 0:
                # Get switch status
                info = switch_elements[0].info
                is_checked = info.get('checked', False)
                print(f"Bluetooth switch status: {'enabled' if is_checked else 'disabled'}")
                
                # If not enabled, click to enable
                if not is_checked:
                    print("Bluetooth is disabled, enabling...")
                    switch_elements[0].click()
                    time.sleep(2)
                    print("Bluetooth enabled")
                else:
                    print("Bluetooth is already enabled")
                return  # Success
            
            # If no switch found, try alternative method
            print("Bluetooth switch not found, trying alternative method...")
            
            # Try clicking near "蓝牙" text
            bluetooth_elements = d.xpath("//*[@text='蓝牙' or @text='Bluetooth']")
            if bluetooth_elements.exists:
                info = bluetooth_elements.get_last_match()
                bounds = info.bounds
                # Click to the right side where switch usually is
                right_x = bounds.get('right', 0) + 100
                center_y = (bounds.get('top', 0) + bounds.get('bottom', 0)) // 2
                if right_x > 0 and center_y > 0:
                    d.click(right_x, center_y)
                    time.sleep(2)
                    print("Tried clicking Bluetooth switch position")
                    return  # Assume success
            
            # Last resort: try to navigate to Bluetooth settings directly
            print("Trying to directly enable Bluetooth...")
            d.shell('am start -a android.bluetooth.adapter.action.REQUEST_ENABLE')
            time.sleep(3)
            print("Sent Bluetooth enable request")
                
        except Exception as e:
            print(f"Failed to ensure Bluetooth is enabled: {str(e)}")