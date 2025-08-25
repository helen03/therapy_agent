#!/usr/bin/env python3
"""
聊天功能测试脚本
测试后端API的聊天功能
"""

import requests
import json
import time

def test_chat_functionality():
    """测试聊天功能"""
    base_url = "http://localhost:5001"
    
    print("🧪 开始测试聊天功能...")
    
    # 1. 测试登录
    print("\n1. 测试登录...")
    login_data = {
        "user_info": {
            "username": "user1",
            "password": "ph6n76gec9"
        }
    }
    
    try:
        response = requests.post(f"{base_url}/api/login", json=login_data)
        response.raise_for_status()
        login_result = response.json()
        
        if login_result.get("success"):
            print("✅ 登录成功")
            user_id = login_result["userID"]
            session_id = login_result["sessionID"]
            print(f"   用户ID: {user_id}")
            print(f"   会话ID: {session_id}")
            print(f"   初始提示: {login_result.get('model_prompt', 'N/A')}")
        else:
            print("❌ 登录失败")
            return False
    except Exception as e:
        print(f"❌ 登录异常: {e}")
        return False
    
    # 2. 测试聊天消息
    print("\n2. 测试聊天消息...")
    
    test_messages = [
        "我感觉很好",
        "Continue",
        "Happy",
        "我想聊聊我的工作压力",
        "我感到有些焦虑"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n   测试消息 {i}: '{message}'")
        
        chat_data = {
            "choice_info": {
                "user_id": user_id,
                "session_id": session_id,
                "user_choice": message
            }
        }
        
        try:
            response = requests.post(f"{base_url}/api/update_session", json=chat_data)
            response.raise_for_status()
            chat_result = response.json()
            
            if "chatbot_response" in chat_result:
                print(f"   ✅ 回复: {chat_result['chatbot_response']}")
                if "user_options" in chat_result:
                    print(f"   选项: {chat_result['user_options']}")
            else:
                print(f"   ❌ 无回复: {chat_result.get('error', '未知错误')}")
                
        except Exception as e:
            print(f"   ❌ 消息发送异常: {e}")
    
    print("\n✅ 聊天功能测试完成")
    return True

if __name__ == "__main__":
    test_chat_functionality()