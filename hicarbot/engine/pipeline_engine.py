"""
Pipeline Engine for HiCarBot
This module implements the core execution engine for the automation framework.
"""

import yaml
import json
import logging
from typing import Dict, Any, List, Optional
from hicarbot.models.models import DataContext, Action
from hicarbot.actions.simple_bluetooth import SimpleBluetoothToggleAction

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ActionExecutor:
    """Action executor for running actions"""
    
    def __init__(self, data_context: DataContext):
        self.data_context = data_context
        # Action type mapping
        self.action_mapping = {
            'simple_bluetooth_toggle': SimpleBluetoothToggleAction
        }
    
    def execute_action(self, action_config: Dict) -> bool:
        """Execute a single action"""
        action_type = action_config.get('type')
        params = action_config.get('params', {})
        name = action_config.get('name', action_type)
        
        logger.info(f"Executing action: {name} ({action_type})")
        
        # Get action class
        action_class = self.action_mapping.get(action_type)
        if not action_class:
            logger.warning(f"Unknown action type: {action_type}")
            return False
        
        # Create and execute action
        try:
            action = action_class(name, params)
            return action.execute(self.data_context)
        except Exception as e:
            logger.error(f"Failed to execute action {name}: {str(e)}")
            return False


class ConfigParser:
    """Configuration parser"""
    
    @staticmethod
    def parse(config_file: str) -> Dict:
        """Parse configuration file"""
        logger.info(f"Parsing configuration file: {config_file}")
        with open(config_file, 'r', encoding='utf-8') as f:
            if config_file.endswith('.yaml') or config_file.endswith('.yml'):
                config = yaml.safe_load(f)
            else:
                config = json.load(f)
        logger.info("Configuration parsing completed")
        return config


class PipelineEngine:
    """Main pipeline engine"""
    
    def __init__(self):
        self.data_context = DataContext()
        self.action_executor = ActionExecutor(self.data_context)
        self.config = None
    
    def load_config(self, config_file: str):
        """Load configuration file"""
        self.config = ConfigParser.parse(config_file)
        logger.info(f"Pipeline '{self.config.get('name', 'Unknown')}' loaded successfully")
    
    def run(self):
        """Run the pipeline"""
        if not self.config:
            logger.error("No configuration loaded")
            return
        
        logger.info(f"Starting pipeline: {self.config.get('name', 'Unknown')}")
        
        # Set variables
        variables = self.config.get('variables', {})
        for key, value in variables.items():
            self.data_context.set_variable(key, value)
        
        # Execute action sequence
        actions = self.config.get('actions', [])
        for i, action_config in enumerate(actions):
            logger.info(f"Executing action {i+1}/{len(actions)}")
            success = self.action_executor.execute_action(action_config)
            if not success:
                logger.error("Pipeline terminated due to action failure")
                return
        
        logger.info("Pipeline execution completed successfully")