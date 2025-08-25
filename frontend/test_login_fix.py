#!/usr/bin/env python3
"""
测试登录页面功能的脚本
"""
import requests
import json
import time

def test_login_api():
    """测试登录API是否正常工作"""
    print("🧪 测试登录API...")
    
    try:
        # 测试登录
        login_data = {'user_info': {'username': 'user1', 'password': 'ph6n76gec9'}}
        response = requests.post('http://localhost:5000/api/login', json=login_data, timeout=10)
        
        print(f"📊 状态码: {response.status_code}")
        print(f"📄 响应内容: {response.text[:200]}...")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 登录API正常工作")
            print(f"🆔 用户ID: {data.get('userID')}")
            print(f"🔑 会话ID: {data.get('sessionID')}")
            print(f"💬 初始消息: {data.get('model_prompt', 'N/A')[:100]}...")
            return True
        else:
            print("❌ 登录API返回错误")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务器")
        print("💡 请确保后端服务正在运行在 http://localhost:5000")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_frontend_build():
    """测试前端是否可以正常构建"""
    print("\n🔨 测试前端构建...")
    
    import subprocess
    import os
    
    try:
        # 检查是否在正确的目录
        if not os.path.exists('package.json'):
            print("❌ 不在正确的目录中，请确保在frontend目录下运行")
            return False
        
        # 运行构建测试
        result = subprocess.run(['npm', 'run', 'build'], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ 前端构建成功")
            return True
        else:
            print("❌ 前端构建失败")
            print(f"错误: {result.stderr[:500]}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 前端构建超时")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def check_file_structure():
    """检查文件结构是否正确"""
    print("\n📁 检查文件结构...")
    
    required_files = [
        'src/LoginSimple.js',
        'src/LoginSimple.css',
        'src/App.js',
        'src/config.js',
        'src/ActionProvider.js',
        'src/MessageParser.js'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ 缺少以下文件:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    else:
        print("✅ 所有必需文件都存在")
        return True

def main():
    """主测试函数"""
    print("🚀 开始测试登录页面...")
    print("=" * 50)
    
    # 检查文件结构
    files_ok = check_file_structure()
    
    # 测试后端API
    api_ok = test_login_api()
    
    # 测试前端构建
    build_ok = test_frontend_build()
    
    print("\n" + "=" * 50)
    print("📋 测试结果总结:")
    print(f"📁 文件结构: {'✅ 通过' if files_ok else '❌ 失败'}")
    print(f"🔌 后端API: {'✅ 通过' if api_ok else '❌ 失败'}")
    print(f"🔨 前端构建: {'✅ 通过' if build_ok else '❌ 失败'}")
    
    if files_ok and api_ok and build_ok:
        print("\n🎉 所有测试通过！登录页面应该正常工作。")
        print("💡 运行 'npm start' 来启动前端应用")
    else:
        print("\n⚠️  存在一些问题，请根据上述信息进行修复。")

if __name__ == "__main__":
    main()