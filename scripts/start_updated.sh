#!/bin/bash

# 更新版的一键启动 Therapy Agent 应用

# 设置颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查是否在正确的目录
if [ ! -d "model" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
  echo -e "${RED}错误: 请在项目根目录下运行此脚本${NC}"
  echo -e "请切换到包含 model, backend 和 frontend 目录的目录，然后再次运行脚本"
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

# 确保 frontend 目录下有 .env 文件
if [ ! -f "frontend/.env" ]; then
  echo -e "${YELLOW}未找到 frontend/.env，正在从 .env.example 创建...${NC}"
  cp frontend/.env.example frontend/.env
  echo -e "${GREEN}frontend/.env 创建成功${NC}"
fi

# 安装后端依赖
echo -e "${BLUE}安装后端依赖...${NC}"
cd backend
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
cd frontend
npm install --legacy-peer-deps > ../logs/frontend_install.log 2>&1
if [ $? -ne 0 ]; then
  echo -e "${RED}前端依赖安装失败，请查看 logs/frontend_install.log${NC}"
  cd ..
  exit 1
fi
cd ..
echo -e "${GREEN}前端依赖安装成功${NC}"

# 设置 Node.js 环境变量（解决 OpenSSL 问题）
export NODE_OPTIONS=--openssl-legacy-provider

# 启动后端服务
echo -e "${BLUE}启动后端服务...${NC}"
cd backend/api
python3 flask_backend_with_aws.py > ../../logs/backend.log 2>&1 &
BACEND_PID=$!
echo -e "${GREEN}后端服务已启动（PID: $BACEND_PID）${NC}"
echo -e "${YELLOW}日志文件: logs/backend.log${NC}"

# 等待后端启动
echo -e "${BLUE}等待后端服务初始化...${NC}"
sleep 5

# 启动前端服务
echo -e "${BLUE}启动前端服务...${NC}"
(cd "/Users/liuyanjun/therapy_agent/frontend" && npm run start > "/Users/liuyanjun/therapy_agent/logs/frontend.log" 2>&1) &
FRONTEND_PID=$!
echo -e "${GREEN}前端服务已启动（PID: $FRONTEND_PID）${NC}"
echo -e "${YELLOW}日志文件: logs/frontend.log${NC}"

# 显示启动完成信息
cat << EOF

${GREEN}🎉 Therapy Agent 应用已成功启动！${NC}

${BLUE}访问应用:${NC}
  - 本地访问: http://localhost:3000
  - 局域网访问: http://$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1):3000

${YELLOW}注意事项:${NC}
  - 查看后端日志: tail -f logs/backend.log
  - 查看前端日志: tail -f logs/frontend.log
  - 停止服务: 按 Ctrl+C 终止此脚本，或使用 kill $BACEND_PID $FRONTEND_PID

EOF

# 等待用户中断
trap "echo '\n停止服务...'; kill $BACEND_PID $FRONTEND_PID; echo '服务已停止'; exit 0" INT

# 保持脚本运行
while true;
do
sleep 1
done