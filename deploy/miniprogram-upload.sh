#!/bin/bash

# 微信小程序上传脚本

echo "🚀 开始上传微信小程序..."

# 检查是否在项目根目录
if [ ! -d "miniprogram" ]; then
    echo "❌ 错误：请在项目根目录运行此脚本"
    exit 1
fi

# 检查是否安装了微信开发者工具
if ! command -v cli &> /dev/null; then
    echo "❌ 错误：未找到微信开发者工具 CLI"
    echo "请先安装微信开发者工具：https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html"
    exit 1
fi

# 进入小程序目录
cd miniprogram

# 获取版本号（从 project.config.json 或使用日期）
VERSION=$(date +%Y%m%d.%H%M)
DESC="自动部署：$(date '+%Y-%m-%d %H:%M:%S')"

echo "📦 版本号: $VERSION"
echo "📝 描述: $DESC"

# 上传小程序
echo "⬆️  上传小程序代码..."
cli upload \
    --project ./ \
    --version $VERSION \
    --desc "$DESC" \
    --verbose

if [ $? -eq 0 ]; then
    echo "✅ 小程序上传成功！"
    echo "🌐 版本: $VERSION"
    echo "📋 描述: $DESC"
    echo "💡 请登录微信小程序后台提交审核"
else
    echo "❌ 小程序上传失败"
    exit 1
fi

echo "🎉 小程序部署完成！"