import cv2
import numpy as np
from PIL import Image
import pponnxcr
import subprocess
import re


def take_screenshot():
    """使用ADB对Android设备进行截图"""
    # 使用ADB截图并保存到本地
    import os
    os.system('adb shell screencap -p /sdcard/screenshot.png')
    os.system('adb pull /sdcard/screenshot.png ./screenshot.png')
    os.system('adb shell rm /sdcard/screenshot.png')
    
    # 读取截图
    screenshot = cv2.imread('screenshot.png')
    return screenshot


def get_screen_size():
    """获取Android设备屏幕分辨率"""
    result = subprocess.run(['adb', 'shell', 'wm', 'size'], capture_output=True, text=True)
    if result.returncode == 0:
        # 解析输出，格式为 "Physical size: 1080x2340"
        match = re.search(r'Physical size: (\d+)x(\d+)', result.stdout)
        if match:
            width = int(match.group(1))
            height = int(match.group(2))
            return width, height
    return None


def ocr_screenshot_with_position(image):
    """使用pponnxcr对图像进行文字识别并返回位置信息"""
    # 初始化pponnxcr TextSystem
    text_sys = pponnxcr.TextSystem('zhs')  # 使用简体中文模型
    
    # 将OpenCV图像转换为PIL图像
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    # 进行OCR识别
    result = text_sys.detect_and_ocr(np.array(pil_image))
    
    # 提取识别结果和位置信息
    texts = []
    for boxed_result in result:
        text = boxed_result.text
        confidence = boxed_result.score
        # 获取文本框坐标
        box = boxed_result.box
        # 计算中心点坐标
        x_coords = box[:, 0]
        y_coords = box[:, 1]
        center_x = int(np.mean(x_coords))
        center_y = int(np.mean(y_coords))
        
        texts.append({
            'text': text,
            'confidence': confidence,
            'box': box,
            'center': (center_x, center_y)
        })
    
    return texts


def click_on_text(target_text, ocr_results, screen_size):
    """根据OCR识别结果点击指定文本"""
    # 查找目标文本
    for result in ocr_results:
        if target_text in result['text']:
            # 获取文本中心点坐标
            center_x, center_y = result['center']
            
            # 如果提供了屏幕尺寸，进行坐标转换
            if screen_size:
                # 这里假设截图尺寸和屏幕尺寸一致
                # 如果需要更精确的转换，可以根据实际截图尺寸进行计算
                pass
            
            # 执行点击操作
            import os
            os.system(f'adb shell input tap {center_x} {center_y}')
            print(f"已在坐标 ({center_x}, {center_y}) 点击文本: {result['text']}")
            return True
    
    print(f"未找到文本: {target_text}")
    return False


def main():
    # 获取设备屏幕尺寸
    print("正在获取设备屏幕尺寸...")
    screen_size = get_screen_size()
    if screen_size:
        print(f"设备屏幕尺寸: {screen_size[0]}x{screen_size[1]}")
    else:
        print("获取设备屏幕尺寸失败")
    
    # 获取截图
    print("正在获取Android设备截图...")
    screenshot = take_screenshot()
    
    if screenshot is not None:
        print("截图获取成功，正在进行OCR识别...")
        # 进行OCR识别
        ocr_results = ocr_screenshot_with_position(screenshot)
        
        # 输出识别结果
        print("\nOCR识别结果:")
        print("-" * 50)
        for result in ocr_results:
            print(f"文字: {result['text']} (置信度: {result['confidence']:.2f}) 位置: {result['center']}")
        
        # 示例：点击包含特定文本的区域
        # 这里以点击"Google"为例
        target_text = "百度一下"
        click_on_text(target_text, ocr_results, screen_size)
    else:
        print("截图获取失败")


if __name__ == "__main__":
    main()