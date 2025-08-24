"""
Advanced action implementations for the Pipeline Engine
This module provides advanced implementations of various actions.
"""

import time
import os
import cv2
import numpy as np
from PIL import Image
import pponnxcr
from typing import Dict, Any, List
from core.models import Action, DataContext


class ToggleBluetoothAction(Action):
    """Toggle Bluetooth Action for toggling Bluetooth state"""
    
    def execute(self, context: DataContext) -> bool:
        try:
            print("提示：请确保设备屏幕已解锁，否则可能无法正确识别蓝牙开关")
            
            # Execute ADB command to open Bluetooth settings
            os.system('adb shell am start -a android.settings.BLUETOOTH_SETTINGS')
            
            # Wait for page to load
            time.sleep(3)
            
            # Take screenshot and perform OCR
            screenshot = self._take_screenshot()
            if screenshot is None:
                return False
            
            # Check if screenshot is valid
            if screenshot.size == 0 or screenshot.shape[0] < 100 or screenshot.shape[1] < 100:
                print("截图无效或尺寸过小，可能屏幕未解锁")
                return False
            
            ocr_results = self._perform_ocr(screenshot, 'zhs')
            
            # Print OCR results for debugging
            print("OCR识别结果:")
            if len(ocr_results) == 0:
                print("  未识别到任何文本，可能屏幕未解锁或页面未加载完成")
                # Try default position
                switch_position = (900, 250)
            else:
                for i, result in enumerate(ocr_results):
                    print(f"  {i+1}. 文本: '{result['text']}' 置信度: {result['confidence']:.2f} 位置: {result['center']}")
                
                # Find the Bluetooth switch position using improved method
                switch_position = self._find_bluetooth_switch_improved(ocr_results)
            
            if switch_position:
                # Click on the Bluetooth switch
                self._click_position(switch_position[0], switch_position[1])
                print(f"已点击蓝牙开关位置: {switch_position}")
                return True
            else:
                print("未找到蓝牙开关位置")
                return False
                
        except Exception as e:
            print(f"Toggle Bluetooth action failed: {str(e)}")
            return False
    
    def _take_screenshot(self):
        """Take screenshot using ADB"""
        try:
            # Take screenshot
            os.system('adb shell screencap -p /sdcard/screenshot.png')
            os.system('adb pull /sdcard/screenshot.png ./screenshot.png')
            os.system('adb shell rm /sdcard/screenshot.png')
            
            # Read screenshot
            screenshot = cv2.imread('screenshot.png')
            return screenshot
        except Exception as e:
            print(f"Failed to take screenshot: {str(e)}")
            return None
    
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
            print(f"OCR failed: {str(e)}")
            return []
    
    def _find_bluetooth_switch_improved(self, ocr_results: List[Dict]) -> tuple:
        """Find Bluetooth switch position using improved method"""
        # Look for "蓝牙" text near the top of the screen
        for result in ocr_results:
            if "蓝牙" in result['text'] and result['center'][1] < 500:  # Near the top
                # Bluetooth switch is typically to the right of the "蓝牙" text
                # Estimate switch position based on common UI patterns
                switch_x = result['center'][0] + 400  # Adjust this offset as needed
                switch_y = result['center'][1]
                print(f"基于文本'{result['text']}'计算开关位置: ({switch_x}, {switch_y})")
                return (switch_x, switch_y)
        
        # Alternative method: Look for common switch indicators
        for result in ocr_results:
            # Look for ON/OFF text which might be near switches
            if result['text'] in ["ON", "OFF", "开启", "关闭"] and result['center'][1] < 500:
                # Switch is typically to the left of the status text
                switch_x = result['center'][0] - 100
                switch_y = result['center'][1]
                print(f"基于状态文本'{result['text']}'计算开关位置: ({switch_x}, {switch_y})")
                return (switch_x, switch_y)
        
        # If we can't find it by text, try to find it by common patterns
        # Bluetooth switches are often near the top right of the screen
        print("使用默认开关位置: (900, 250)")
        return (900, 250)  # Default position for a 1080px wide screen
    
    def _click_position(self, x: int, y: int):
        """Click at specified position using ADB"""
        os.system(f'adb shell input tap {x} {y}')
        time.sleep(0.5)


