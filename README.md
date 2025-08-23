# HiCarBot - Android自动化测试工具

HiCarBot是一个基于OCR识别的Android设备自动化测试工具，支持通过流水线配置实现复杂的自动化操作流程。

## 功能特性

1. **OCR文字识别**：使用pponnxcr库进行高效的OCR识别
2. **自动化点击**：根据OCR识别结果自动点击指定文本
3. **流水线编排**：通过YAML配置文件编排复杂的操作流程
4. **变量支持**：支持在配置文件中使用变量
5. **多种动作**：支持OCR识别、点击、输入、等待等多种动作

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. 编写流水线配置文件（YAML格式）
2. 运行流水线：
   ```bash
   python main.py login_pipeline.yaml
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
    type: "动作类型"  # ocr, click_text, click_position, input, wait, set_variable
    params:
      # 动作参数
```

## 动作类型

1. **ocr**：截图并进行OCR识别
2. **click_text**：点击指定文本
3. **click_position**：点击指定坐标
4. **input**：输入文本
5. **wait**：等待指定时间
6. **set_variable**：设置变量

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
```

### 2. 百度文章搜索与收藏

查看 `baidu_article_search_pipeline.yaml` 文件了解详细配置。
更多说明请参考 `baidu_automation_task.md` 文档。