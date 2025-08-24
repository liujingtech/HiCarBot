"""
Integration tests for HiCarBot
"""

import pytest
import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hicarbot.core.pipeline_engine import PipelineEngine


def test_bluetooth_pipeline():
    """Test the bluetooth pipeline execution"""
    # Create a temporary YAML file for testing
    test_config = """
name: "蓝牙设置测试"
version: "1.0"
description: "测试打开Android设备的蓝牙设置页面"

actions:
  - name: "打开蓝牙设置"
    type: "open_bluetooth"
  
  - name: "等待页面加载"
    type: "wait"
    params:
      seconds: 1
"""
    
    # Write test config to a temporary file
    with open("test_bluetooth.yaml", "w", encoding="utf-8") as f:
        f.write(test_config)
    
    try:
        # Create and run pipeline engine
        engine = PipelineEngine()
        engine.load_config("test_bluetooth.yaml")
        
        # The pipeline should load successfully
        assert engine.config is not None
        assert engine.config["name"] == "蓝牙设置测试"
        
        # Check that actions are loaded
        actions = engine.config.get("actions", [])
        assert len(actions) == 2
        assert actions[0]["type"] == "open_bluetooth"
        assert actions[1]["type"] == "wait"
        
    finally:
        # Clean up temporary file
        if os.path.exists("test_bluetooth.yaml"):
            os.remove("test_bluetooth.yaml")