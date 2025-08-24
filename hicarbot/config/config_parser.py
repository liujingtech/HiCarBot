"""
Configuration Parser for Pipeline Engine
This module handles parsing of pipeline configuration files in JSON or YAML format.
"""

import json
import yaml
import os
from typing import Dict, Any


class ConfigParser:
    """Parser for pipeline configuration files"""
    
    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        """
        Load and parse a configuration file.
        
        Args:
            config_path (str): Path to the configuration file
            
        Returns:
            Dict[str, Any]: Parsed configuration data
            
        Raises:
            FileNotFoundError: If the config file doesn't exist
            ValueError: If the file format is unsupported
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            if config_path.endswith('.json'):
                return ConfigParser._parse_json(f)
            elif config_path.endswith(('.yaml', '.yml')):
                return ConfigParser._parse_yaml(f)
            else:
                raise ValueError(f"Unsupported configuration file format: {config_path}")
    
    @staticmethod
    def _parse_json(file_handle) -> Dict[str, Any]:
        """Parse JSON configuration file"""
        try:
            return json.load(file_handle)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {str(e)}")
    
    @staticmethod
    def _parse_yaml(file_handle) -> Dict[str, Any]:
        """Parse YAML configuration file"""
        try:
            return yaml.safe_load(file_handle)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in configuration file: {str(e)}")
    
    @staticmethod
    def validate_config(config: Dict[str, Any]) -> bool:
        """
        Validate the configuration structure.
        
        Args:
            config (Dict[str, Any]): Configuration to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Check required fields
        required_fields = ['name', 'pipeline']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required field in configuration: {field}")
        
        # Validate pipeline structure
        pipeline = config['pipeline']
        if not isinstance(pipeline, list):
            raise ValueError("Pipeline must be a list of actions")
        
        # Validate each action
        for i, action in enumerate(pipeline):
            if not isinstance(action, dict):
                raise ValueError(f"Action {i} must be a dictionary")
            
            if 'type' not in action:
                raise ValueError(f"Action {i} missing required 'type' field")
        
        return True