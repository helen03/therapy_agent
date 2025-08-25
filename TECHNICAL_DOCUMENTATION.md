# MindGuide 治疗助手技术文档

## 系统架构概述

MindGuide 是一个基于 React + Flask 的心理治疗助手系统，包含以下核心组件：

- **前端**：React 应用，使用 react-chatbot-kit 构建聊天界面
- **后端**：Flask API 服务器，提供用户认证和会话管理
- **数据库**：SQLAlchemy ORM 管理用户数据和会话记录
- **AI 服务**：LLM 集成提供治疗对话功能

## 用户注册流程

### 1. 前端注册表单提交
**文件**: <mcfile name="Login.js" path="/Users/liuyanjun/therapy_agent/frontend/src/Login.js"></mcfile> (第 250-280 行)

```javascript
const response = await axios.post(`${apiBaseUrl}/api/register`, {
  user_info: { username, password, email }
});
```

### 2. 后端注册 API 处理
**文件**: <mcfile name="__init__.py" path="/Users/liuyanjun/therapy_agent/backend/__init__.py"></mcfile> (第 65-112 行)

<mcsymbol name="register" filename="__init__.py" path="/Users/liuyanjun/therapy_agent/backend/__init__.py" startline="65" type="function"></mcsymbol> 函数处理：
- 验证输入参数
- 检查用户名和邮箱是否已存在
- 创建新用户并哈希密码
- 生成 JWT token

### 3. 密码哈希处理
**文件**: <mcfile name="models.py" path="/Users/liuyanjun/therapy_agent/backend/database/models.py"></mcfile> (第 35-45 行)

<mcsymbol name="set_password" filename="models.py" path="/Users/liuyanjun/therapy_agent/backend/database/models.py" startline="35" type="function"></mcsymbol> 方法：
- 使用 bcrypt.gensalt() 生成盐值
- 使用 bcrypt.hashpw() 哈希密码
- 存储哈希后的密码到数据库

## 用户登录流程

### 1. 前端登录请求
**文件**: <mcfile name="Login.js" path="/Users/liuyanjun/therapy_agent/frontend/src/Login.js"></mcfile> (第 230-250 行)

```javascript
const response = await axios.post(`${apiBaseUrl}/api/login`, {
  user_info: { username, password }
});
```

### 2. 后端登录验证
**文件**: <mcfile name="__init__.py" path="/Users/liuyanjun/therapy_agent/backend/__init__.py"></mcfile> (第 114-187 行)

<mcsymbol name="login" filename="__init__.py" path="/Users/liuyanjun/therapy_agent/backend/__init__.py" startline="114" type="function"></mcsymbol> 函数处理：
- 解析请求数据
- 查询用户信息
- 验证密码哈希
- 创建会话记录
- 生成 JWT token

### 3. 密码验证
**文件**: <mcfile name="models.py" path="/Users/liuyanjun/therapy_agent/backend/database/models.py"></mcfile> (第 45-50 行)

<mcsymbol name="check_password" filename="models.py" path="/Users/liuyanjun/therapy_agent/backend/database/models.py" startline="45" type="function"></mcsymbol> 方法：
- 使用 bcrypt.checkpw() 验证密码
- 返回布尔验证结果

### 4. JWT Token 生成
**文件**: <mcfile name="models.py" path="/Users/liuyanjun/therapy_agent/backend/database/models.py"></mcfile> (第 50-65 行)

<mcsymbol name="generate_auth_token" filename="models.py" path="/Users/liuyanjun/therapy_agent/backend/database/models.py" startline="50" type="function"></mcsymbol> 方法：
- 使用 jwt.encode() 生成 token
- 设置过期时间（默认 3600 秒）

## 会话管理流程

### 1. 会话初始化
**文件**: <mcfile name="llm_therapy_service.py" path="/Users/liuyanjun/therapy_agent/backend/services/llm_therapy_service.py"></mcfile> (第 25-43 行)

<mcsymbol name="initialize_session" filename="llm_therapy_service.py" path="/Users/liuyanjun/therapy_agent/backend/services/llm_therapy_service.py" startline="25" type="function"></mcsymbol> 方法：
- 创建会话键
- 初始化对话历史
- 生成初始问候语

