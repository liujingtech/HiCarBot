import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from hicarbot.main import main

if __name__ == "__main__":
    main()