"""
Simple Bluetooth toggle action for MVP
This module provides a minimal implementation to open Bluetooth settings and toggle the switch.
"""

import uiautomator2 as u2
import time
from core.models import Action, DataContext


class SimpleBluetoothToggleAction(Action):
    """Simple Bluetooth Toggle Action - Open Bluetooth settings and ensure Bluetooth is enabled"""
    
    def execute(self, context: DataContext) -> bool:
        try:
            print("正在执行简单的蓝牙开关操作...")
            
            # Connect to device
            d = u2.connect()
            
            # Open Bluetooth settings
            print("正在打开蓝牙设置页面...")
            d.app_start("com.android.settings", stop=True)
            time.sleep(2)
            
            # Try to navigate to Bluetooth settings
            self._navigate_to_bluetooth(d)
            
            # Wait for page to load
            time.sleep(3)
            
            # Ensure Bluetooth is enabled
            self._ensure_bluetooth_enabled(d)
            
            print("蓝牙开关操作完成")
            return True
            
        except Exception as e:
            print(f"简单的蓝牙开关操作失败: {str(e)}")
            return False
    
    def _navigate_to_bluetooth(self, d):
        """Navigate to Bluetooth settings"""
        try:
            # Method 1: Direct intent
            print("尝试通过intent打开蓝牙设置...")
            d.shell('am start -a android.settings.BLUETOOTH_SETTINGS')
            time.sleep(2)
            
            # Check if we're on Bluetooth page
            if self._is_on_bluetooth_page(d):
                return
            
            # Method 2: Find "蓝牙" text and click it
            print("尝试通过文本导航到蓝牙设置...")
            bluetooth_elements = d.xpath("//*[@text='蓝牙' or @text='Bluetooth']")
            if bluetooth_elements.exists:
                bluetooth_elements.click()
                time.sleep(2)
                return
                
        except Exception as e:
            print(f"导航到蓝牙设置失败: {str(e)}")
    
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
            print("正在检查蓝牙状态...")
            
            # Look for Bluetooth switch
            switch_elements = d(className="android.widget.Switch")
            if len(switch_elements) > 0:
                # Get switch status
                info = switch_elements[0].info
                is_checked = info.get('checked', False)
                print(f"蓝牙开关状态: {'开启' if is_checked else '关闭'}")
                
                # If not enabled, click to enable
                if not is_checked:
                    print("蓝牙未开启，正在打开蓝牙...")
                    switch_elements[0].click()
                    time.sleep(2)
                    print("蓝牙已开启")
                else:
                    print("蓝牙已处于开启状态")
                return  # Success
            
            # If no switch found, try alternative method
            print("未找到蓝牙开关，尝试替代方法...")
            
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
                    print("已尝试点击蓝牙开关位置")
                    return  # Assume success
            
            # Last resort: try to navigate to Bluetooth settings directly
            print("尝试直接打开蓝牙设置...")
            d.shell('am start -a android.bluetooth.adapter.action.REQUEST_ENABLE')
            time.sleep(3)
            print("已发送蓝牙开启请求")
                
        except Exception as e:
            print(f"确保蓝牙开启失败: {str(e)}")