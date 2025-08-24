# HiCarBot - Android自动化测试工具

HiCarBot是一个基于OCR识别的Android设备自动化测试工具，支持通过流水线配置实现复杂的自动化操作流程。

## 功能特性

- OCR文字识别
- 自动化点击
- 流水线编排
- 多种动作支持

## 安装依赖

```bash
pip install -r requirements.txt
```

确保已安装ADB工具并添加到系统PATH中。

## 使用方法

1. 连接Android设备并启用USB调试
2. 确保设备屏幕已解锁
3. 编写流水线配置文件（YAML格式）
4. 运行流水线：
   ```bash
   python run.py <pipeline_config.yaml>
   ```

## 动作类型

1. **ocr**：截图并进行OCR识别
2. **click_text**：点击指定文本
3. **click_position**：点击指定坐标
4. **input**：输入文本
5. **wait**：等待指定时间
6. **open_bluetooth**：打开蓝牙设置页面
7. **simple_bluetooth_toggle**：打开蓝牙设置页面并确保蓝牙已开启

## 示例

### MVP蓝牙开关控制

```yaml
name: "MVP蓝牙开关控制"
version: "1.0"
description: "最简化的蓝牙开关控制 - 打开蓝牙设置页面并确保蓝牙已开启"

actions:
  - name: "打开蓝牙并确保开启"
    type: "simple_bluetooth_toggle"
```

## 项目结构

```
HiCarBot/
├── hicarbot/                 # 主源代码目录
│   ├── core/                 # 核心功能模块
├── examples/                 # 使用示例
└── requirements.txt          # 依赖包列表
```