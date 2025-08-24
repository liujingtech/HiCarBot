# HiCarBot - Modern Android Automation Framework

HiCarBot is a modern Android automation framework designed with simplicity and reliability in mind. It focuses on direct UI manipulation rather than complex OCR processing, making it fast and accurate.

## Key Features

- **Direct UI Manipulation**: Uses UIAutomator2 for reliable UI element interaction
- **Minimal Dependencies**: Only essential libraries for maximum stability
- **Clean Architecture**: Well-organized modular structure
- **Easy to Use**: Simple YAML configuration for defining automation flows
- **Fast Execution**: No OCR processing overhead

## Installation

```bash
pip install -r requirements.txt
```

Make sure you have ADB installed and added to your system PATH.

## Prerequisites

Before using HiCarBot, ensure:

1. **Android device connected** via USB with USB debugging enabled
2. **Device screen unlocked** - automation requires visible UI elements
3. **Bluetooth settings accessible** - the app needs permission to access Bluetooth settings

## Usage

1. Connect your Android device and enable USB debugging
2. Ensure the device screen is unlocked
3. Run the automation pipeline:
   ```bash
   python run.py <pipeline_config.yaml>
   ```

Or directly:
```bash
python hicarbot/main.py <pipeline_config.yaml>
```

## Example

### MVP Bluetooth Toggle

The simplest and most reliable way to ensure Bluetooth is enabled:

```yaml
name: "MVP Bluetooth Toggle"
version: "1.0"
description: "Minimal Bluetooth toggle - Open Bluetooth settings and ensure it's enabled"

actions:
  - name: "Open Bluetooth and ensure enabled"
    type: "simple_bluetooth_toggle"
```

Run it with:
```bash
python run.py examples/mvp_bluetooth_toggle.yaml
```

This will:
1. Open the Bluetooth settings page
2. Check if Bluetooth is enabled
3. If not enabled, automatically toggle the switch to enable it

## Project Structure

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
└── run.py                    # Simple runner script
```

## Development

### Adding New Actions

1. Create a new action class in `hicarbot/actions/`
2. Inherit from the base `Action` class
3. Implement the `execute` method
4. Register the action in `hicarbot/engine/pipeline_engine.py`

### Running Tests

Currently no automated tests are implemented. Manual testing is recommended.

## Contributing

Contributions are welcome! Please submit issues and pull requests to improve HiCarBot.

## License

This project is licensed under the MIT License.