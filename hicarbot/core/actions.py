"""
Action implementations for the Pipeline Engine
This module provides concrete implementations of various actions.
"""

import time
import subprocess
import os
import cv2
import numpy as np
from PIL import Image
import pponnxcr
from typing import Dict, Any, List
from core.models import Action, DataContext


class OCRAction(Action):
    """OCR Action for text recognition"""
    
    def execute(self, context: DataContext) -> bool:
        try:
            # Get parameters
            region = self.params.get('region')
            language = self.params.get('language', 'zhs')
            save_to = self.params.get('save_to', 'ocr_result')
            
            # Take screenshot (using ADB)
            screenshot = self._take_screenshot()
            if screenshot is None:
                return False
            
            # Crop to region if specified
            if region:
                x, y, w, h = region
                screenshot = screenshot[y:y+h, x:x+w]
            
            # Perform OCR
            ocr_results = self._perform_ocr(screenshot, language)
            
            # Save results to context
            context.set_ocr_results(save_to, ocr_results)
            context.variables[save_to] = ocr_results
            
            # Print OCR results for debugging
            print(f"OCR识别结果 ({save_to}):")
            for i, result in enumerate(ocr_results):
                print(f"  {i+1}. 文本: '{result['text']}' 置信度: {result['confidence']:.2f} 位置: {result['center']}")
            
            return True
        except Exception as e:
            print(f"OCR action failed: {str(e)}")
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


class ClickAction(Action):
    """Click Action for tapping on screen coordinates"""
    
    def execute(self, context: DataContext) -> bool:
        try:
            position = self.params.get('position')
            text = self.params.get('text')
            offset = self.params.get('offset', [0, 0])
            action_type = self.params.get('action', 'tap')
            
            # Resolve variables in text
            if text:
                original_text = text
                text = self._resolve_variables(text, context)
                print(f"变量解析: '{original_text}' -> '{text}'")
            
            # If text is specified, find it in OCR results
            if text:
                position = self._find_text_position(text, context, offset)
                if position is None:
                    print(f"未找到文本 '{text}'")
                    return False
                else:
                    print(f"找到文本 '{text}'，点击位置: {position}")
            
            # Execute the click action
            if position:
                return self._execute_click(position, action_type)
            
            print("未提供有效的点击位置")
            return False
        except Exception as e:
            print(f"Click action failed: {str(e)}")
            return False
    
    def _find_text_position(self, target_text: str, context: DataContext, offset: List[int]):
        """Find text position in OCR results"""
        # Search in OCR results
        exact_match = None
        partial_match = None
        
        for result_set_key, result_set in context.ocr_results.items():
            if isinstance(result_set, list):
                for item in result_set:
                    item_text = item.get('text', '')
                    # 精确匹配
                    if target_text == item_text:
                        exact_match = (result_set_key, item)
                        break
                    # 包含匹配（作为备选）
                    elif target_text in item_text and partial_match is None:
                        partial_match = (result_set_key, item)
        
        # 优先使用精确匹配
        match = exact_match if exact_match else partial_match
        
        if match:
            result_set_key, item = match
            center = item['center']
            position = [
                center[0] + offset[0],
                center[1] + offset[1]
            ]
            match_type = "精确" if exact_match else "包含"
            print(f"在OCR结果'{result_set_key}'中找到{match_type}匹配文本'{target_text}': {item['text']} 位置:{item['center']}, 偏移后位置:{position}")
            return position
        
        return None
    
    def _execute_click(self, position: List[int], action_type: str) -> bool:
        """Execute click action using ADB"""
        try:
            x, y = position
            print(f"执行点击操作: {action_type} at ({x}, {y})")
            if action_type == 'tap':
                os.system(f'adb shell input tap {x} {y}')
            elif action_type == 'long_press':
                os.system(f'adb shell input swipe {x} {y} {x} {y} 1000')
            # Add more action types as needed
            return True
        except Exception as e:
            print(f"Failed to execute click: {str(e)}")
            return False
    
    def _resolve_variables(self, text: str, context: DataContext) -> str:
        """Resolve variables in text"""
        resolved = text
        for var_name, var_value in context.variables.items():
            # 替换 {{variable_name}} 格式的变量
            resolved = resolved.replace(f'{{{{{var_name}}}}}', str(var_value))
        return resolved


