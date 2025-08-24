import cv2
import numpy as np
from PIL import Image
import pponnxcr
import subprocess
import re
import time
import json
import yaml
from typing import Dict, Any, List, Optional, Union
import logging
import os
import sys

# Add the parent directory to the Python path to allow imports from sibling directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.models import DataContext
from core.actions import OCRAction, ClickAction, WaitAction, InputAction, ConditionAction, OpenBluetoothAction
from core.advanced_actions import ToggleBluetoothAction, ToggleBluetoothActionV2
from core.bluetooth_status import CheckBluetoothStatusAction
from core.direct_bluetooth_control import EnableBluetoothAction, DisableBluetoothAction
from core.calculate_switch_position import CalculateBluetoothSwitchPositionAction

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ActionExecutor:
    """动作执行器"""
    
    def __init__(self, data_context: DataContext):
        self.data_context = data_context
        # 动作类型映射
        self.action_mapping = {
            'ocr': OCRAction,
            'click_text': ClickAction,
            'click_position': ClickAction,
            'wait': WaitAction,
            'input': InputAction,
            'condition': ConditionAction,
            'open_bluetooth': OpenBluetoothAction,
            'toggle_bluetooth': ToggleBluetoothAction,
            'toggle_bluetooth_v2': ToggleBluetoothActionV2,
            'check_bluetooth_status': CheckBluetoothStatusAction,
            'enable_bluetooth': EnableBluetoothAction,
            'disable_bluetooth': DisableBluetoothAction,
            'calculate_bluetooth_switch_position': CalculateBluetoothSwitchPositionAction
        }
    
    def take_screenshot(self) -> np.ndarray:
        """使用ADB对Android设备进行截图"""
        logger.info("正在获取Android设备截图...")
        # 使用ADB截图并保存到本地
        os.system('adb shell screencap -p /sdcard/screenshot.png')
        os.system('adb pull /sdcard/screenshot.png ./screenshot.png')
        os.system('adb shell rm /sdcard/screenshot.png')
        
        # 读取截图
        screenshot = cv2.imread('screenshot.png')
        logger.info("截图获取成功")
        return screenshot
    
    def get_screen_size(self) -> Optional[tuple]:
        """获取Android设备屏幕分辨率"""
        logger.info("正在获取设备屏幕尺寸...")
        result = subprocess.run(['adb', 'shell', 'wm', 'size'], capture_output=True, text=True)
        if result.returncode == 0:
            # 解析输出，格式为 "Physical size: 1080x2340"
            match = re.search(r'Physical size: (\d+)x(\d+)', result.stdout)
            if match:
                width = int(match.group(1))
                height = int(match.group(2))
                logger.info(f"设备屏幕尺寸: {width}x{height}")
                return width, height
        logger.warning("获取设备屏幕尺寸失败")
        return None
    
    def ocr_screenshot_with_position(self, image: np.ndarray) -> List[Dict]:
        """使用pponnxcr对图像进行文字识别并返回位置信息"""
        logger.info("正在进行OCR识别...")
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
        
        logger.info(f"OCR识别完成，共识别到{len(texts)}个文本")
        return texts
    
    def click_on_position(self, x: int, y: int):
        """在指定坐标执行点击操作"""
        logger.info(f"正在点击坐标 ({x}, {y})")
        os.system(f'adb shell input tap {x} {y}')
        time.sleep(0.5)  # 等待点击效果
    
    def click_on_text(self, target_text: str):
        """根据OCR识别结果点击指定文本"""
        logger.info(f"正在查找并点击文本: {target_text}")
        # 查找目标文本
        result = self.data_context.find_text_position(target_text)
        if result:
            # 获取文本中心点坐标
            center_x, center_y = result['center']
            # 执行点击操作
            self.click_on_position(center_x, center_y)
            logger.info(f"已在坐标 ({center_x}, {center_y}) 点击文本: {result['text']}")
            return True
        else:
            logger.warning(f"未找到文本: {target_text}")
            return False
    
    def wait(self, seconds: float):
        """等待指定时间"""
        logger.info(f"等待 {seconds} 秒")
        time.sleep(seconds)
    
    def input_text(self, text: str):
        """输入文本"""
        logger.info(f"输入文本: {text}")
        # 将文本中的空格替换为%sp字符
        escaped_text = text.replace(' ', '%s').replace('"', '\\"')
        os.system(f'adb shell input text "{escaped_text}"')
        time.sleep(0.5)
    
    def execute_action(self, action_config: Dict) -> bool:
        """执行单个动作"""
        action_type = action_config.get('type')
        params = action_config.get('params', {})
        name = action_config.get('name', action_type)
        
        logger.info(f"执行动作: {name} ({action_type})")
        
        # 获取动作类
        action_class = self.action_mapping.get(action_type)
        if not action_class:
            logger.warning(f"未知的动作类型: {action_type}")
            return False
        
        # 创建并执行动作
        try:
            action = action_class(name, params)
            return action.execute(self.data_context)
        except Exception as e:
            logger.error(f"执行动作 {name} 时发生错误: {str(e)}")
            return False


class ConfigParser:
    """配置解析器"""
    
    @staticmethod
    def parse(config_file: str) -> Dict:
        """解析配置文件"""
        logger.info(f"正在解析配置文件: {config_file}")
        with open(config_file, 'r', encoding='utf-8') as f:
            if config_file.endswith('.yaml') or config_file.endswith('.yml'):
                config = yaml.safe_load(f)
            else:
                config = json.load(f)
        logger.info("配置文件解析完成")
        return config


class PipelineEngine:
    """流水线引擎"""
    
    def __init__(self):
        self.data_context = DataContext()
        self.action_executor = ActionExecutor(self.data_context)
        self.config = None
    
    def load_config(self, config_file: str):
        """加载配置文件"""
        self.config = ConfigParser.parse(config_file)
        logger.info(f"流水线 '{self.config.get('name', 'Unknown')}' 加载完成")
    
    def run(self):
        """运行流水线"""
        if not self.config:
            logger.error("未加载配置文件")
            return
        
        logger.info(f"开始执行流水线: {self.config.get('name', 'Unknown')}")
        
        # 设置变量
        variables = self.config.get('variables', {})
        for key, value in variables.items():
            self.data_context.set_variable(key, value)
        
        # 执行动作序列
        actions = self.config.get('actions', [])
        for i, action_config in enumerate(actions):
            logger.info(f"执行第 {i+1}/{len(actions)} 个动作")
            success = self.action_executor.execute_action(action_config)
            if not success:
                logger.error(f"动作执行失败，流水线终止")
                return
        
        logger.info("流水线执行完成")