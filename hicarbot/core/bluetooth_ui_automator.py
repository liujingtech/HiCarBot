"""
Bluetooth status detection using uiautomator2
"""

import uiautomator2 as u2
import time
import os
from typing import Dict, Any, Optional
from core.models import Action, DataContext


class CheckBluetoothStatusWithUIAction(Action):
    """Check Bluetooth Status using UI Automator"""
    
    def execute(self, context: DataContext) -> bool:
        try:
            print("正在使用UI Automator检测蓝牙状态...")
            
            # Connect to device
            d = u2.connect()
            
            # Open Bluetooth settings
            print("正在打开蓝牙设置页面...")
            d.app_start("com.android.settings", stop=True)
            # Wait for app to start
            time.sleep(2)
            
            # Try to navigate to Bluetooth settings
            self._navigate_to_bluetooth_settings(d)
            
            # Wait for page to load
            time.sleep(3)
            
            # Check Bluetooth status
            is_enabled = self._check_bluetooth_status(d)
            
            # Save result to context
            context.set_variable('bluetooth_status', is_enabled)
            context.set_variable('is_bluetooth_enabled', is_enabled)
            print(f"蓝牙状态 (UI Automator): {'开启' if is_enabled else '关闭'}")
            
            return True
            
        except Exception as e:
            print(f"使用UI Automator检测蓝牙状态失败: {str(e)}")
            # Set default value
            context.set_variable('bluetooth_status', False)
            context.set_variable('is_bluetooth_enabled', False)
            return True
    
    def _navigate_to_bluetooth_settings(self, d):
        """Navigate to Bluetooth settings page"""
        try:
            # Try different methods to open Bluetooth settings
            
            # Method 1: Direct intent
            print("尝试通过intent打开蓝牙设置...")
            d.shell('am start -a android.settings.BLUETOOTH_SETTINGS')
            time.sleep(2)
            
            # Check if we're on Bluetooth settings page
            if self._is_on_bluetooth_page(d):
                return
            
            # Method 2: Navigate through Settings app
            print("尝试通过设置应用导航到蓝牙设置...")
            # Look for "蓝牙" or "Bluetooth" text
            bluetooth_elements = d.xpath("//*[@text='蓝牙' or @text='Bluetooth']")
            if bluetooth_elements.exists:
                bluetooth_elements.click()
                time.sleep(2)
                return
            
            # Method 3: Search for Bluetooth in settings
            print("尝试在设置中搜索蓝牙...")
            search_elements = d.xpath("//*[@text='搜索' or @text='Search']")
            if search_elements.exists:
                search_elements.click()
                time.sleep(1)
                # Input "蓝牙" in search box
                search_boxes = d.xpath("//android.widget.EditText")
                if search_boxes.exists:
                    search_boxes.set_text("蓝牙")
                    time.sleep(1)
                    # Click search result
                    result_elements = d.xpath("//*[@text='蓝牙']")
                    if result_elements.exists:
                        result_elements.click()
                        time.sleep(2)
                        return
            
        except Exception as e:
            print(f"导航到蓝牙设置页面失败: {str(e)}")
    
    def _is_on_bluetooth_page(self, d) -> bool:
        """Check if we're on Bluetooth settings page"""
        try:
            # Look for Bluetooth-related elements
            bluetooth_elements = d.xpath("//*[@text='蓝牙' or @text='Bluetooth']")
            return bluetooth_elements.exists
        except:
            return False
    
    def _check_bluetooth_status(self, d) -> bool:
        """Check Bluetooth status using UI elements"""
        try:
            # Method 1: Look for switch elements
            print("正在查找蓝牙开关...")
            # Look for Bluetooth switch specifically
            # Try to find switch near "蓝牙" text
            bluetooth_text = d.xpath("//*[@text='蓝牙' or @text='Bluetooth']")
            if bluetooth_text.exists:
                # For now, we'll just check if we can find any switch
                switch_elements = d(className="android.widget.Switch")
                if len(switch_elements) > 0:
                    # Check if first switch is checked (enabled)
                    try:
                        info = switch_elements[0].info
                        is_checked = info.get('checked', False)
                        print(f"找到蓝牙开关，状态: {'开启' if is_checked else '关闭'}")
                        return is_checked
                    except:
                        pass
            
            # Method 2: Look for any switch elements and check if they're related to Bluetooth
            switch_elements = d(className="android.widget.Switch")
            for switch in switch_elements:
                # Check if this switch is in the upper part of screen and likely Bluetooth switch
                try:
                    info = switch.info
                    bounds = info.get('bounds', {})
                    if bounds.get('top', 0) < 500:  # Likely in header area
                        is_checked = info.get('checked', False)
                        print(f"找到顶部开关，状态: {'开启' if is_checked else '关闭'}")
                        return is_checked
                except:
                    continue
            
            # Method 3: Look for status text
            print("通过文本查找蓝牙状态...")
            status_elements = d.xpath("//*[@text='开启' or @text='关闭' or @text='ON' or @text='OFF']")
            if status_elements.exists:
                try:
                    info = status_elements.get_last_match()
                    text = info.get('text', '').upper()
                    if '开启' in text or 'ON' in text:
                        print("检测到蓝牙已开启")
                        return True
                    elif '关闭' in text or 'OFF' in text:
                        print("检测到蓝牙已关闭")
                        return False
                except:
                    pass
            
            # Method 4: Look for Bluetooth device list (indicates Bluetooth is on)
            print("通过设备列表查找蓝牙状态...")
            device_elements = d.xpath("//*[@text='已配对设备' or @text='Paired devices' or @text='可用设备' or @text='Available devices']")
            if device_elements.exists:
                print("检测到蓝牙设备列表，蓝牙已开启")
                return True
            
            print("无法确定蓝牙状态，默认为关闭")
            return False
            
        except Exception as e:
            print(f"检查蓝牙状态失败: {str(e)}")
            return False


