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
            # Execute ADB command to open Bluetooth settings
            os.system('adb shell am start -a android.settings.BLUETOOTH_SETTINGS')
            
            # Wait for page to load
            time.sleep(3)
            
            # Take screenshot and perform OCR
            screenshot = self._take_screenshot()
            if screenshot is None:
                return False
            
            ocr_results = self._perform_ocr(screenshot, 'zhs')
            
            # Print OCR results for debugging
            print("OCR识别结果:")
            for i, result in enumerate(ocr_results):
                print(f"  {i+1}. 文本: '{result['text']}' 置信度: {result['confidence']:.2f} 位置: {result['center']}")
            
            # Find the Bluetooth switch position
            switch_position = self._find_bluetooth_switch(ocr_results)
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
    
    def _find_bluetooth_switch(self, ocr_results: List[Dict]) -> tuple:
        """Find Bluetooth switch position based on OCR results"""
        # Look for "蓝牙" text near the top of the screen
        for result in ocr_results:
            if "蓝牙" in result['text'] and result['center'][1] < 500:  # Near the top
                # Bluetooth switch is typically to the right of the "蓝牙" text
                # Estimate switch position based on screen width (assuming 1080px width)
                switch_x = result['center'][0] + 500  # Adjust this offset as needed
                switch_y = result['center'][1]
                return (switch_x, switch_y)
        
        # If we can't find it by text, try to find it by common patterns
        # Bluetooth switches are often near the top right of the screen
        return (900, 250)  # Default position for a 1080px wide screen
    
    def _click_position(self, x: int, y: int):
        """Click at specified position using ADB"""
        os.system(f'adb shell input tap {x} {y}')
        time.sleep(0.5)