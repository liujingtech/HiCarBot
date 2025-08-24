"""
Custom action for calculating Bluetooth switch position
"""

import time
import os
from typing import Dict, Any
from core.models import Action, DataContext


class CalculateBluetoothSwitchPositionAction(Action):
    """Calculate Bluetooth Switch Position Action"""
    
    def execute(self, context: DataContext) -> bool:
        try:
            # Get OCR results
            ocr_results = context.get_ocr_results('bluetooth_page')
            
            # Check if we have any OCR results
            if not ocr_results or len(ocr_results) == 0:
                print("未获取到OCR识别结果，可能屏幕未解锁或页面未加载完成")
                # Use default position as fallback
                context.set_variable('bluetooth_switch_x', 900)
                context.set_variable('bluetooth_switch_y', 250)
                return True
            
            # Print OCR results for debugging
            print("OCR识别结果:")
            for i, result in enumerate(ocr_results):
                print(f"  {i+1}. 文本: '{result['text']}' 置信度: {result['confidence']:.2f} 位置: {result['center']}")
            
            # Find "蓝牙" text position
            bluetooth_text_position = None
            for result in ocr_results:
                if "蓝牙" in result['text'] and result['center'][1] < 500:  # Near the top
                    bluetooth_text_position = result['center']
                    print(f"找到蓝牙文本位置: {bluetooth_text_position}")
                    break
            
            # Calculate switch position
            if bluetooth_text_position:
                # Switch is typically to the right of the "蓝牙" text
                switch_x = bluetooth_text_position[0] + 400  # Adjust this offset as needed
                switch_y = bluetooth_text_position[1]
                print(f"基于蓝牙文本位置计算开关位置: ({switch_x}, {switch_y})")
            else:
                # Try to find ON/OFF text
                status_text_position = None
                for result in ocr_results:
                    if result['text'] in ["ON", "OFF", "开启", "关闭"] and result['center'][1] < 500:
                        status_text_position = result['center']
                        print(f"找到状态文本位置: {status_text_position}")
                        break
                
                if status_text_position:
                    # Switch is typically to the left of the status text
                    switch_x = status_text_position[0] - 100
                    switch_y = status_text_position[1]
                    print(f"基于状态文本位置计算开关位置: ({switch_x}, {switch_y})")
                else:
                    # Try to find any text that might be near the top right
                    top_right_texts = [result for result in ocr_results if result['center'][1] < 500 and result['center'][0] > 500]
                    if top_right_texts:
                        # Use the rightmost text as reference
                        rightmost_text = max(top_right_texts, key=lambda x: x['center'][0])
                        switch_x = rightmost_text['center'][0] + 100
                        switch_y = rightmost_text['center'][1]
                        print(f"基于右上角文本位置计算开关位置: ({switch_x}, {switch_y})")
                    else:
                        # Use default position
                        switch_x = 900
                        switch_y = 250
                        print(f"使用默认开关位置: ({switch_x}, {switch_y})")
            
            # Save switch position to context
            context.set_variable('bluetooth_switch_x', switch_x)
            context.set_variable('bluetooth_switch_y', switch_y)
            
            return True
        except Exception as e:
            print(f"计算蓝牙开关位置失败: {str(e)}")
            # Use default position as fallback
            context.set_variable('bluetooth_switch_x', 900)
            context.set_variable('bluetooth_switch_y', 250)
            return True