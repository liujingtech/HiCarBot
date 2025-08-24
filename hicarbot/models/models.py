"""
Data Models for HiCarBot
This module defines the core data structures used throughout the framework.
"""

from typing import Dict, Any, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DataContext:
    """Data context for storing and passing data between actions"""
    
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.ocr_results: Dict[str, List[Dict]] = {}
        self.execution_history: List[Dict] = []
    
    def set_variable(self, key: str, value: Any):
        """Set a variable in the context"""
        self.variables[key] = value
        logger.debug(f"Set variable {key} = {value}")
    
    def get_variable(self, key: str, default: Any = None) -> Any:
        """Get a variable from the context"""
        return self.variables.get(key, default)
    
    def set_ocr_results(self, key: str, results: List[Dict]):
        """Set OCR results in the context"""
        self.ocr_results[key] = results
        logger.debug(f"Set OCR results {key} with {len(results)} items")
    
    def get_ocr_results(self, key: str) -> List[Dict]:
        """Get OCR results from the context"""
        return self.ocr_results.get(key, [])
    
    def find_text_position(self, target_text: str, ocr_result_key: Optional[str] = None) -> Optional[Dict]:
        """Find text position in OCR results"""
        # If OCR result key is specified, search only in that result set
        if ocr_result_key:
            results = self.ocr_results.get(ocr_result_key, [])
            for result in results:
                if target_text in result['text']:
                    return result
        else:
            # Search in all OCR results
            for results in self.ocr_results.values():
                for result in results:
                    if target_text in result['text']:
                        return result
        return None


class Action:
    """Base class for all actions"""
    
    def __init__(self, name: str, params: Dict[str, Any]):
        self.name = name
        self.params = params
    
    def execute(self, context: DataContext) -> bool:
        """Execute the action, to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement execute method")