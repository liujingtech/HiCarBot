#!/usr/bin/env python3
"""
HiCarBot Runner
Simple runner for the HiCarBot automation framework.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hicarbot.main import main

if __name__ == "__main__":
    # Call the main function from hicarbot.main
    sys.exit(main())