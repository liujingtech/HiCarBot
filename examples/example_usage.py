"""
Example usage of the pipeline engine with OCR functionality
"""

from pipeline_engine import PipelineEngine


def run_example():
    """Run an example pipeline"""
    print("Running OCR and Click Automation Pipeline Example")
    print("=" * 50)
    
    # Create a pipeline engine with our example configuration
    engine = PipelineEngine("login_pipeline.yaml")
    
    # Execute the pipeline
    success = engine.execute()
    
    if success:
        print("\nPipeline executed successfully!")
    else:
        print("\nPipeline execution failed!")


if __name__ == "__main__":
    run_example()