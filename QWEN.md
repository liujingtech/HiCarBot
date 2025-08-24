# HiCarBot - Android自动化测试工具

## 项目概述

HiCarBot是一个现代化的Android自动化测试工具，通过流水线配置实现复杂的自动化操作流程。它能够模拟用户在Android设备上的操作，如点击、输入、等待等，并通过直接UI操作技术实现可靠高效的自动化测试。

主要技术栈：
- Python 3.x
- uiautomator2 (UI自动化)
- OpenCV (图像处理)
- ADB (Android调试桥)
- YAML (配置文件格式)

## 现代化项目结构

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
├── run.py                   # 简单运行脚本
└── README.md                # 项目说明文档
```

## 核心组件

### 流水线引擎 (Pipeline Engine)
位于 `hicarbot/engine/pipeline_engine.py`，是自动化流程的核心调度器，负责：
- 解析配置文件
- 执行动作序列
- 管理执行状态和数据上下文

### 动作系统 (Action System)
位于 `hicarbot/actions/`，提供具体的动作实现：
- Simple Bluetooth Toggle Action (MVP实现)

### 配置解析器 (Config Parser)
位于 `hicarbot/engine/pipeline_engine.py`，负责解析YAML配置文件。

## 安装和运行

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行项目
```bash
# 方法1: 使用run.py入口
python run.py <pipeline_config.yaml>

# 方法2: 直接运行主模块
python hicarbot/main.py <pipeline_config.yaml>
```

### 连接Android设备
确保已安装ADB工具并添加到系统PATH中，Android设备已连接并启用USB调试。

## 配置文件格式

支持YAML格式的配置文件，包含以下主要部分：

```yaml
name: "流水线名称"
version: "版本号"
description: "描述信息"

variables:
  key: "value"  # 变量定义

actions:
  - name: "动作名称"
    type: "动作类型"
    params:
      # 动作参数
```

### 支持的动作类型
1. **simple_bluetooth_toggle**: 打开蓝牙设置并确保已开启 (MVP实现)

## 开发指南

### 添加新的动作类型
1. 在 `hicarbot/actions/` 中创建新的动作类，继承自 `Action` 基类
2. 实现 `execute` 方法
3. 在 `hicarbot/engine/pipeline_engine.py` 中注册新动作类型

### 运行测试
目前未实现自动化测试，推荐手动测试。

## 示例配置

### MVP蓝牙开关控制
```yaml
name: "MVP蓝牙开关控制"
version: "1.0"
description: "最小化蓝牙开关控制 - 打开蓝牙设置并确保已开启"

actions:
  - name: "打开蓝牙并确保开启"
    type: "simple_bluetooth_toggle"
```

## 常用命令

1. **查看连接的Android设备**:
   ```bash
   adb devices
   ```

2. **获取设备屏幕尺寸**:
   ```bash
   adb shell wm size
   ```

3. **运行示例流水线**:
   ```bash
   python run.py examples/mvp_bluetooth_toggle.yaml
   ```

## 贡献指南

欢迎提交Issue和Pull Request来改进HiCarBot项目。

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 许可证

本项目采用MIT许可证。