class ToggleBluetoothActionV2(Action):
    """Toggle Bluetooth Action V2 - Using pattern recognition for switch detection"""
    
    def execute(self, context: DataContext) -> bool:
        try:
            print("提示：请确保设备屏幕已解锁，否则可能无法正确识别蓝牙开关")
            
            # Execute ADB command to open Bluetooth settings
            os.system('adb shell am start -a android.settings.BLUETOOTH_SETTINGS')
            
            # Wait for page to load
            time.sleep(3)
            
            # Take screenshot
            screenshot = self._take_screenshot()
            if screenshot is None:
                return False
            
            # Check if screenshot is valid
            if screenshot.size == 0 or screenshot.shape[0] < 100 or screenshot.shape[1] < 100:
                print("截图无效或尺寸过小，可能屏幕未解锁")
                return False
            
            # Find switch position using image processing
            switch_position = self._find_bluetooth_switch_by_image(screenshot)
            if switch_position:
                # Click on the Bluetooth switch
                self._click_position(switch_position[0], switch_position[1])
                print(f"已点击蓝牙开关位置: {switch_position}")
                return True
            else:
                print("未找到蓝牙开关位置，使用备用方法")
                # Fallback to OCR method
                return self._fallback_to_ocr_method()
                
        except Exception as e:
            print(f"Toggle Bluetooth action failed: {str(e)}")
            return False
    
    def _take_screenshot(self):
        """Take screenshot using ADB"""
        try:
            # Take screenshot
            os.system('adb shell screencap -p /sdcard/screenshot.png')
            os.system('adb pull /sdcard/screenshot.png ./screenshot.png')
            os.system('adb shell rm /sdcard/screenshot.png')
            
            # Read screenshot
            screenshot = cv2.imread('screenshot.png')
            return screenshot
        except Exception as e:
            print(f"Failed to take screenshot: {str(e)}")
            return None
    
    def _find_bluetooth_switch_by_image(self, image):
        """Find Bluetooth switch using image processing techniques"""
        try:
            # Convert to HSV color space
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Define range of blue color in HSV (common switch color)
            lower_blue = np.array([100, 50, 50])
            upper_blue = np.array([130, 255, 255])
            
            # Threshold the HSV image to get only blue colors
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Look for switch-like shapes (typically small rectangles)
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                # Switches are typically small and have specific aspect ratios
                if 30 < w < 100 and 10 < h < 50:
                    # Check if it's in the upper part of the screen
                    if y < 500:
                        center_x = x + w // 2
                        center_y = y + h // 2
                        print(f"通过图像处理找到可能的开关位置: ({center_x}, {center_y})")
                        return (center_x, center_y)
            
            return None
        except Exception as e:
            print(f"图像处理失败: {str(e)}")
            return None
    
    def _fallback_to_ocr_method(self):
        """Fallback to OCR method"""
        try:
            # Take screenshot and perform OCR
            screenshot = self._take_screenshot()
            if screenshot is None:
                return False
            
            # Check if screenshot is valid
            if screenshot.size == 0 or screenshot.shape[0] < 100 or screenshot.shape[1] < 100:
                print("截图无效或尺寸过小，可能屏幕未解锁")
                return False
            
            ocr_results = self._perform_ocr(screenshot, 'zhs')
            
            # Print OCR results for debugging
            print("OCR识别结果:")
            if len(ocr_results) == 0:
                print("  未识别到任何文本，可能屏幕未解锁或页面未加载完成")
                return False
            
            for i, result in enumerate(ocr_results):
                print(f"  {i+1}. 文本: '{result['text']}' 置信度: {result['confidence']:.2f} 位置: {result['center']}")
            
            # Find the Bluetooth switch position using improved method
            switch_position = self._find_bluetooth_switch_improved(ocr_results)
            if switch_position:
                # Click on the Bluetooth switch
                self._click_position(switch_position[0], switch_position[1])
                print(f"已点击蓝牙开关位置: {switch_position}")
                return True
            else:
                print("备用方法也未找到蓝牙开关位置")
                return False
        except Exception as e:
            print(f"备用方法失败: {str(e)}")
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
            print(f"OCR failed: {str(e)}")
            return []
    
    def _find_bluetooth_switch_improved(self, ocr_results: List[Dict]) -> tuple:
        """Find Bluetooth switch position using improved method"""
        # Look for "蓝牙" text near the top of the screen
        for result in ocr_results:
            if "蓝牙" in result['text'] and result['center'][1] < 500:  # Near the top
                # Bluetooth switch is typically to the right of the "蓝牙" text
                # Estimate switch position based on common UI patterns
                switch_x = result['center'][0] + 400  # Adjust this offset as needed
                switch_y = result['center'][1]
                print(f"基于文本'{result['text']}'计算开关位置: ({switch_x}, {switch_y})")
                return (switch_x, switch_y)
        
        # Alternative method: Look for common switch indicators
        for result in ocr_results:
            # Look for ON/OFF text which might be near switches
            if result['text'] in ["ON", "OFF", "开启", "关闭"] and result['center'][1] < 500:
                # Switch is typically to the left of the status text
                switch_x = result['center'][0] - 100
                switch_y = result['center'][1]
                print(f"基于状态文本'{result['text']}'计算开关位置: ({switch_x}, {switch_y})")
                return (switch_x, switch_y)
        
        # If we can't find it by text, try to find it by common patterns
        # Bluetooth switches are often near the top right of the screen
        print("使用默认开关位置: (900, 250)")
        return (900, 250)  # Default position for a 1080px wide screen
    
    def _click_position(self, x: int, y: int):
        """Click at specified position using ADB"""
        os.system(f'adb shell input tap {x} {y}')
        time.sleep(0.5)