class WaitAction(Action):
    """Wait Action for pausing execution"""
    
    def execute(self, context: DataContext) -> bool:
        try:
            seconds = self.params.get('seconds', 1)
            condition = self.params.get('condition')
            
            # If condition is specified, wait until condition is met or timeout
            if condition:
                timeout = self.params.get('timeout', 30)
                interval = self.params.get('interval', 1)
                start_time = time.time()
                
                while time.time() - start_time < timeout:
                    # In a real implementation, this would evaluate the condition
                    # For now, we'll just wait
                    time.sleep(interval)
                
                return True
            else:
                # Simple wait
                time.sleep(seconds)
                return True
        except Exception as e:
            print(f"Wait action failed: {str(e)}")
            return False


class InputAction(Action):
    """Input Action for entering text"""
    
    def execute(self, context: DataContext) -> bool:
        try:
            text = self.params.get('text', '')
            
            # Resolve variables in text
            resolved_text = self._resolve_variables(text, context)
            
            # Execute input using ADB
            # Escape special characters
            escaped_text = resolved_text.replace(' ', '%s').replace('"', '\\"')
            os.system(f'adb shell input text "{escaped_text}"')
            
            return True
        except Exception as e:
            print(f"Input action failed: {str(e)}")
            return False
    
    def _resolve_variables(self, text: str, context: DataContext) -> str:
        """Resolve variables in text"""
        resolved = text
        for var_name, var_value in context.variables.items():
            resolved = resolved.replace(f'${{{var_name}}}', str(var_value))
        return resolved


class ConditionAction(Action):
    """Condition Action for branching logic"""
    
    def execute(self, context: DataContext) -> bool:
        try:
            expression = self.params.get('expression', 'True')
            if_true = self.params.get('if_true', [])
            if_false = self.params.get('if_false', [])
            
            # Evaluate the condition
            result = self._evaluate_expression(expression, context)
            print(f"条件表达式 '{expression}' 的结果: {result}")
            
            # Execute the appropriate branch
            branch_to_execute = if_true if result else if_false
            if branch_to_execute:
                # In a full implementation, we would execute the branch actions
                # For now, we're just printing what would be executed
                print(f"将执行分支: {branch_to_execute}")
                # Here you would normally execute the actions in the branch
                # For demonstration, we'll just return True
                return True
            else:
                print("没有需要执行的分支")
                return True
                
        except Exception as e:
            print(f"Condition action failed: {str(e)}")
            return False
    
    def _evaluate_expression(self, expression: str, context: DataContext) -> bool:
        """Evaluate condition expression"""
        # This is a simplified implementation
        # A production implementation would need a proper expression evaluator
        try:
            # Create a safe evaluation environment
            eval_globals = {
                "__builtins__": {},
                "len": len,
                "str": str,
                "int": int,
                "float": float,
                "bool": bool,
                "any": any,
                "all": all,
            }
            
            # Add context variables
            eval_locals = context.variables.copy()
            
            # Evaluate expression
            return bool(eval(expression, eval_globals, eval_locals))
        except Exception as e:
            print(f"Failed to evaluate expression '{expression}': {str(e)}")
            return False


class OpenBluetoothAction(Action):
    """Open Bluetooth Settings Action for launching Bluetooth settings page"""
    
    def execute(self, context: DataContext) -> bool:
        try:
            # Execute ADB command to open Bluetooth settings
            os.system('adb shell am start -a android.settings.BLUETOOTH_SETTINGS')
            return True
        except Exception as e:
            print(f"Open Bluetooth action failed: {str(e)}")
            return False