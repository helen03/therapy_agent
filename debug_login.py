#!/usr/bin/env python3
import os
import bcrypt
from backend import create_app
from backend.database.models import User
from backend import db
import json
import requests

# 创建应用
def debug_user_and_password(username, password):
    app = create_app()
    with app.app_context():
        # 1. 直接在数据库中检查用户
        print(f"\n===== 直接数据库检查 ====")
        user = User.query.filter_by(username=username).first()
        
        if user:
            print(f"找到用户 '{username}' (ID: {user.id})")
            print(f"邮箱: {user.email}")
            print(f"密码哈希: {user.password_hash}")
            print(f"密码哈希长度: {len(user.password_hash)}")
            
            # 2. 直接测试密码验证逻辑
            print("\n===== 密码验证测试 ====")
            print(f"输入密码: '{password}'")
            print(f"密码编码后: '{password.encode('utf-8')}'")
            print(f"哈希编码后: '{user.password_hash.encode('utf-8')}'")
            
            # 使用bcrypt直接验证
            is_valid = bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8'))
            print(f"bcrypt直接验证结果: {is_valid}")
            
            # 使用User模型的check_password方法
            is_valid_model = user.check_password(password)
            print(f"User模型check_password方法验证结果: {is_valid_model}")
            
            return user
        else:
            print(f"未找到用户 '{username}'")
            return None

# 3. 测试API调用
def test_api_login(username, password):
    print("\n===== API登录测试 ====")
    login_url = 'http://localhost:5002/api/login'
    credentials = {
        'user_info': {
            'username': username,
            'password': password
        }
    }
    
    print(f"API URL: {login_url}")
    print(f"请求数据: {json.dumps(credentials, indent=2)}")
    
    try:
        response = requests.post(
            login_url,
            data=json.dumps(credentials),
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        try:
            response_json = response.json()
            print(f"响应JSON: {json.dumps(response_json, indent=2)}")
        except json.JSONDecodeError:
            print("无法解析响应为JSON")
            
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")

if __name__ == '__main__':
    # 调试用户 'user00'
    username = 'user00'
    password = 'password'
    
    print(f"开始调试用户 '{username}'")
    user = debug_user_and_password(username, password)
    
    if user:
        # 如果用户存在，测试API登录
        test_api_login(username, password)
    else:
        print("用户不存在，无法测试API登录")