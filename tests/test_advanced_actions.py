"""
Test cases for advanced actions in HiCarBot
"""

import pytest
import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hicarbot.core.models import DataContext
from hicarbot.core.advanced_actions import ToggleBluetoothAction


def test_toggle_bluetooth_action():
    """Test ToggleBluetoothAction creation"""
    action = ToggleBluetoothAction("test_toggle_bluetooth", {})
    assert action.name == "test_toggle_bluetooth"
    assert action.params == {}


def test_find_bluetooth_switch():
    """Test finding Bluetooth switch position"""
    action = ToggleBluetoothAction("test_toggle_bluetooth", {})
    
    # Mock OCR results with "蓝牙" text near the top
    ocr_results = [
        {"text": "蓝牙", "confidence": 0.9, "center": (200, 250)},
        {"text": "设备名称", "confidence": 0.9, "center": (150, 600)}
    ]
    
    # Test finding switch position
    switch_position = action._find_bluetooth_switch(ocr_results)
    assert switch_position is not None
    # Should be offset to the right of the "蓝牙" text
    assert switch_position[0] > 200
    assert switch_position[1] == 250