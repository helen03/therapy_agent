#!/usr/bin/env python3
"""
统一测试脚本，用于测试MindGuide系统的各个组件
"""

import requests
import json
import os
import sys

# 添加项目路径到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_backend_api():
    """测试后端API"""
    print("🧪 测试后端API...")
    
    base_url = 'http://localhost:5000/api'
    
    # 测试1: 健康检查端点
    try:
        response = requests.get(f'{base_url}/health', timeout=5)
        print(f"  健康检查: {'✅ 通过' if response.status_code == 200 else '❌ 失败'}")
    except:
        print("  健康检查: ⚠️  无法连接")
    
    # 测试2: 登录端点
    try:
        response = requests.post(
            f'{base_url}/login',
            json={"user_info": {"username": "test", "password": "test"}},
            timeout=5
        )
        # 401表示端点存在但认证失败，这是正常的
        print(f"  登录端点: {'✅ 可访问' if response.status_code in [200, 401] else '❌ 失败'}")
    except:
        print("  登录端点: ⚠️  无法连接")
        
    # 测试3: 注册端点
    try:
        response = requests.post(
            f'{base_url}/register',
            json={"user_info": {"username": "test", "password": "test"}},
            timeout=5
        )
        # 400表示端点存在但参数验证失败，这是正常的
        print(f"  注册端点: {'✅ 可访问' if response.status_code in [200, 400] else '❌ 失败'}")
    except:
        print("  注册端点: ⚠️  无法连接")

def test_frontend():
    """测试前端配置"""
    print("\n🎨 测试前端配置...")
    
    # 检查.env文件
    env_path = os.path.join(os.path.dirname(__file__), 'frontend', '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            content = f.read()
            if 'REACT_APP_API_BASE_URL' in content:
                print("  环境配置: ✅ 存在")
            else:
                print("  环境配置: ❌ 缺少API基础URL")
    else:
        print("  环境配置: ⚠️  .env文件不存在")

def test_database():
    """测试数据库连接"""
    print("\n💾 测试数据库...")
    
    try:
        from backend.database.models import db, User
        from backend import create_app
        
        app = create_app()
        with app.app_context():
            # 尝试查询用户表
            user_count = User.query.count()
            print(f"  数据库连接: ✅ 正常 (用户数: {user_count})")
    except Exception as e:
        print(f"  数据库连接: ❌ 失败 ({e})")

def test_llm_integration():
    """测试LLM集成"""
    print("\n🤖 测试LLM集成...")
    
    try:
        from backend.models.llm_integration import get_llm
        llm = get_llm()
        
        if hasattr(llm, 'api_type'):
            print(f"  LLM实例: ✅ 创建成功 (类型: {llm.api_type})")
            
            # 测试情感分析
            try:
                emotion = llm.analyze_emotion("我今天感觉很好")
                print(f"  情感分析: ✅ 正常 (结果: {emotion})")
            except Exception as e:
                print(f"  情感分析: ⚠️  错误 ({e})")
        else:
            print("  LLM实例: ❌ 创建失败")
    except Exception as e:
        print(f"  LLM集成: ❌ 失败 ({e})")

def main():
    print("🚀 MindGuide 系统测试")
    print("=" * 50)
    
    test_backend_api()
    test_frontend()
    test_database()
    test_llm_integration()
    
    print("\n" + "=" * 50)
    print("测试完成!")

if __name__ == '__main__':
    main()