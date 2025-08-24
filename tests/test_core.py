"""
Test cases for HiCarBot
"""

import pytest
import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hicarbot.core.models import DataContext
from hicarbot.core.actions import OpenBluetoothAction


def test_data_context():
    """Test DataContext functionality"""
    context = DataContext()
    
    # Test variable setting and getting
    context.set_variable("test_key", "test_value")
    assert context.get_variable("test_key") == "test_value"
    assert context.get_variable("nonexistent_key", "default") == "default"
    
    # Test OCR results setting and getting
    test_results = [{"text": "test", "confidence": 0.9, "box": [], "center": (100, 200)}]
    context.set_ocr_results("test_result", test_results)
    assert context.get_ocr_results("test_result") == test_results


def test_open_bluetooth_action():
    """Test OpenBluetoothAction creation"""
    action = OpenBluetoothAction("test_bluetooth_action", {})
    assert action.name == "test_bluetooth_action"
    assert action.params == {}