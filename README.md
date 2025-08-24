# HiCarBot - 现代化Android自动化测试框架

HiCarBot是一个现代化的Android自动化测试框架，设计注重简洁性和可靠性。它专注于直接UI操作而非复杂的OCR处理，使其快速且准确。

## 核心特性

- **直接UI操作**：使用UIAutomator2进行可靠的UI元素交互
- **最小依赖**：只包含必要的库以保证最大稳定性
- **清晰架构**：良好组织的模块化结构
- **易于使用**：简单的YAML配置定义自动化流程
- **快速执行**：无OCR处理开销

## 安装依赖

```bash
pip install -r requirements.txt
```

确保已安装ADB并添加到系统PATH中。

## 前提条件

使用HiCarBot之前，请确保：

1. **Android设备已连接**：通过USB连接并启用USB调试
2. **设备屏幕已解锁**：自动化需要可见的UI元素
3. **蓝牙设置可访问**：应用需要访问蓝牙设置的权限

## 使用方法

1. 连接Android设备并启用USB调试
2. 确保设备屏幕已解锁
3. 运行自动化流水线：
   ```bash
   python run.py <pipeline_config.yaml>
   ```

或者直接运行：
```bash
python hicarbot/main.py <pipeline_config.yaml>
```

## 示例

### MVP蓝牙开关控制

最简单可靠的蓝牙开启方式：

```yaml
name: "MVP蓝牙开关控制"
version: "1.0"
description: "最小化蓝牙开关控制 - 打开蓝牙设置并确保已开启"

actions:
  - name: "打开蓝牙并确保开启"
    type: "simple_bluetooth_toggle"
```

运行方式：
```bash
python run.py examples/mvp_bluetooth_toggle.yaml
```

该操作将：
1. 打开蓝牙设置页面
2. 检查蓝牙是否已开启
3. 如果未开启，自动切换开关以开启蓝牙

## 项目结构

```
HiCarBot/
├── hicarbot/                 # 主源代码目录
│   ├── __init__.py           # 包初始化文件
│   ├── main.py               # 主入口点
│   ├── actions/              # 动作实现模块
│   │   ├── __init__.py
│   │   └── simple_bluetooth.py  # 简单蓝牙切换动作
│   ├── engine/               # 核心执行引擎
│   │   ├── __init__.py
│   │   └── pipeline_engine.py  # 流水线执行引擎
│   ├── models/               # 数据模型
│   │   ├── __init__.py
│   │   └── models.py         # 核心数据结构
│   └── utils/                # 工具函数
│       ├── __init__.py
├── examples/                 # 示例配置
│   └── mvp_bluetooth_toggle.yaml  # MVP蓝牙切换示例
├── requirements.txt         # Python依赖
└── run.py                    # 简单运行脚本
```

## 开发指南

### 添加新动作

1. 在`hicarbot/actions/`中创建新的动作类
2. 继承基础`Action`类
3. 实现`execute`方法
4. 在`hicarbot/engine/pipeline_engine.py`中注册动作

### 运行测试

目前未实现自动化测试，推荐手动测试。

## 贡献

欢迎提交Issue和Pull Request来改进HiCarBot项目。

## 许可证

本项目采用MIT许可证。