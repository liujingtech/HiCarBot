import cv2
import numpy as np
from PIL import Image
import pponnxcr

def test_pponnxcr():
    """测试pponnxcr库的基本用法"""
    
    # 创建一个简单的测试图像
    # 实际使用中，你可以加载真实的图像
    img = np.ones((100, 300, 3), dtype=np.uint8) * 255  # 白色背景
    cv2.putText(img, 'Hello World', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    # 将OpenCV图像转换为PIL图像
    pil_image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    # 方法1: 使用TextSystem (推荐)
    print("方法1: 使用TextSystem")
    text_sys = pponnxcr.TextSystem('zhs')  # 使用简体中文模型
    result = text_sys.detect_and_ocr(np.array(pil_image))
    
    print(f"检测到 {len(result)} 个文本框:")
    for i, boxed_result in enumerate(result):
        print(f"  文本 {i+1}: '{boxed_result.text}' (置信度: {boxed_result.score:.2f})")
    
    # 方法2: 分别使用检测器和识别器
    print("\n方法2: 分别使用检测器和识别器")
    detector = pponnxcr.TextDetector('zhs')
    recognizer = pponnxcr.TextRecognizer('zhs')
    
    # 检测文本框
    dt_boxes, det_elapse = detector(np.array(pil_image))
    print(f"检测耗时: {det_elapse:.3f}s, 检测到 {len(dt_boxes)} 个文本框")
    
    # 裁剪文本区域并识别
    img_crop_list = []
    for box in dt_boxes:
        # 简化的裁剪方法
        x_coords = box[:, 0]
        y_coords = box[:, 1]
        x1, x2 = int(min(x_coords)), int(max(x_coords))
        y1, y2 = int(min(y_coords)), int(max(y_coords))
        img_crop = np.array(pil_image)[y1:y2, x1:x2]
        img_crop_list.append(img_crop)
    
    # 识别文本
    rec_res, rec_elapse = recognizer(img_crop_list)
    print(f"识别耗时: {rec_elapse:.3f}s")
    
    for i, (text, score) in enumerate(rec_res):
        print(f"  文本 {i+1}: '{text}' (置信度: {score:.2f})")

if __name__ == "__main__":
    test_pponnxcr()