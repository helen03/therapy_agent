# LLM 集成部署指南

本文档提供了将 Therapy Agent 从基于规则的系统迁移到大语言模型（LLM）的完整部署指南。

## 🚀 主要变更

### 架构变更
1. **移除了规则引擎**：不再使用 `rule_based_model.py` 的决策逻辑
2. **新增 LLM 服务**：`LLMTherapyService` 处理所有治疗对话
3. **统一的 API 端点**：所有客户端使用相同的聊天接口
4. **增强的情感分析**：实时情绪检测和危机处理

### 新增功能
1. **智能对话**：基于 LLM 的自然语言处理
2. **情感分析**：实时情绪识别和响应
3. **危机干预**：自动检测和处理危机情况
4. **上下文记忆**：跨会话的对话历史管理
5. **多模态支持**：支持文本、情感和上下文输入

## 📋 部署步骤

### 1. 环境配置

```bash
# 设置环境变量
export OPENAI_API_KEY="your-openai-api-key"  # 如果使用 OpenAI
export LLM_MODEL_TYPE="huggingface"         # 或 "openai"
export LLM_MODEL_NAME="gpt2"                # 或其他模型名称

# 或者创建 .env 文件
echo "OPENAI_API_KEY=your-openai-api-key" > backend/.env
echo "LLM_MODEL_TYPE=huggingface" >> backend/.env
echo "LLM_MODEL_NAME=gpt2" >> backend/.env
```

### 2. 依赖安装

```bash
# 安装新的依赖
cd backend
pip install -r requirements.txt

# 如果需要 OpenAI 支持
pip install openai

# 如果需要其他模型
pip install transformers torch
```

### 3. 数据库迁移（可选）

```bash
# 如果数据库结构有变化
flask db migrate -m "add_llm_support"
flask db upgrade
```

### 4. 启动服务

```bash
# 启动后端服务
flask run --host=0.0.0.0 --port=5000

# 或者使用生产模式
gunicorn -w 4 -b 0.0.0.0:5000 "backend:create_app()"
```

### 5. 测试集成

```bash
# 运行集成测试
python test_llm_integration.py

# 测试 API 端点
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好，我今天心情不好", "session_id": "test", "user_id": "test"}'
```

## 🔧 配置选项

### LLM 模型配置

```python
# 支持的模式
MODEL_TYPES = ["huggingface", "openai"]

# HuggingFace 模型选项
HUGGINGFACE_MODELS = ["gpt2", "microsoft/DialoGPT-medium", "facebook/blenderbot-400M-distill"]

# OpenAI 模型选项  
OPENAI_MODELS = ["gpt-3.5-turbo", "gpt-4"]
```

### 环境变量

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `OPENAI_API_KEY` | OpenAI API 密钥 | 无 |
| `LLM_MODEL_TYPE` | 模型类型 | `huggingface` |
| `LLM_MODEL_NAME` | 模型名称 | `gpt2` |
| `MAX_RESPONSE_LENGTH` | 最大响应长度 | `300` |
| `TEMPERATURE` | 生成温度 | `0.7` |

## 📱 客户端更新

### Android 应用
- 更新了 API 端点路径
- 增加了错误处理
- 支持新的响应格式

### 微信小程序  
- 使用统一的 `/api/chat` 端点
- 支持用户 ID 和会话管理
- 增强的错误处理

### Web 前端
- 保持向后兼容
- 自动使用新的 LLM 服务
- 支持情感显示选项

## 🧪 API 端点

### 主要端点

1. **聊天端点** `POST /api/chat`
   ```json
   {
     "message": "用户消息",
     "session_id": "会话ID", 
     "user_id": "用户ID"
   }
   ```

2. **移动登录** `POST /api/mobile_login`
   ```json
   {
     "username": "用户名",
     "avatar": "头像URL"
   }
   ```

3. **会话更新** `POST /api/update_session` (向后兼容)

### 响应格式

```json
{
  "success": true,
  "response": "AI回复内容",
  "options": ["选项1", "选项2", "选项3"],
  "emotion": "happy",
  "requires_followup": false,
  "session_id": "会话ID",
  "user_id": "用户ID"
}
```

## 🔍 监控和日志

### 日志配置

```python
# 在 backend/__init__.py 中配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s : %(message)s"
)
```

### 关键监控指标

1. **LLM 响应时间**：监控生成延迟
2. **情感分析准确率**：跟踪情绪识别
3. **危机检测**：记录危机干预事件
4. **API 错误率**：监控服务健康状态

## 🚨 危机处理

### 自动检测
系统会自动检测以下危机情况：
- 自杀倾向表达
- 严重情绪困扰  
- 紧急求助信号

### 响应流程
1. 情感分析检测危机信号
2. 生成紧急响应内容
3. 提供危机资源信息
4. 记录危机事件日志

## 📊 性能优化

### 缓存策略
```python
# 对话历史缓存
self.conversation_histories: Dict[str, List[Dict]] = {}

# 模型缓存  
_llm_instance = None  # 单例模式
```

### 批处理优化
- 情感分析批处理
- 响应生成优化
- 内存管理优化

## 🔧 故障排除

### 常见问题

1. **LLM 初始化失败**
   ```bash
   # 检查模型文件
   # 检查网络连接
   # 验证 API 密钥
   ```

2. **响应时间过长**
   ```bash
   # 调整 max_length 参数
   # 使用更小的模型
   # 启用缓存
   ```

3. **情感分析不准确**
   ```bash
   # 检查情感分析模型
   # 验证输入文本预处理
   ```

### 调试模式

```bash
# 启用详细日志
export LOG_LEVEL=DEBUG

# 测试单个功能
python -c "from backend.models.llm_integration import get_llm; llm = get_llm(); print(llm.analyze_emotion('测试文本'))"
```

## 🎯 生产部署

### Docker 部署

```dockerfile
# 使用官方 Python 镜像
FROM python:3.9-slim

# 安装依赖
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制代码
COPY . .

# 启动服务
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend:create_app()"]
```

### Kubernetes 部署

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: therapy-agent
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: therapy-agent
        image: therapy-agent:latest
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: therapy-secrets
              key: openai-api-key
```

## 📈 性能基准

### 预期性能
- **响应时间**: < 2秒 (本地模型), < 1秒 (OpenAI)
- **并发支持**: 50+ 并发用户
- **准确率**: 85%+ 情感识别准确率

### 监控指标
- CPU 使用率
- 内存使用量  
- API 响应时间
- 错误率

## 🔮 未来扩展

### 计划功能
1. **多语言支持**：国际化响应生成
2. **语音交互**：语音输入输出集成
3. **个性化模型**：用户特定的微调
4. **多模态输入**：支持图像和语音情感分析

### 技术路线
1. **模型优化**：量化、蒸馏、剪枝
2. **缓存优化**：向量数据库集成
3. **边缘计算**：端侧模型部署
4. **联邦学习**：隐私保护训练

---

**注意**：在生产环境部署前，请进行充分的测试和验证，确保所有功能正常工作并满足性能要求。