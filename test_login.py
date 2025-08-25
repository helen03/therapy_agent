#!/usr/bin/env python3
import os
import requests
import json

# 后端API地址
BACKEND_URL = 'http://127.0.0.1:5000/api/login'

# 测试登录函数
def test_login(username, password):
    headers = {'Content-Type': 'application/json'}
    data = {
        'user_info': {
            'username': username,
            'password': password
        }
    }
    
    print(f"发送的请求数据: {data}")
    
    try:
        response = requests.post(BACKEND_URL, headers=headers, data=json.dumps(data))
        print(f"响应状态码: {response.status_code}")
        print(f"响应头: {response.headers}")
        
        try:
            result = response.json()
            print(f"响应内容: {result}")
            print(f"登录测试结果: {'成功' if result.get('success') else '失败'}")
            return result.get('success', False)
        except json.JSONDecodeError:
            print(f"无法解析响应为JSON: {response.text}")
            return False
    except Exception as e:
        print(f"登录测试出错: {e}")
        return False

if __name__ == '__main__':
    # 测试用户'user11'的登录
    print("测试用户'user11'的登录...")
    test_login('user11', 'password123')  # 使用我们刚刚设置的密码