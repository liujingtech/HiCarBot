# 流水线功能架构设计

## 1. 流水线的基本结构和组件

### 核心组件包括：
- **Pipeline Engine（流水线引擎）**：核心调度器，负责解析配置、执行动作和管理状态
- **Action Executor（动作执行器）**：执行具体动作的组件
- **Data Context（数据上下文）**：存储和传递动作间的数据
- **Configuration Parser（配置解析器）**：解析JSON/YAML配置文件

## 2. 支持的动作类型

1. **OCR识别动作 (OCR Action)**：对屏幕截图进行OCR识别
2. **点击动作 (Click Action)**：在指定坐标或文本位置执行点击
3. **等待动作 (Wait Action)**：暂停执行指定时间
4. **输入动作 (Input Action)**：输入文本内容
5. **条件判断动作 (Condition Action)**：根据条件决定执行分支

## 3. 动作之间的数据传递和状态管理

- 使用`DataContext`类存储变量和OCR结果
- 支持变量引用和表达式计算
- 提供执行历史记录和状态跟踪

## 4. 配置文件格式设计

支持JSON和YAML两种格式，包含：
- 流水线名称、版本和描述
- 变量定义
- 动作序列定义
- 每个动作的参数配置

## 5. 错误处理和重试机制

- 每个动作支持配置重试策略（最大尝试次数、延迟时间）
- 统一的异常处理和日志记录
- 失败时的优雅降级处理

## 6. 日志记录和执行状态跟踪

- 多级别日志记录（DEBUG、INFO、WARN、ERROR）
- 执行进度跟踪
- 详细的执行状态报告

## 文件结构

```
HiCarBot/
├── actions.py              # 动作实现模块
├── config_parser.py        # 配置解析器
├── login_pipeline.yaml     # 示例流水线配置
├── main.py                 # 主入口点
├── pipeline_design.md      # 架构设计文档
├── pipeline_engine.py      # 核心流水线引擎
├── requirements.txt        # 依赖包列表
├── README.md              # 项目说明文档
└── test_pipeline.py        # 测试脚本
```

## 使用方法

1. 安装依赖：`pip install -r requirements.txt`
2. 编写流水线配置文件（YAML或JSON格式）
3. 运行流水线：`python main.py pipeline_config.yaml`

该架构具有良好的扩展性，可以轻松添加新的动作类型，支持复杂的自动化流程编排。