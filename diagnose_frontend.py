#!/usr/bin/env python3
"""
前端问题诊断脚本
通过模拟浏览器行为来诊断前端问题
"""

import requests
import json
import time

def test_frontend_issues():
    """诊断前端问题"""
    base_url = "http://localhost:5001"
    
    print("🔍 开始前端问题诊断...")
    
    # 1. 测试登录API
    print("\n1. 测试登录API...")
    try:
        login_response = requests.post(f"{base_url}/api/login", json={
            "user_info": {"username": "user1", "password": "ph6n76gec9"}
        })
        login_data = login_response.json()
        
        if login_data.get("success"):
            print("✅ 登录API正常")
            user_id = login_data["userID"]
            session_id = login_data["sessionID"]
            print(f"   用户ID: {user_id}")
            print(f"   会话ID: {session_id}")
            print(f"   初始选择: {login_data.get('choices', [])}")
        else:
            print("❌ 登录API失败")
            return
    except Exception as e:
        print(f"❌ 登录API异常: {e}")
        return
    
    # 2. 测试聊天API
    print("\n2. 测试聊天API...")
    test_messages = [
        "我感觉很好",
        "Continue",
        "Happy",
        "我想聊聊工作压力"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n   测试消息 {i}: '{message}'")
        
        try:
            chat_response = requests.post(f"{base_url}/api/update_session", json={
                "choice_info": {
                    "user_id": user_id,
                    "session_id": session_id,
                    "user_choice": message
                }
            })
            
            if chat_response.status_code == 200:
                chat_data = chat_response.json()
                if "chatbot_response" in chat_data:
                    print(f"   ✅ 回复: {chat_data['chatbot_response']}")
                    if "user_options" in chat_data:
                        print(f"   选项: {chat_data['user_options']}")
                else:
                    print(f"   ❌ 无回复: {chat_data.get('error', '未知错误')}")
            else:
                print(f"   ❌ HTTP错误: {chat_response.status_code}")
                
        except Exception as e:
            print(f"   ❌ 聊天异常: {e}")
    
    # 3. 分析可能的问题
    print("\n3. 问题分析...")
    print("如果后端API完全正常，但前端仍有问题，可能的原因：")
    print("   • React状态管理问题")
    print("   • react-chatbot-kit配置问题")
    print("   • 组件props传递问题")
    print("   • JavaScript执行错误")
    print("   • 浏览器缓存问题")
    
    # 4. 提供解决方案
    print("\n4. 建议的解决方案:")
    print("   1. 清除浏览器缓存 (Ctrl+F5)")
    print("   2. 打开浏览器开发者工具 (F12)")
    print("   3. 查看Console标签的JavaScript错误")
    print("   4. 查看Network标签的网络请求")
    print("   5. 尝试无痕模式")
    
    print("\n✅ 诊断完成")

if __name__ == "__main__":
    test_frontend_issues()