### 2. 消息处理
**文件**: <mcfile name="llm_therapy_service.py" path="/Users/liuyanjun/therapy_agent/backend/services/llm_therapy_service.py"></mcfile> (第 45-104 行)

<mcsymbol name="process_message" filename="llm_therapy_service.py" path="/Users/liuyanjun/therapy_agent/backend/services/llm_therapy_service.py" startline="45" type="function"></mcsymbol> 方法：
- 添加用户消息到历史
- 分析情绪和意图
- 生成治疗性回复
- 管理对话上下文

### 3. API 会话更新
**文件**: <mcfile name="__init__.py" path="/Users/liuyanjun/therapy_agent/backend/__init__.py"></mcfile> (第 311-334 行)

<mcsymbol name="update_session" filename="__init__.py" path="/Users/liuyanjun/therapy_agent/backend/__init__.py" startline="311" type="function"></mcsymbol> 函数：
- 处理用户选择
- 调用 LLM 服务处理消息
- 返回聊天机器人的回复

## 前端聊天交互

### 1. 消息解析器
**文件**: <mcfile name="MessageParser.js" path="/Users/liuyanjun/therapy_agent/frontend/src/MessageParser.js"></mcfile> (第 1-60 行)

<mcsymbol name="parse" filename="MessageParser.js" path="/Users/liuyanjun/therapy_agent/frontend/src/MessageParser.js" startline="7" type="function"></mcsymbol> 方法处理：
- 用户认证状态检查
- 协议选择验证
- 消息类型路由

### 2. 动作提供者
**文件**: <mcfile name="ActionProvider.js" path="/Users/liuyanjun/therapy_agent/frontend/src/ActionProvider.js"></mcfile> (第 1-228 行)

主要方法：
- <mcsymbol name="askForPassword" filename="ActionProvider.js" path="/Users/liuyanjun/therapy_agent/frontend/src/ActionProvider.js" startline="12" type="function"></mcsymbol> - 请求密码输入
- <mcsymbol name="updateUserID" filename="ActionProvider.js" path="/Users/liuyanjun/therapy_agent/frontend/src/ActionProvider.js" startline="25" type="function"></mcsymbol> - 验证用户凭证
- <mcsymbol name="sendRequest" filename="ActionProvider.js" path="/Users/liuyanjun/therapy_agent/frontend/src/ActionProvider.js" startline="75" type="function"></mcsymbol> - 发送会话更新请求
- <mcsymbol name="handleReceivedData" filename="ActionProvider.js" path="/Users/liuyanjun/therapy_agent/frontend/src/ActionProvider.js" startline="85" type="function"></mcsymbol> - 处理后端响应

### 3. 主应用组件
**文件**: <mcfile name="App.js" path="/Users/liuyanjun/therapy_agent/frontend/src/App.js"></mcfile> (第 1-156 行)

<mcsymbol name="App" filename="App.js" path="/Users/liuyanjun/therapy_agent/frontend/src/App.js" startline="7" type="class"></mcsymbol> 组件：
- 管理用户登录状态
- 初始化聊天配置
- 处理登录/注册回调

## 认证中间件

### 1. Token 验证装饰器
**文件**: <mcfile name="__init__.py" path="/Users/liuyanjun/therapy_agent/backend/__init__.py"></mcfile> (第 413-434 行)

<mcsymbol name="token_required" filename="__init__.py" path="/Users/liuyanjun/therapy_agent/backend/__init__.py" startline="413" type="function"></mcsymbol> 装饰器：
- 检查 Authorization 头
- 验证 JWT token
- 注入用户对象到路由函数

### 2. Token 验证方法
**文件**: <mcfile name="models.py" path="/Users/liuyanjun/therapy_agent/backend/database/models.py"></mcfile> (第 65-75 行)

<mcsymbol name="verify_auth_token" filename="models.py" path="/Users/liuyanjun/therapy_agent/backend/database/models.py" startline="65" type="function"></mcsymbol> 静态方法：
- 使用 jwt.decode() 解析 token
- 查询并返回用户对象

## 数据库模型

### 1. 用户模型
**文件**: <mcfile name="models.py" path="/Users/liuyanjun/therapy_agent/backend/database/models.py"></mcfile> (第 18-75 行)

<mcsymbol name="User" filename="models.py" path="/Users/liuyanjun/therapy_agent/backend/database/models.py" startline="18" type="class"></mcsymbol> 类包含：
- 用户基本信息字段
- 密码哈希方法
- Token 生成和验证方法
- 关系映射到会话和选择

