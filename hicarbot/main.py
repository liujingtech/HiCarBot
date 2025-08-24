#!/usr/bin/env python3
"""
HiCarBot Main Entry Point
This is the main entry point for the HiCarBot automation framework.
"""

import sys
import os
import argparse
from hicarbot.engine.pipeline_engine import PipelineEngine

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='HiCarBot - Android Automation Framework')
    parser.add_argument('config_file', help='Pipeline configuration file (YAML or JSON)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate config file
    if not os.path.exists(args.config_file):
        print(f"Error: Configuration file '{args.config_file}' not found")
        return 1
    
    # Create and run pipeline engine
    try:
        engine = PipelineEngine()
        engine.load_config(args.config_file)
        engine.run()
        return 0
    except Exception as e:
        print(f"Error: Failed to run pipeline - {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())