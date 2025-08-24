"""
Debug script for testing OCR functionality
"""

import cv2
import numpy as np
from PIL import Image
import pponnxcr
import os

def test_ocr():
    """Test OCR functionality"""
    try:
        # Take screenshot
        print("正在获取截图...")
        os.system('adb shell screencap -p /sdcard/screenshot.png')
        os.system('adb pull /sdcard/screenshot.png ./screenshot.png')
        os.system('adb shell rm /sdcard/screenshot.png')
        
        # Check if screenshot file exists and size
        if os.path.exists('screenshot.png'):
            size = os.path.getsize('screenshot.png')
            print(f"截图文件大小: {size} 字节")
            if size < 1000:
                print("截图文件太小，可能有问题")
                return
        
        # Read screenshot
        screenshot = cv2.imread('screenshot.png')
        if screenshot is None:
            print("无法读取截图文件")
            return
        
        print(f"截图尺寸: {screenshot.shape}")
        
        # Initialize OCR system
        print("正在初始化OCR系统...")
        text_sys = pponnxcr.TextSystem('zhs')  # 使用简体中文模型
        
        # Convert OpenCV image to PIL
        pil_image = Image.fromarray(cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB))
        
        # Perform OCR
        print("正在进行OCR识别...")
        result = text_sys.detect_and_ocr(np.array(pil_image))
        
        # Process results
        print(f"OCR识别完成，共识别到{len(result)}个文本")
        for i, boxed_result in enumerate(result):
            text = boxed_result.text
            confidence = boxed_result.score
            print(f"  {i+1}. 文本: '{text}' 置信度: {confidence:.2f}")
            
    except Exception as e:
        print(f"OCR测试失败: {str(e)}")

if __name__ == "__main__":
    test_ocr()