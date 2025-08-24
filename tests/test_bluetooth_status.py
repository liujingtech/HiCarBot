"""
Test cases for Bluetooth status checking in HiCarBot
"""

import pytest
import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hicarbot.core.models import DataContext
from hicarbot.core.bluetooth_status import CheckBluetoothStatusAction


def test_check_bluetooth_status_action():
    """Test CheckBluetoothStatusAction creation"""
    action = CheckBluetoothStatusAction("test_check_bluetooth_status", {})
    assert action.name == "test_check_bluetooth_status"
    assert action.params == {}


def test_analyze_bluetooth_status_from_ocr():
    """Test analyzing Bluetooth status from OCR results"""
    action = CheckBluetoothStatusAction("test_check_bluetooth_status", {})
    
    # Test with enabled status
    ocr_results_enabled = [
        {"text": "蓝牙", "confidence": 0.9, "center": (200, 250)},
        {"text": "开启", "confidence": 0.9, "center": (800, 250)}
    ]
    assert action._analyze_bluetooth_status_from_ocr(ocr_results_enabled) == True
    
    # Test with disabled status
    ocr_results_disabled = [
        {"text": "蓝牙", "confidence": 0.9, "center": (200, 250)},
        {"text": "关闭", "confidence": 0.9, "center": (800, 250)}
    ]
    assert action._analyze_bluetooth_status_from_ocr(ocr_results_disabled) == False
    
    # Test with no status indicators
    ocr_results_unknown = [
        {"text": "蓝牙", "confidence": 0.9, "center": (200, 250)},
        {"text": "设备名称", "confidence": 0.9, "center": (150, 600)}
    ]
    assert action._analyze_bluetooth_status_from_ocr(ocr_results_unknown) == False