# Therapy Agent 启动注意事项

## 环境要求

### 后端环境
- Python 3.7+（推荐3.9）
- pip 工具
- 必要的Python库（见 `model/requirements.txt`）

### 前端环境
- Node.js 14+（项目在v18上测试通过，但需要特殊配置）
- npm 6+ 或 yarn

## 启动前准备

### 1. 安装后端依赖

```bash
cd model
pip install -r requirements.txt
```

### 2. 安装前端依赖

```bash
cd view
npm install --legacy-peer-deps
```

**注意：** 必须使用 `--legacy-peer-deps` 标志，否则会出现 react-chatbot-kit 与 react 版本不兼容的依赖冲突。

### 3. Node.js 版本问题

如果使用 Node.js v17+（包括v18），需要设置环境变量以解决OpenSSL错误：

```bash
export NODE_OPTIONS=--openssl-legacy-provider
```

### 4. 模型文件说明

项目运行时会显示 `Warning: Model files not found. Using fallback models.` 警告，这是因为缺少预训练模型文件，但不影响基本功能的使用。

### 5. Numpy 版本警告

如果看到 `A NumPy version >=1.19.5 and <1.27.0 is required` 警告，这是因为当前安装的NumPy版本略低于要求，但通常不会影响功能使用。如要解决，可升级NumPy：

```bash
pip install --upgrade numpy
```

## 启动顺序

1. 首先启动后端服务
2. 然后启动前端服务

## 访问应用

前端启动成功后，可通过以下URL访问应用：
- 本地访问：http://localhost:3000
- 局域网访问：http://[你的IP地址]:3000

## 停止服务

- 按 `Ctrl+C` 可以停止运行中的服务
- 先停止前端服务，再停止后端服务

## 常见问题解决

1. **CSV文件找不到错误**
   - 确保 `EmpatheticPersonas.csv` 文件存在于 `model` 目录下

2. **模块导入错误**
   - 使用 `start_backend.py` 脚本启动后端，该脚本已包含路径设置

3. **跨域问题**
   - 后端已配置CORS，通常无需额外设置

4. **浏览器白屏**
   - 检查前端控制台是否有错误信息
   - 确认后端服务是否正常运行

## 开发模式说明

- 后端运行在调试模式下，代码修改后会自动重启
- 前端支持热重载，修改代码后浏览器会自动刷新

## 生产环境建议

- 使用Gunicorn或uWSGI等WSGI服务器运行后端
- 构建前端生产版本：`npm run build`，然后使用Nginx等静态文件服务器部署
- 关闭调试模式
- 考虑使用Docker容器化部署