# HiCarBot项目工程结构设计

```
HiCarBot/
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
├── .gitignore
├── .env.example
├── hicarbot/
│   ├── __init__.py
│   ├── __main__.py
│   ├── main.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── config_parser.py
│   │   └── settings.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── pipeline_engine.py
│   │   └── actions.py
│   ├── automation/
│   │   ├── __init__.py
│   │   ├── login_pipeline.yaml
│   │   └── baidu_article_search_pipeline.yaml
│   ├── ocr/
│   │   ├── __init__.py
│   │   └── screenshot_ocr.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── resources/
│       ├── screenshots/
│       └── templates/
├── tests/
│   ├── __init__.py
│   ├── test_pipeline.py
│   ├── test_pponnxcr.py
│   ├── test_config/
│   ├── test_core/
│   ├── test_automation/
│   └── test_ocr/
├── docs/
│   ├── pipeline_design.md
│   ├── baidu_automation_task.md
│   ├── architecture.md
│   └── usage.md
├── examples/
│   └── example_usage.py
├── scripts/
│   └── deploy.sh
└── data/
    └── sample_data/
```

## 各目录和文件的用途说明

### 根目录文件
- **LICENSE**: 项目的许可证文件
- **README.md**: 项目介绍、使用说明和快速开始指南
- **requirements.txt**: 项目依赖包列表
- **setup.py**: 项目的安装和打包配置文件
- **.gitignore**: Git版本控制忽略文件配置
- **.env.example**: 环境变量配置示例文件

### hicarbot/ (主源代码目录)
这是项目的主要Python包目录：

- **__init__.py**: 包初始化文件，使目录成为Python包
- **__main__.py**: 允许包作为脚本直接运行的入口点
- **main.py**: 程序主入口文件

#### config/ (配置管理)
- **config_parser.py**: 配置文件解析器
- **settings.py**: 应用设置和常量定义

#### core/ (核心功能)
- **pipeline_engine.py**: 自动化流程引擎核心
- **actions.py**: 自动化操作动作定义

#### automation/ (自动化流程)
- **login_pipeline.yaml**: 登录自动化流程配置
- **baidu_article_search_pipeline.yaml**: 百度文章搜索自动化流程配置

#### ocr/ (光学字符识别)
- **screenshot_ocr.py**: 截图OCR识别功能

#### utils/ (工具函数)
- 存放通用工具函数和辅助类

#### resources/ (资源文件)
- **screenshots/**: 存放截图示例或测试用截图
- **templates/**: 存放模板文件

### tests/ (测试文件)
- **test_pipeline.py**: 流程引擎测试
- **test_pponnxcr.py**: OCR功能测试
- 其他子目录对应源代码的模块结构，便于组织测试文件

### docs/ (文档)
- **pipeline_design.md**: 流程设计文档
- **baidu_automation_task.md**: 百度自动化任务说明
- **architecture.md**: 系统架构文档
- **usage.md**: 使用指南文档

### examples/ (示例代码)
- **example_usage.py**: 使用示例代码

### scripts/ (脚本文件)
- 存放部署、构建等脚本文件

### data/ (数据文件)
- 存放示例数据或测试数据

这种结构遵循了Python项目的标准组织方式，具有以下优势：
1. 清晰的模块划分，便于维护和扩展
2. 分离源代码、测试、文档和资源文件
3. 符合Python包的组织规范
4. 易于进行单元测试和集成测试
5. 便于文档维护和版本控制
6. 支持通过setup.py进行包安装和分发