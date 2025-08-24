# 移动端部署指南

本文档提供了 Therapy Agent 项目的 Android 应用和微信小程序的部署指南。

## Android 应用部署

### 开发环境要求

- Android Studio 2022.3.1 或更高版本
- JDK 17
- Android SDK 34
- Gradle 8.0

### 构建 Android 应用

1. **使用构建脚本**
   ```bash
   cd deploy
   bash android-build.sh
   ```

2. **手动构建**
   ```bash
   cd android
   ./gradlew clean
   ./gradlew assembleRelease
   ```

3. **生成的 APK 文件位置**
   - `android/app/build/outputs/apk/release/app-release.apk`
   - 构建脚本会自动复制到 `deploy/android/therapy-agent-release.apk`

### 安装和测试

1. **连接 Android 设备**
   ```bash
   adb devices  # 确认设备连接
   ```

2. **安装 APK**
   ```bash
   adb install deploy/android/therapy-agent-release.apk
   ```

3. **运行应用**
   ```bash
   adb shell am start -n com.therapyagent/.MainActivity
   ```

### 发布到应用商店

1. **生成签名密钥**
   ```bash
   keytool -genkey -v -keystore therapy-agent.keystore -alias therapyagent -keyalg RSA -keysize 2048 -validity 10000
   ```

2. **配置签名**
   在 `android/app/build.gradle` 中添加签名配置：
   ```gradle
   android {
       signingConfigs {
           release {
               storeFile file("therapy-agent.keystore")
               storePassword "your_password"
               keyAlias "therapyagent"
               keyPassword "your_password"
           }
       }
       buildTypes {
           release {
               signingConfig signingConfigs.release
           }
       }
   }
   ```

3. **构建发布版本**
   ```bash
   ./gradlew assembleRelease
   ```

## 微信小程序部署

### 开发环境要求

- 微信开发者工具最新版本
- 小程序 AppID（需要注册微信小程序账号）

### 配置小程序

1. **修改项目配置**
   - 在 `miniprogram/project.config.json` 中替换 `your-miniprogram-appid` 为实际 AppID
   - 配置服务器域名（需要在微信小程序后台配置）

2. **服务器域名配置**
   - request 合法域名：`https://your-backend-domain.com`
   - uploadFile 合法域名：`https://your-backend-domain.com`
   - downloadFile 合法域名：`https://your-backend-domain.com`

### 上传和发布

1. **使用上传脚本**
   ```bash
   cd deploy
   bash miniprogram-upload.sh
   ```

2. **手动上传**
   - 打开微信开发者工具
   - 导入 `miniprogram` 目录
   - 点击"上传"按钮
   - 填写版本号和项目备注

3. **提交审核**
   - 登录[微信小程序后台](https://mp.weixin.qq.com/)
   - 在"开发管理"中提交审核
   - 审核通过后发布

### 测试小程序

1. **开发版测试**
   - 在微信开发者工具中预览
   - 扫描二维码在微信中测试

2. **体验版测试**
   - 上传后设置为体验版
   - 邀请测试人员体验

## 后端 API 部署

### Docker 部署

1. **构建后端镜像**
   ```bash
   docker build -f deploy/Dockerfile.backend -t therapy-agent-backend .
   ```

2. **启动服务**
   ```bash
   cd deploy
   docker-compose up -d
   ```

3. **查看日志**
   ```bash
   docker-compose logs -f backend
   ```

### 环境变量配置

创建 `.env` 文件：
```bash
DATABASE_URL=sqlite:////app/app.db
FLASK_ENV=production
CORS_ORIGINS=https://your-domain.com,https://mini-program.com
```

## 生产环境配置

### Nginx 配置

1. **SSL 证书**
   - 申请 SSL 证书（Let's Encrypt 或商业证书）
   - 配置证书路径在 `deploy/nginx.conf`

2. **域名解析**
   - 将域名解析到服务器 IP
   - 配置 HTTPS 重定向

### 数据库配置

1. **生产数据库**
   ```bash
   # 使用 PostgreSQL 或 MySQL
   DATABASE_URL=postgresql://user:password@host:port/database
   ```

2. **数据库迁移**
   ```bash
   flask db upgrade
   ```

## 监控和维护

### 健康检查

```bash
# 检查服务状态
curl http://localhost:5000/health

# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 备份策略

1. **数据库备份**
   ```bash
   # SQLite 备份
   sqlite3 app.db ".backup backup.db"
   
   # 定期备份脚本
   */30 * * * * /path/to/backup-script.sh
   ```

2. **日志轮转**
   ```bash
   # 配置 logrotate
   /var/log/therapy-agent/*.log {
       daily
       rotate 7
       compress
       missingok
       notifempty
   }
   ```

## 故障排除

### 常见问题

1. **Android 构建失败**
   - 检查 JDK 版本
   - 清理 Gradle 缓存：`./gradlew clean`

2. **小程序网络请求失败**
   - 检查服务器域名配置
   - 验证 SSL 证书有效性

3. **CORS 错误**
   - 检查 Nginx CORS 配置
   - 验证域名白名单

### 技术支持

- Android 问题：查看 Android Studio 日志
- 小程序问题：微信开发者工具调试
- 后端问题：查看 Docker 容器日志

## 版本更新

### Android 更新

1. 更新 `android/app/build.gradle` 中的版本号
2. 重新构建和签名 APK
3. 提交到应用商店

### 小程序更新

1. 更新版本号并上传
2. 提交微信审核
3. 发布新版本

### 后端更新

1. 构建新的 Docker 镜像
2. 滚动更新服务：`docker-compose up -d --build`

---

**注意**：生产环境部署前请进行充分测试，确保所有功能正常工作。