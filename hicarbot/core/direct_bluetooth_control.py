"""
Direct Bluetooth control action for HiCarBot
"""

import subprocess
import time
import os
from typing import Dict, Any
from core.models import Action, DataContext


class EnableBluetoothAction(Action):
    """Enable Bluetooth Action for directly enabling Bluetooth via ADB"""
    
    def execute(self, context: DataContext) -> bool:
        try:
            print("正在尝试通过ADB直接启用蓝牙...")
            
            # Method 1: Try using service call
            result = self._enable_bluetooth_via_service_call()
            if result:
                context.set_variable('bluetooth_enabled', True)
                print("蓝牙已成功启用")
                return True
            
            # Method 2: Try using settings command as fallback
            print("Service call方法失败，尝试使用settings命令...")
            result = self._enable_bluetooth_via_settings()
            if result:
                context.set_variable('bluetooth_enabled', True)
                print("蓝牙已成功启用")
                return True
            
            # Method 3: If both methods fail, use the open_bluetooth approach
            print("ADB命令方法失败，尝试打开蓝牙设置页面...")
            os.system('adb shell am start -a android.settings.BLUETOOTH_SETTINGS')
            time.sleep(2)  # Wait for page to load
            context.set_variable('bluetooth_enabled', None)  # Unknown state
            print("已打开蓝牙设置页面，请手动开启蓝牙")
            return True
            
        except Exception as e:
            print(f"启用蓝牙失败: {str(e)}")
            return False
    
    def _enable_bluetooth_via_service_call(self) -> bool:
        """Enable Bluetooth via service call"""
        try:
            # Enable Bluetooth using service call
            # Command: service call bluetooth_manager 6
            result = subprocess.run(
                "adb shell service call bluetooth_manager 6",
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                print(f"Service call输出: {output}")
                # Check if the call was successful
                # Successful call typically returns something like "Result: Parcel(00000000 00000001 ..."
                return "00000001" in output or "Parcel" in output
            return False
        except Exception as e:
            print(f"Service call方法失败: {str(e)}")
            return False
    
    def _enable_bluetooth_via_settings(self) -> bool:
        """Enable Bluetooth via settings command"""
        try:
            # Enable Bluetooth using settings command
            result = subprocess.run(
                "adb shell settings put global bluetooth_on 1",
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("已通过settings命令启用蓝牙")
                return True
            else:
                print(f"Settings命令失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"Settings命令方法失败: {str(e)}")
            return False


class DisableBluetoothAction(Action):
    """Disable Bluetooth Action for directly disabling Bluetooth via ADB"""
    
    def execute(self, context: DataContext) -> bool:
        try:
            print("正在尝试通过ADB直接禁用蓝牙...")
            
            # Method 1: Try using service call
            result = self._disable_bluetooth_via_service_call()
            if result:
                context.set_variable('bluetooth_enabled', False)
                print("蓝牙已成功禁用")
                return True
            
            # Method 2: Try using settings command as fallback
            print("Service call方法失败，尝试使用settings命令...")
            result = self._disable_bluetooth_via_settings()
            if result:
                context.set_variable('bluetooth_enabled', False)
                print("蓝牙已成功禁用")
                return True
            
            # Method 3: If both methods fail, use the open_bluetooth approach
            print("ADB命令方法失败，尝试打开蓝牙设置页面...")
            os.system('adb shell am start -a android.settings.BLUETOOTH_SETTINGS')
            time.sleep(2)  # Wait for page to load
            context.set_variable('bluetooth_enabled', None)  # Unknown state
            print("已打开蓝牙设置页面，请手动关闭蓝牙")
            return True
            
        except Exception as e:
            print(f"禁用蓝牙失败: {str(e)}")
            return False
    
    def _disable_bluetooth_via_service_call(self) -> bool:
        """Disable Bluetooth via service call"""
        try:
            # Disable Bluetooth using service call
            # Command: service call bluetooth_manager 7
            result = subprocess.run(
                "adb shell service call bluetooth_manager 7",
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                print(f"Service call输出: {output}")
                # Check if the call was successful
                return "00000001" in output or "Parcel" in output
            return False
        except Exception as e:
            print(f"Service call方法失败: {str(e)}")
            return False
    
    def _disable_bluetooth_via_settings(self) -> bool:
        """Disable Bluetooth via settings command"""
        try:
            # Disable Bluetooth using settings command
            result = subprocess.run(
                "adb shell settings put global bluetooth_on 0",
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("已通过settings命令禁用蓝牙")
                return True
            else:
                print(f"Settings命令失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"Settings命令方法失败: {str(e)}")
            return False