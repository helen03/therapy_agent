# 部署指南

## 环境配置

### 开发环境
默认使用 `http://localhost:5001` 作为API服务器地址。

### 生产环境
生产环境会自动检测当前域名并配置API地址：
- 如果访问 `http://yourdomain.com`，API会自动指向 `http://yourdomain.com:5001`
- 如果使用HTTPS，API会自动使用 `https://yourdomain.com:5001`

## 环境变量配置

### 开发环境 (.env.development)
```
REACT_APP_API_BASE_URL=http://localhost:5001
REACT_APP_ENV=development
```

### 生产环境 (.env.production)
```
REACT_APP_API_BASE_URL=
REACT_APP_ENV=production
```

### 自定义环境变量
你可以通过以下方式设置自定义API地址：

#### Linux/Mac:
```bash
export REACT_APP_API_BASE_URL=https://your-api-server.com
npm start
```

#### Windows:
```cmd
set REACT_APP_API_BASE_URL=https://your-api-server.com
npm start
```

## 构建生产版本

```bash
# 构建生产版本
npm run build

# 构建后的文件将位于 build/ 目录
# 可以将这些文件部署到任何静态文件服务器
```

## 部署到生产服务器

### 1. 构建应用
```bash
npm run build
```

### 2. 部署到服务器
将 `build/` 目录下的所有文件复制到服务器的web根目录。

### 3. 配置反向代理（推荐）
使用Nginx或其他反向代理将API请求转发到后端服务：

#### Nginx配置示例
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        root /path/to/your/build;
        try_files $uri /index.html;
    }
    
    location /api/ {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 故障排除

### 检查环境
打开浏览器控制台，查看环境信息输出。

### API连接问题
确保：
1. 后端服务正在运行
2. 防火墙允许相应端口
3. 环境变量配置正确
4. CORS配置正确

### 调试信息
在浏览器控制台中查看以下信息：
- 当前域名和端口
- API基础URL
- 环境类型（开发/生产）

## 支持的环境变量

| 变量名 | 描述 | 示例 |
|--------|------|------|
| REACT_APP_API_BASE_URL | API服务器地址 | https://api.example.com |
| REACT_APP_ENV | 环境标识 | development/production |

## 注意事项

1. 所有环境变量必须以 `REACT_APP_` 开头
2. 修改环境变量后需要重启开发服务器
3. 生产环境建议配置HTTPS
4. 确保后端API允许跨域请求