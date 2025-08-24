# HiCarBot - Android自动化测试工具

HiCarBot是一个基于OCR识别的Android设备自动化测试工具，支持通过流水线配置实现复杂的自动化操作流程。它可以模拟用户在Android设备上的操作，如点击、输入、等待等，并通过OCR技术识别屏幕内容，实现智能化的自动化测试。

## 功能特性

1. **OCR文字识别**：使用pponnxcr库进行高效的OCR识别，准确识别屏幕上的文字内容
2. **自动化点击**：根据OCR识别结果自动点击指定文本或坐标位置
3. **流水线编排**：通过YAML配置文件编排复杂的操作流程，支持变量和条件判断
4. **多种动作支持**：支持OCR识别、点击、输入、等待等多种自动化动作
5. **变量管理**：支持在配置文件中定义和使用变量，提高配置复用性
6. **ADB集成**：通过ADB与Android设备通信，实现设备控制

## 应用场景

- Android应用功能测试
- 用户操作流程自动化
- 重复性任务自动化执行
- 移动端UI测试
- 应用性能基准测试

## 安装依赖

```bash
pip install -r requirements.txt
```

确保已安装ADB工具并添加到系统PATH中。

## 使用方法

1. 连接Android设备并启用USB调试
2. 编写流水线配置文件（YAML格式）
3. 运行流水线：
   ```bash
   python run.py <pipeline_config.yaml>
   ```

或者直接运行：
```bash
python hicarbot/main.py <pipeline_config.yaml>
```

## 配置文件格式

```yaml
name: "流水线名称"
version: "版本号"
description: "描述信息"

variables:
  key: "value"  # 变量定义

actions:
  - name: "动作名称"
    type: "动作类型"  # ocr, click_text, click_position, input, wait
    params:
      # 动作参数
```

## 动作类型

1. **ocr**：截图并进行OCR识别
   - `region`: [x, y, width, height] - 可选，指定识别区域
   - `language`: 语言类型，默认为'zhs'(简体中文)
   - `save_to`: 保存结果的变量名

2. **click_text**：点击指定文本
   - `text`: 要点击的文本内容
   - `offset`: [x, y] - 可选，点击位置偏移量
   - `action`: 点击类型，'tap'(默认)或'long_press'

3. **click_position**：点击指定坐标
   - `position`: [x, y] - 点击的坐标位置

4. **input**：输入文本
   - `text`: 要输入的文本内容，支持变量替换

5. **wait**：等待指定时间
   - `seconds`: 等待的秒数
   
9. **check_bluetooth_status**：检查蓝牙是否开启
   - 无参数
   - 检查结果保存在变量 `is_bluetooth_enabled` 中
   
10. **enable_bluetooth**：直接启用蓝牙（无需打开设置页面）
    - 无参数
    
11. **disable_bluetooth**：直接禁用蓝牙（无需打开设置页面）
    - 无参数

## 示例

### 1. 登录流程测试

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
  
  - name: "等待登录完成"
    type: "wait"
    params:
      seconds: 3
      
  - name: "验证登录结果"
    type: "ocr"
```

### 2. 百度文章搜索与收藏

```yaml
name: "百度文章搜索与收藏"
version: "1.0"
description: "在百度App中搜索技术文章并收藏感兴趣的内容"

variables:
  search_keyword: "人工智能发展现状"

actions:
  - name: "启动百度App并截图OCR"
    type: "ocr"
  
  - name: "等待应用加载完成"
    type: "wait"
    params:
      seconds: 3
  
  - name: "点击搜索框"
    type: "click_text"
    params:
      text: "搜索"
  
  - name: "输入搜索关键词"
    type: "input"
    params:
      text: "{{search_keyword}}"
  
  - name: "点击搜索按钮"
    type: "click_text"
    params:
      text: "百度一下"
  
  - name: "等待搜索结果加载"
    type: "wait"
    params:
      seconds: 5
  
  - name: "截图检查搜索结果"
    type: "ocr"
  
  - name: "点击第一篇技术文章"
    type: "click_text"
    params:
      text: "技术"
  
  - name: "等待文章页面加载"
    type: "wait"
    params:
      seconds: 4
  
  - name: "截图文章页面"
    type: "ocr"
  
  - name: "查找并点击收藏按钮"
    type: "click_text"
    params:
      text: "收藏"
  
  - name: "等待收藏操作完成"
    type: "wait"
    params:
      seconds: 2
  
  - name: "最终截图确认收藏成功"
    type: "ocr"
```

### 3. 打开蓝牙设置

```yaml
name: "蓝牙设置测试"
version: "1.0"
description: "测试打开Android设备的蓝牙设置页面"

actions:
  - name: "打开蓝牙设置"
    type: "open_bluetooth"
  
  - name: "等待页面加载"
    type: "wait"
    params:
      seconds: 3
```

### 6. 直接控制蓝牙

```yaml
name: "直接控制蓝牙示例"
version: "1.0"
description: "直接启用或禁用蓝牙的示例"

actions:
  - name: "启用蓝牙"
    type: "enable_bluetooth"
  
  - name: "等待蓝牙启用"
    type: "wait"
    params:
      seconds: 2
  
  - name: "禁用蓝牙"
    type: "disable_bluetooth"
```

更多示例请查看 `hicarbot/automation/` 目录下的配置文件。

## 项目结构

```
HiCarBot/
├── hicarbot/                 # 主源代码目录
│   ├── core/                 # 核心功能模块
│   ├── automation/           # 自动化流程配置文件
│   └── ocr/                  # OCR相关功能
├── docs/                     # 文档目录
├── examples/                 # 使用示例
├── tests/                    # 测试文件
└── requirements.txt          # 依赖包列表
```

## 开发指南

### 添加新的动作类型

1. 在 `hicarbot/core/actions.py` 中创建新的动作类，继承自 `Action` 基类
2. 实现 `execute` 方法
3. 在 `hicarbot/core/pipeline_engine.py` 中注册新动作类型

### 运行测试

```bash
python -m pytest tests/
```

## 贡献

欢迎提交Issue和Pull Request来改进HiCarBot项目。

## 许可证

本项目采用 [LICENSE](LICENSE) 许可证。