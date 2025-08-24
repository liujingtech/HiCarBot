"""
Bluetooth status checking action for HiCarBot
"""

import subprocess
import re
import time
import os
import cv2
import numpy as np
from PIL import Image
import pponnxcr
from typing import Dict, Any, List
from core.models import Action, DataContext


class CheckBluetoothStatusAction(Action):
    """Check Bluetooth Status Action for checking if Bluetooth is enabled"""
    
    def execute(self, context: DataContext) -> bool:
        try:
            # Method 1: Try to get Bluetooth status via ADB command
            status = self._get_bluetooth_status_via_adb()
            if status is not None:
                context.set_variable('bluetooth_status', status)
                context.set_variable('is_bluetooth_enabled', status)
                print(f"蓝牙状态 (ADB): {'开启' if status else '关闭'}")
                return True
            
            # Method 2: If ADB method fails, try OCR method
            print("无法通过ADB获取蓝牙状态，尝试通过OCR识别...")
            return self._check_bluetooth_status_via_ocr(context)
            
        except Exception as e:
            print(f"检查蓝牙状态失败: {str(e)}")
            return False
    
    def _get_bluetooth_status_via_adb(self) -> bool | None:
        """Get Bluetooth status via ADB command"""
        try:
            # Try different ADB commands to check Bluetooth status
            commands = [
                "adb shell settings get global bluetooth_on",
                "adb shell dumpsys bluetooth_manager | grep 'enabled'",
            ]
            
            for command in commands:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    output = result.stdout.strip()
                    # Parse the output
                    if "bluetooth_on" in command:
                        # Returns 1 if enabled, 0 if disabled
                        return output == "1"
                    elif "enabled" in command:
                        # Check if "enabled" is in output
                        return "enabled" in output.lower()
            
            return None  # Could not determine status
        except Exception as e:
            print(f"ADB命令检查蓝牙状态失败: {str(e)}")
            return None
    
    def _check_bluetooth_status_via_ocr(self, context: DataContext) -> bool:
        """Check Bluetooth status via OCR method"""
        try:
            # Open Bluetooth settings
            os.system('adb shell am start -a android.settings.BLUETOOTH_SETTINGS')
            time.sleep(3)  # Wait for page to load
            
            # Take screenshot
            os.system('adb shell screencap -p /sdcard/screenshot.png')
            os.system('adb pull /sdcard/screenshot.png ./screenshot.png')
            os.system('adb shell rm /sdcard/screenshot.png')
            
            # Read screenshot
            screenshot = cv2.imread('screenshot.png')
            if screenshot is None:
                print("无法读取截图")
                return False
            
            # Perform OCR
            ocr_results = self._perform_ocr(screenshot, 'zhs')
            
            # Print OCR results for debugging
            print("OCR识别结果:")
            for i, result in enumerate(ocr_results):
                print(f"  {i+1}. 文本: '{result['text']}' 置信度: {result['confidence']:.2f} 位置: {result['center']}")
            
            # Look for status indicators
            is_enabled = self._analyze_bluetooth_status_from_ocr(ocr_results)
            
            # Save result to context
            context.set_variable('bluetooth_status', is_enabled)
            context.set_variable('is_bluetooth_enabled', is_enabled)
            print(f"蓝牙状态 (OCR): {'开启' if is_enabled else '关闭'}")
            
            return True
        except Exception as e:
            print(f"OCR检查蓝牙状态失败: {str(e)}")
            return False
    
    def _perform_ocr(self, image, language: str) -> List[Dict]:
        """Perform OCR on image"""
        try:
            # Initialize OCR system
            text_sys = pponnxcr.TextSystem(language)
            
            # Convert OpenCV image to PIL
            pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            
            # Perform OCR
            result = text_sys.detect_and_ocr(np.array(pil_image))
            
            # Process results
            texts = []
            for boxed_result in result:
                text = boxed_result.text
                confidence = boxed_result.score
                box = boxed_result.box
                
                # Calculate center point
                x_coords = box[:, 0]
                y_coords = box[:, 1]
                center_x = int(np.mean(x_coords))
                center_y = int(np.mean(y_coords))
                
                texts.append({
                    'text': text,
                    'confidence': confidence,
                    'box': box.tolist(),
                    'center': (center_x, center_y)
                })
            
            return texts
        except Exception as e:
            print(f"OCR执行失败: {str(e)}")
            return []
    
    def _analyze_bluetooth_status_from_ocr(self, ocr_results: List[Dict]) -> bool:
        """Analyze Bluetooth status from OCR results"""
        # Look for common status indicators
        status_indicators = {
            'enabled': ['开启', 'ON', '启用', '已开启', '打开'],
            'disabled': ['关闭', 'OFF', '禁用', '已关闭', '未开启']
        }
        
        # Check all OCR results for status indicators
        all_text = " ".join([result['text'] for result in ocr_results])
        
        # Check for enabled indicators
        for indicator in status_indicators['enabled']:
            if indicator in all_text:
                return True
        
        # Check for disabled indicators
        for indicator in status_indicators['disabled']:
            if indicator in all_text:
                return False
        
        # If we can't determine from text, look for the switch position
        # Typically, if we see "蓝牙" text with a switch nearby, we can infer status
        for result in ocr_results:
            if "蓝牙" in result['text']:
                # Look for visual indicators near the Bluetooth text
                # This is a simplified approach - in reality, you might need to analyze 
                # the actual switch graphics or look for specific UI elements
                pass
        
        # Default to False if no indicators found
        print("无法从OCR结果确定蓝牙状态，默认为关闭")
        return False