class ToggleBluetoothWithUIAction(Action):
    """Toggle Bluetooth using UI Automator"""
    
    def execute(self, context: DataContext) -> bool:
        try:
            print("正在使用UI Automator切换蓝牙状态...")
            
            # Connect to device
            d = u2.connect()
            
            # Open Bluetooth settings
            print("正在打开蓝牙设置页面...")
            d.app_start("com.android.settings", stop=True)
            # Wait for app to start
            time.sleep(2)
            
            # Navigate to Bluetooth settings
            self._navigate_to_bluetooth_settings(d)
            
            # Wait for page to load
            time.sleep(3)
            
            # Find and click Bluetooth switch
            success = self._toggle_bluetooth_switch(d)
            
            if success:
                print("蓝牙开关已切换")
                return True
            else:
                print("切换蓝牙开关失败")
                return False
                
        except Exception as e:
            print(f"使用UI Automator切换蓝牙状态失败: {str(e)}")
            return False
    
    def _navigate_to_bluetooth_settings(self, d):
        """Navigate to Bluetooth settings page"""
        try:
            # Try different methods to open Bluetooth settings
            
            # Method 1: Direct intent
            print("尝试通过intent打开蓝牙设置...")
            d.shell('am start -a android.settings.BLUETOOTH_SETTINGS')
            time.sleep(2)
            
            # Check if we're on Bluetooth settings page
            if self._is_on_bluetooth_page(d):
                return
            
            # Method 2: Navigate through Settings app
            print("尝试通过设置应用导航到蓝牙设置...")
            # Look for "蓝牙" or "Bluetooth" text
            bluetooth_elements = d.xpath("//*[@text='蓝牙' or @text='Bluetooth']")
            if bluetooth_elements.exists:
                bluetooth_elements.click()
                time.sleep(2)
                return
            
        except Exception as e:
            print(f"导航到蓝牙设置页面失败: {str(e)}")
    
    def _is_on_bluetooth_page(self, d) -> bool:
        """Check if we're on Bluetooth settings page"""
        try:
            # Look for Bluetooth-related elements
            bluetooth_elements = d.xpath("//*[@text='蓝牙' or @text='Bluetooth']")
            return bluetooth_elements.exists
        except:
            return False
    
    def _toggle_bluetooth_switch(self, d) -> bool:
        """Find and toggle Bluetooth switch"""
        try:
            print("正在查找蓝牙开关...")
            # Look for Bluetooth switch specifically
            # Try to find switch near "蓝牙" text
            bluetooth_text = d.xpath("//*[@text='蓝牙' or @text='Bluetooth']")
            if bluetooth_text.exists:
                # Look for a switch in the same area
                switch_elements = d(className="android.widget.Switch")
                if len(switch_elements) > 0:
                    print("找到蓝牙开关，正在切换...")
                    # Click the first switch
                    switch_elements[0].click()
                    time.sleep(1)
                    return True
            
            # If we can't find the switch, try to find it by position
            print("通过位置查找蓝牙开关...")
            # Look for "蓝牙" text and click nearby area
            bluetooth_elements = d.xpath("//*[@text='蓝牙' or @text='Bluetooth']")
            if bluetooth_elements.exists:
                # Get element bounds
                try:
                    info = bluetooth_elements.get_last_match()
                    bounds = info.bounds
                    # Click to the right of the text (where switch usually is)
                    right_x = bounds.get('right', 0) + 100
                    center_y = (bounds.get('top', 0) + bounds.get('bottom', 0)) // 2
                    if right_x > 0 and center_y > 0:
                        d.click(right_x, center_y)
                        time.sleep(1)
                        return True
                except:
                    pass
            
            print("未找到蓝牙开关")
            return False
            
        except Exception as e:
            print(f"切换蓝牙开关失败: {str(e)}")
            return False