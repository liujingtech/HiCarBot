"""
Test cases for UI Automator Bluetooth control in HiCarBot
"""

import pytest
import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hicarbot.core.models import DataContext
from hicarbot.core.bluetooth_ui_automator import CheckBluetoothStatusWithUIAction, ToggleBluetoothWithUIAction


def test_check_bluetooth_status_ui_action():
    """Test CheckBluetoothStatusWithUIAction creation"""
    action = CheckBluetoothStatusWithUIAction("test_check_bluetooth_status_ui", {})
    assert action.name == "test_check_bluetooth_status_ui"
    assert action.params == {}


def test_toggle_bluetooth_ui_action():
    """Test ToggleBluetoothWithUIAction creation"""
    action = ToggleBluetoothWithUIAction("test_toggle_bluetooth_ui", {})
    assert action.name == "test_toggle_bluetooth_ui"
    assert action.params == {}


def test_ui_action_methods():
    """Test UI action methods exist"""
    check_action = CheckBluetoothStatusWithUIAction("test_check_bluetooth_status_ui", {})
    toggle_action = ToggleBluetoothWithUIAction("test_toggle_bluetooth_ui", {})
    
    # These methods would require an actual Android device to test properly
    # For now, we'll just ensure they exist and can be called
    assert hasattr(check_action, '_navigate_to_bluetooth_settings')
    assert hasattr(check_action, '_is_on_bluetooth_page')
    assert hasattr(check_action, '_check_bluetooth_status')
    assert hasattr(check_action, '_is_bluetooth_switch')
    
    assert hasattr(toggle_action, '_navigate_to_bluetooth_settings')
    assert hasattr(toggle_action, '_is_on_bluetooth_page')
    assert hasattr(toggle_action, '_toggle_bluetooth_switch')
    assert hasattr(toggle_action, '_is_bluetooth_switch')