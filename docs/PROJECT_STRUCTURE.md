# Therapy Agent 项目结构

以下是Therapy Agent项目的完整目录结构，整理自项目根目录：

```
/Users/liuyanjun/therapy_agent/
├── .claude/                     # Claude相关配置
├── 2025-08-23-this-session-is-being-continued-from-a-previous-co.txt
├── CLAUDE.md
├── INTEGRATION_SUMMARY.md       # 集成摘要文档
├── LICENSE.md                   # 许可证信息
├── PROGRAM_FLOW_DESCRIPTION.md  # 程序流程描述
├── README.md                    # 项目说明
├── STARTUP_GUIDE.md             # 启动指南
├── model/                       # 模型相关代码
│   ├── .env                     # 环境变量配置
│   ├── EmpatheticPersonas.csv   # 共情角色数据
│   ├── LLM_CONFIGURATION.md     # LLM配置文档
│   ├── README.md
│   ├── __init__.py
│   ├── __pycache__/             # Python编译缓存
│   ├── app.db                   # 应用数据库
│   ├── classifiers.py           # 分类器实现
│   ├── companion_enhancer.py    # 陪伴增强器
│   ├── config.py                # 配置文件
│   ├── countries.py             # 国家相关数据
│   ├── flask_backend_with_aws.py # Flask后端与AWS集成
│   ├── inspirational_cards.py   # 励志卡片生成
│   ├── llm_integration.py       # LLM集成模块
│   ├── mcp_integration.py
│   ├── memory_integration.py    # 记忆集成
│   ├── migrations/              # 数据库迁移
│   ├── models.py                # 数据模型
│   ├── rag_system.py            # RAG系统
│   ├── requirements.txt         # 项目依赖
│   ├── rule_based_model.py      # 规则基础模型
│   ├── test_add_data.py         # 数据添加测试
│   ├── test_add_data_flask.py   # Flask数据添加测试
│   ├── test_final_integration.py # 最终集成测试
│   ├── test_memory_integration.py # 记忆集成测试
│   ├── test_new_features_integration.py # 新功能集成测试
│   ├── test_run.py              # 运行测试
│   ├── test_satbot_memory.py    # Satbot记忆测试
│   ├── tokenizer/               # 分词器
│   ├── tts_service.py           # 文本转语音服务
│   └── wsgi.py                  # WSGI入口
├── satbot_flowchart.svg         # Satbot流程图
├── start_all.sh                 # 启动所有服务脚本
├── start_backend.py             # 启动后端脚本
├── test_ai_companion_features.py # AI陪伴功能测试
├── test_api_endpoints.py        # API端点测试
├── test_integration_simple.py   # 简单集成测试
├── test_new_features.py         # 新功能测试
├── verify_features.py           # 功能验证
└── view/                        # 前端视图
    ├── README.md
    ├── package-lock.json
    ├── package.json
    ├── preview.png
    ├── public/                  # 公共资源
    └── src/                     # 源代码
        ├── ActionProvider.js
        ├── App.css
        ├── App.js
        ├── MessageParser.js
        ├── config.js
        ├── index.js
        └── widgets/             # 组件
```

## 目录说明

- **根目录**：包含项目文档、启动脚本和测试文件
- **model/**：包含后端模型、服务和数据库相关代码
  - **migrations/**：数据库迁移文件
  - **tokenizer/**：自然语言处理分词器
- **view/**：前端React应用代码
  - **public/**：静态资源
  - **src/**：React源代码和组件

这个结构展示了项目的主要组成部分，包括模型层、前端视图和各种测试文件。