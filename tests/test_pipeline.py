"""
Test script to verify the pipeline engine functionality
"""

import os
import sys

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Try to import the pipeline engine
    from pipeline_engine import PipelineEngine
    print("Pipeline engine imported successfully!")
    
    # Check if the example config file exists
    if os.path.exists("login_pipeline.yaml"):
        print("Example configuration file found!")
        
        # Try to create a pipeline engine instance (without executing)
        try:
            engine = PipelineEngine("login_pipeline.yaml")
            print(f"Pipeline engine created successfully!")
            print(f"Pipeline name: {engine.config.get('name', 'Unnamed')}")
            print(f"Number of actions: {len(engine.actions)}")
        except Exception as e:
            print(f"Error creating pipeline engine: {e}")
    else:
        print("Example configuration file not found!")
        
except ImportError as e:
    print(f"Failed to import pipeline engine: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")