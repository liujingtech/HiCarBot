import sys
import os

# Add the hicarbot directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'hicarbot'))

from hicarbot.main import main

if __name__ == "__main__":
    # Change to the hicarbot directory to ensure relative paths work correctly
    os.chdir(os.path.join(os.path.dirname(__file__), 'hicarbot'))
    main()