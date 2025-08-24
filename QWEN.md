# HiCarBot - Android自动化测试工具

## 项目概述

HiCarBot是一个基于OCR识别的Android设备自动化测试工具，支持通过流水线配置实现复杂的自动化操作流程。它能够模拟用户在Android设备上的操作，如点击、输入、等待等，并通过OCR技术识别屏幕内容，实现智能化的自动化测试。

主要技术栈：
- Python 3.x
- pponnxcr (OCR识别库)
- OpenCV (图像处理)
- ADB (Android调试桥)
- YAML (配置文件格式)

## 项目结构

```
HiCarBot/
├── hicarbot/                 # 主源代码目录
│   ├── core/                 # 核心功能模块
│   ├── automation/           # 自动化流程配置文件
│   ├── config/               # 配置管理
│   ├── ocr/                  # OCR相关功能
│   ├── utils/                # 工具函数
│   └── resources/            # 资源文件
├── docs/                     # 文档目录
├── examples/                 # 使用示例
├── tests/                    # 测试文件
├── scripts/                  # 脚本文件
├── data/                     # 数据文件
├── requirements.txt          # 依赖包列表
├── run.py                   # 项目运行入口
└── README.md                # 项目说明文档
```

## 核心组件

### 流水线引擎 (Pipeline Engine)
位于 `hicarbot/core/pipeline_engine.py`，是自动化流程的核心调度器，负责：
- 解析配置文件
- 执行动作序列
- 管理执行状态和数据上下文

### 动作执行器 (Action Executor)
位于 `hicarbot/core/actions.py`，提供具体的动作实现：
- OCR识别动作
- 点击动作
- 等待动作
- 输入动作
- 条件判断动作

### 配置解析器 (Config Parser)
位于 `hicarbot/config/config_parser.py`，负责解析YAML/JSON格式的配置文件。

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
1. **ocr**: 截图并进行OCR识别
2. **click_text**: 点击指定文本
3. **click_position**: 点击指定坐标
4. **input**: 输入文本
5. **wait**: 等待指定时间
6. **set_variable**: 设置变量

## 开发指南

### 添加新的动作类型
1. 在 `hicarbot/core/actions.py` 中创建新的动作类，继承自 `Action` 基类
2. 实现 `execute` 方法
3. 在 `hicarbot/core/pipeline_engine.py` 中注册新动作类型

### 运行测试
```bash
python -m pytest tests/
```

或运行特定测试文件：
```bash
python tests/test_pipeline.py
```

## 示例配置

### 登录流程测试
```yaml
name: "登录流程测试"
version: "1.0"
description: "测试Android应用的登录流程"

variables:
  username: "testuser"
  password: "testpass123"

actions:
  - name: "截图并OCR识别"
    type: "ocr"
  
  - name: "点击用户名输入框"
    type: "click_text"
    params:
      text: "用户名"
  
  - name: "输入用户名"
    type: "input"
    params:
      text: "{{username}}"
  
  - name: "点击密码输入框"
    type: "click_text"
    params:
      text: "密码"
  
  - name: "输入密码"
    type: "input"
    params:
      text: "{{password}}"
  
  - name: "点击登录按钮"
    type: "click_text"
    params:
      text: "登录"
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
   python run.py hicarbot/automation/login_pipeline.yaml
   ```

## 贡献指南

欢迎提交Issue和Pull Request来改进HiCarBot项目。

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 许可证

本项目采用 [LICENSE](LICENSE) 许可证。