# HiCarBot - Android Automation Testing Tool

## Project Overview

HiCarBot is a modern Android automation testing tool that enables complex automation workflows through pipeline configuration. It simulates user operations on Android devices such as clicking, inputting, and waiting, and utilizes OCR technology to intelligently automate testing processes.

Key Technologies:
- Python 3.x
- uiautomator2 (UI automation)
- OpenCV (Image processing)
- ADB (Android Debug Bridge)
- YAML (Configuration format)

## Modernized Project Structure

```
HiCarBot/
├── hicarbot/                 # Main source directory
│   ├── __init__.py           # Package initializer
│   ├── main.py               # Main entry point
│   ├── actions/              # Action implementations
│   │   ├── __init__.py
│   │   └── simple_bluetooth.py  # Simple Bluetooth toggle action
│   ├── engine/               # Core execution engine
│   │   ├── __init__.py
│   │   └── pipeline_engine.py  # Pipeline execution engine
│   ├── models/               # Data models
│   │   ├── __init__.py
│   │   └── models.py         # Core data structures
│   └── utils/                # Utility functions
│       ├── __init__.py
├── examples/                 # Example configurations
│   └── mvp_bluetooth_toggle.yaml  # Minimal Bluetooth toggle example
├── requirements.txt         # Python dependencies
├── run.py                   # Simple runner script
└── README.md                # Project documentation
```

## Core Components

### Pipeline Engine
Located at `hicarbot/engine/pipeline_engine.py`, this is the core scheduler responsible for:
- Parsing configuration files
- Executing action sequences
- Managing execution state and data context

### Action System
Located at `hicarbot/actions/`, provides concrete action implementations:
- Simple Bluetooth Toggle Action (MVP implementation)

### Configuration Parser
Located at `hicarbot/engine/pipeline_engine.py`, handles YAML configuration file parsing.

## Installation and Usage

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Project
```bash
# Method 1: Using run.py entry point
python run.py <pipeline_config.yaml>

# Method 2: Direct module execution
python hicarbot/main.py <pipeline_config.yaml>
```

### Connect Android Device
Ensure ADB tools are installed and added to system PATH, and Android device is connected with USB debugging enabled.

## Configuration File Format

Supports YAML format configuration files with the following main sections:

```yaml
name: "Pipeline Name"
version: "Version Number"
description: "Description"

variables:
  key: "value"  # Variable definitions

actions:
  - name: "Action Name"
    type: "Action Type"
    params:
      # Action parameters
```

### Supported Action Types
1. **simple_bluetooth_toggle**: Open Bluetooth settings and ensure it's enabled (MVP implementation)

## Development Guide

### Adding New Action Types
1. Create a new action class in `hicarbot/actions/`, inheriting from the `Action` base class
2. Implement the `execute` method
3. Register the action in `hicarbot/engine/pipeline_engine.py`

### Run Tests
Currently no automated tests are implemented. Manual testing is recommended.

## Example Configuration

### MVP Bluetooth Toggle
```yaml
name: "MVP Bluetooth Toggle"
version: "1.0"
description: "Minimal Bluetooth toggle - Open Bluetooth settings and ensure it's enabled"

actions:
  - name: "Open Bluetooth and ensure enabled"
    type: "simple_bluetooth_toggle"
```

## Common Commands

1. **View Connected Android Devices**:
   ```bash
   adb devices
   ```

2. **Get Device Screen Size**:
   ```bash
   adb shell wm size
   ```

3. **Run Example Pipeline**:
   ```bash
   python run.py examples/mvp_bluetooth_toggle.yaml
   ```

## Contribution Guidelines

Welcome to submit Issues and Pull Requests to improve the HiCarBot project.

1. Fork the project
2. Create a feature branch
3. Commit changes
4. Submit a Pull Request

## License

This project is licensed under the MIT License.