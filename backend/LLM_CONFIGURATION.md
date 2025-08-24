# LLM 集成配置说明

本文档详细介绍了 Therapy Agent 项目中如何配置和使用大语言模型(LLM)集成模块，该模块用于替换原有的BERT类模型。

## 概述

LLM 集成模块提供了一个统一的接口，可以使用不同类型的大语言模型来进行情感分析、意图识别和文本生成等任务。当前支持两种模型类型：

1. **Hugging Face 本地模型** - 适用于本地运行的开源模型
2. **OpenAI API** - 适用于访问OpenAI的云端模型服务

## 配置方法

### 环境变量配置

您可以通过设置环境变量来配置LLM集成模块的行为：

| 环境变量名 | 描述 | 默认值 | 示例值 |
|------------|------|--------|--------|
| `LLM_MODEL_TYPE` | 模型类型 (huggingface 或 openai) | `huggingface` | `openai` |
| `LLM_MODEL_NAME` | Hugging Face 模型名称 | `gpt2` | `meta-llama/Llama-2-7b-chat-hf` |
| `OPENAI_API_KEY` | OpenAI API 密钥 (使用OpenAI模型时必需) | 无 | `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |

### `.env` 文件配置

您可以在 `model/.env` 文件中设置上述环境变量，例如：

```
# 使用OpenAI API
LLM_MODEL_TYPE=openai
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 或使用Hugging Face本地模型
# LLM_MODEL_TYPE=huggingface
# LLM_MODEL_NAME=gpt2
```

## 功能说明

LLM集成模块提供以下主要功能：

### 1. 情感分析 (`analyze_emotion`)

分析用户文本中的情感，返回标准化的情感标签。支持的情感包括：
- happy, sad, angry, anxious, jealous, guilty, ashamed, envious
- disgusted, disappointed, loving, insecure, neutral

### 2. 意图识别 (`analyze_intention`)

分析用户文本中是否包含自杀意图，返回：
- `s` - 表示有自杀意图
- `not_s` - 表示没有自杀意图

### 3. 语义相似度计算 (`get_semantic_similarity`)

计算两个文本之间的语义相似度，返回0-1之间的分数，其中0表示完全不相似，1表示完全相同。

### 4. 文本生成 (`generate_response`)

根据输入提示生成自然语言响应。

### 5. 上下文增强 (`enhance_with_context`)

使用对话历史来增强当前提示，使模型能够生成更连贯的响应。

## 使用示例

在项目代码中使用LLM集成模块非常简单：

```python
from model.llm_integration import get_llm

# 获取LLM实例
llm = get_llm()

# 分析情感
emotion = llm.analyze_emotion("我感到非常难过和绝望")
print(f"识别到的情感: {emotion}")

# 分析意图
intention = llm.analyze_intention("我觉得活着没有意义")
print(f"意图分析结果: {intention}")

# 计算语义相似度
similarity = llm.get_semantic_similarity("我感到很伤心", "我情绪很低落")
print(f"语义相似度: {similarity}")

# 生成响应
response = llm.generate_response("如何应对焦虑情绪?")
print(f"生成的响应: {response}")
```

## 性能和回退机制

LLM集成模块设计了多层回退机制，以确保即使在模型加载失败或API调用出错的情况下，系统仍能正常工作：

1. 如果无法加载主模型，将自动尝试使用回退模型
2. 如果回退模型也无法加载，将使用基于规则的简单实现
3. 所有API调用都包含异常处理，确保系统不会崩溃

## 安装依赖

使用LLM集成模块需要安装以下依赖：

```bash
# 在model目录下执行
pip install -r requirements.txt
```

如果您计划使用特定的Hugging Face模型，可能还需要安装额外的依赖，例如：

```bash
pip install transformers torch accelerate
```

## 注意事项

1. 使用OpenAI API时，请确保您的API密钥安全存储，不要将其硬编码在代码中
2. 使用大型Hugging Face模型时，请注意您的硬件资源限制，某些模型可能需要GPU支持
3. 对于生产环境，建议使用更复杂的意图识别和情感分析模型，当前实现提供了基础功能
4. 如有性能问题，可以考虑使用缓存机制来减少重复的API调用

## 故障排除

如果遇到LLM集成相关的问题，请检查以下几点：

1. 环境变量是否正确设置
2. 依赖包是否已正确安装
3. API密钥(如使用OpenAI)是否有效
4. 查看日志以获取详细错误信息

如有其他问题，请参考项目文档或联系技术支持。