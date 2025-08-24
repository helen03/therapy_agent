#!/bin/bash

# 一键启动 Therapy Agent 应用

# 设置颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查是否在正确的目录
if [ ! -d "model" ] || [ ! -d "view" ]; then
  echo -e "${RED}错误: 请在项目根目录下运行此脚本${NC}"
  echo -e "请切换到包含 model 和 view 目录的目录，然后再次运行脚本"
  exit 1
fi

# 创建日志目录
mkdir -p logs

# 检查 Python 是否安装
echo -e "${BLUE}检查 Python 环境...${NC}"
if ! command -v python3 &> /dev/null; then
  echo -e "${RED}错误: 未找到 Python 3${NC}"
  echo -e "请先安装 Python 3.7 或更高版本"
  exit 1
fi

# 检查 pip 是否安装
if ! command -v pip3 &> /dev/null; then
  echo -e "${RED}错误: 未找到 pip3${NC}"
  echo -e "请先安装 pip3"
  exit 1
fi

# 检查 Node.js 是否安装
echo -e "${BLUE}检查 Node.js 环境...${NC}"
if ! command -v node &> /dev/null; then
  echo -e "${RED}错误: 未找到 Node.js${NC}"
  echo -e "请先安装 Node.js 14 或更高版本"
  exit 1
fi

# 检查 npm 是否安装
if ! command -v npm &> /dev/null; then
  echo -e "${RED}错误: 未找到 npm${NC}"
  echo -e "请先安装 npm"
  exit 1
fi

# 安装后端依赖
echo -e "${BLUE}安装后端依赖...${NC}"
cd model
pip3 install -r requirements.txt > ../logs/backend_install.log 2>&1
if [ $? -ne 0 ]; then
  echo -e "${RED}后端依赖安装失败，请查看 logs/backend_install.log${NC}"
  cd ..
  exit 1
fi
cd ..
echo -e "${GREEN}后端依赖安装成功${NC}"

# 安装前端依赖
echo -e "${BLUE}安装前端依赖...${NC}"
cd view
npm install --legacy-peer-deps > ../logs/frontend_install.log 2>&1
if [ $? -ne 0 ]; then
  echo -e "${RED}前端依赖安装失败，请查看 logs/frontend_install.log${NC}"
  cd ..
  exit 1
fi
cd ..
echo -e "${GREEN}前端依赖安装成功${NC}"

# 检查并创建 start_backend.py 脚本
if [ ! -f "start_backend.py" ]; then
  echo -e "${YELLOW}未找到 start_backend.py，正在创建...${NC}"
  cat > start_backend.py << 'EOF'
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入并启动 Flask 应用
from model import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
EOF
  echo -e "${GREEN}start_backend.py 创建成功${NC}"
fi

# 设置 Node.js 环境变量（解决 OpenSSL 问题）
export NODE_OPTIONS=--openssl-legacy-provider

# 启动后端服务
echo -e "${BLUE}启动后端服务...${NC}"
python3 start_backend.py > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}后端服务已启动（PID: $BACKEND_PID）${NC}"
echo -e "${YELLOW}日志文件: logs/backend.log${NC}"

# 等待后端启动
echo -e "${BLUE}等待后端服务初始化...${NC}"
sleep 5

# 启动前端服务
echo -e "${BLUE}启动前端服务...${NC}"
(cd view && npm run start > ../logs/frontend.log 2>&1) &
FRONTEND_PID=$!
echo -e "${GREEN}前端服务已启动（PID: $FRONTEND_PID）${NC}"
echo -e "${YELLOW}日志文件: logs/frontend.log${NC}"

# 显示启动完成信息
cat << EOF

${GREEN}🎉 Therapy Agent 应用已成功启动！${NC}

${BLUE}访问应用:${NC}
  - 本地访问: http://localhost:3000
  - 局域网访问: http://$(hostname -I | awk '{print $1}'):3000

${YELLOW}注意事项:${NC}
  - 查看后端日志: tail -f logs/backend.log
  - 查看前端日志: tail -f logs/frontend.log
  - 停止服务: 按 Ctrl+C 终止此脚本，或使用 kill $BACKEND_PID $FRONTEND_PID

EOF

# 等待用户中断
trap "echo '\n停止服务...'; kill $BACKEND_PID $FRONTEND_PID; echo '服务已停止'; exit 0" INT

# 保持脚本运行
while true; do
sleep 1
done