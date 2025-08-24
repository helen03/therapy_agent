#!/bin/bash

# Android 应用构建和部署脚本

echo "🚀 开始构建 Android 应用..."

# 检查是否在项目根目录
if [ ! -d "android" ]; then
    echo "❌ 错误：请在项目根目录运行此脚本"
    exit 1
fi

cd android

# 清理构建缓存
echo "🧹 清理构建缓存..."
./gradlew clean

# 构建发布版本
echo "🔨 构建发布版本..."
./gradlew assembleRelease

# 检查构建是否成功
if [ $? -eq 0 ]; then
    echo "✅ Android 应用构建成功！"
    
    # 复制 APK 到部署目录
    APK_PATH="app/build/outputs/apk/release/app-release.apk"
    if [ -f "$APK_PATH" ]; then
        mkdir -p ../deploy/android
        cp "$APK_PATH" "../deploy/android/therapy-agent-release.apk"
        echo "📦 APK 文件已复制到: deploy/android/therapy-agent-release.apk"
        echo "📱 文件大小: $(du -h ../deploy/android/therapy-agent-release.apk | cut -f1)"
    else
        echo "⚠️  警告：未找到 APK 文件"
    fi
else
    echo "❌ Android 应用构建失败"
    exit 1
fi

echo "🎉 Android 部署完成！"