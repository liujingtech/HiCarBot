"""
Test cases for direct Bluetooth control in HiCarBot
"""

import pytest
import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hicarbot.core.models import DataContext
from hicarbot.core.direct_bluetooth_control import EnableBluetoothAction, DisableBluetoothAction


def test_enable_bluetooth_action():
    """Test EnableBluetoothAction creation"""
    action = EnableBluetoothAction("test_enable_bluetooth", {})
    assert action.name == "test_enable_bluetooth"
    assert action.params == {}


def test_disable_bluetooth_action():
    """Test DisableBluetoothAction creation"""
    action = DisableBluetoothAction("test_disable_bluetooth", {})
    assert action.name == "test_disable_bluetooth"
    assert action.params == {}


def test_enable_bluetooth_methods():
    """Test EnableBluetoothAction methods"""
    action = EnableBluetoothAction("test_enable_bluetooth", {})
    
    # These methods would require an actual Android device to test properly
    # For now, we'll just ensure they exist and can be called
    assert hasattr(action, '_enable_bluetooth_via_service_call')
    assert hasattr(action, '_enable_bluetooth_via_settings')


def test_disable_bluetooth_methods():
    """Test DisableBluetoothAction methods"""
    action = DisableBluetoothAction("test_disable_bluetooth", {})
    
    # These methods would require an actual Android device to test properly
    # For now, we'll just ensure they exist and can be called
    assert hasattr(action, '_disable_bluetooth_via_service_call')
    assert hasattr(action, '_disable_bluetooth_via_settings')