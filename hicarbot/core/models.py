"""
Data models for the Pipeline Engine
This module defines the core data models used by the pipeline engine.
"""

from typing import Dict, Any, List, Optional
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DataContext:
    """数据上下文，用于存储和传递动作间的数据"""
    
    def __init__(self):
        self.variables = {}
        self.ocr_results = {}
        self.execution_history = []
    
    def set_variable(self, key: str, value: Any):
        """设置变量"""
        self.variables[key] = value
        logger.debug(f"设置变量 {key} = {value}")
    
    def get_variable(self, key: str, default: Any = None) -> Any:
        """获取变量"""
        return self.variables.get(key, default)
    
    def set_ocr_results(self, key: str, results: List[Dict]):
        """设置OCR识别结果"""
        self.ocr_results[key] = results
        logger.debug(f"设置OCR结果 {key}，共{len(results)}个结果")
    
    def get_ocr_results(self, key: str) -> List[Dict]:
        """获取OCR识别结果"""
        return self.ocr_results.get(key, [])
    
    def find_text_position(self, target_text: str, ocr_result_key: str = None) -> Optional[Dict]:
        """根据文本查找位置信息"""
        # 如果指定了OCR结果键，则只在该结果中查找
        if ocr_result_key:
            results = self.ocr_results.get(ocr_result_key, [])
            for result in results:
                if target_text in result['text']:
                    return result
        else:
            # 在所有OCR结果中查找
            for results in self.ocr_results.values():
                for result in results:
                    if target_text in result['text']:
                        return result
        return None


class Action:
    """动作基类"""
    
    def __init__(self, name: str, params: Dict[str, Any]):
        self.name = name
        self.params = params
    
    def execute(self, context: DataContext) -> bool:
        """执行动作，子类需要重写此方法"""
        raise NotImplementedError("子类必须实现execute方法")