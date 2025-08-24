import sys
import os
# Add the parent directory to the Python path to allow imports from subdirectories
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.pipeline_engine import PipelineEngine

def main():
    if len(sys.argv) < 2:
        print("使用方法: python main.py <pipeline_config.yaml>")
        return
    
    config_file = sys.argv[1]
    
    # 创建并运行流水线引擎
    engine = PipelineEngine()
    engine.load_config(config_file)
    engine.run()

if __name__ == "__main__":
    main()