### 2. 会话模型
**文件**: <mcfile name="models.py" path="/Users/liuyanjun/therapy_agent/backend/database/models.py"></mcfile> (第 102-114 行)

<mcsymbol name="UserModelSession" filename="models.py" path="/Users/liuyanjun/therapy_agent/backend/database/models.py" startline="102" type="class"></mcsymbol> 类：
- 存储会话对话内容
- 关联用户和协议选择

## LLM 集成服务

### 1. 治疗服务主类
**文件**: <mcfile name="llm_therapy_service.py" path="/Users/liuyanjun/therapy_agent/backend/services/llm_therapy_service.py"></mcfile> (第 1-276 行)

<mcsymbol name="LLMTherapyService" filename="llm_therapy_service.py" path="/Users/liuyanjun/therapy_agent/backend/services/llm_therapy_service.py" startline="10" type="class"></mcsymbol> 提供：
- 会话初始化和管理
- 消息处理和回复生成
- 情绪分析和危机处理

### 2. API 集成
**文件**: <mcfile name="llm_integration.py" path="/Users/liuyanjun/therapy_agent/backend/models/llm_integration.py"></mcfile> (第 1-90 行)

<mcsymbol name="LLMIntegration" filename="llm_integration.py" path="/Users/liuyanjun/therapy_agent/backend/models/llm_integration.py" startline="10" type="class"></mcsymbol> 类：
- 支持多种 API 类型（OpenAI、Azure、Custom）
- 处理 API 调用和错误处理

## 移动端支持

### 1. 移动登录端点
**文件**: <mcfile name="__init__.py" path="/Users/liuyanjun/therapy_agent/backend/__init__.py"></mcfile> (第 436-479 行)

<mcsymbol name="mobile_login" filename="__init__.py" path="/Users/liuyanjun/therapy_agent/backend/__init__.py" startline="436" type="function"></mcsymbol> 函数：
- 简化移动端登录流程
- 自动创建用户和会话
- 返回初始对话数据

### 2. 聊天端点
**文件**: <mcfile name="__init__.py" path="/Users/liuyanjun/therapy_agent/backend/__init__.py"></mcfile> (第 359-391 行)

<mcsymbol name="chat_endpoint" filename="__init__.py" path="/Users/liuyanjun/therapy_agent/backend/__init__.py" startline="359" type="function"></mcsymbol> 函数：
- 使用 token 认证
- 直接处理聊天消息
- 返回格式化响应

## 测试和调试

### 1. API 测试脚本
**文件**: <mcfile name="test_api.py" path="/Users/liuyanjun/therapy_agent/backend/test_api.py"></mcfile> (第 1-70 行)

测试登录和会话更新功能，包含有效和无效凭证测试。

### 2. 密码重置工具
**文件**: <mcfile name="reset_user_password.py" path="/Users/liuyanjun/therapy_agent/reset_user_password.py"></mcfile>

用于调试用户密码问题，包含 bcrypt 版本检查和密码重置功能。

## 部署和配置

### 1. 依赖管理
**文件**: <mcfile name="requirements.txt" path="/Users/liuyanjun/therapy_agent/backend/requirements.txt"></mcfile> (第 1-36 行)

包含所有 Python 依赖包和版本信息。

### 2. 环境配置
**文件**: <mcfile name=".env" path="/Users/liuyanjun/therapy_agent/frontend/.env"></mcfile>
**文件**: <mcfile name=".env.example" path="/Users/liuyanjun/therapy_agent/frontend/.env.example"></mcfile>

配置 API 基础 URL 和其他环境变量。

## 故障排除指南

### 常见问题

1. **密码验证失败**：检查 bcrypt 版本和盐格式
2. **JWT token 无效**：验证 JWT_SECRET_KEY 环境变量
3. **数据库连接问题**：检查数据库配置和迁移状态
4. **LLM API 调用失败**：验证 API 密钥和端点配置

### 调试步骤

1. 启用后端调试日志（已在 login 函数中添加详细打印）
2. 使用 test_api.py 脚本测试认证流程
3. 检查数据库用户记录和密码哈希
4. 验证环境变量配置

---

*文档最后更新: 2024年*  
*维护团队: MindGuide 开发团队*