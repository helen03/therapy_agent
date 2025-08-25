#!/usr/bin/env python3
"""
测试脚本，用于验证后端API是否能正确响应用户输入
"""

import requests
import json

def test_session_update():
    """测试会话更新API端点"""
    print("测试会话更新API...")
    
    # API端点
    url = "http://localhost:5000/api/update_session"
    
    # 测试数据
    test_data = {
        "choice_info": {
            "user_id": 1,
            "session_id": 1,
            "input_type": "text",
            "user_choice": "你好，我今天感觉有点焦虑"
        }
    }
    
    try:
        # 发送POST请求
        response = requests.post(
            url,
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应头: {response.headers}")
        
        # 尝试解析JSON响应
        try:
            response_data = response.json()
            print(f"响应数据: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
            
            # 检查响应格式
            required_fields = ["chatbot_response", "user_options", "emotion"]
            missing_fields = [field for field in required_fields if field not in response_data]
            
            if missing_fields:
                print(f"❌ 缺少必要字段: {missing_fields}")
                return False
            else:
                print("✅ 响应格式正确")
                return True
                
        except json.JSONDecodeError:
            print(f"❌ 无法解析JSON响应: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")
        return False

def test_llm_service():
    """测试LLM服务"""
    print("\n测试LLM服务...")
    
    try:
        # 导入LLM服务
        from backend.services.llm_therapy_service import therapy_service
        
        # 测试消息处理
        result = therapy_service.process_message(
            user_id=1,
            session_id=1,
            message="你好，我今天感觉有点焦虑",
            input_type="text"
        )
        
        print(f"LLM服务响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        # 检查必要字段
        required_fields = ["response", "options", "emotion"]
        missing_fields = [field for field in required_fields if field not in result]
        
        if missing_fields:
            print(f"❌ LLM服务缺少必要字段: {missing_fields}")
            return False
        else:
            print("✅ LLM服务响应格式正确")
            return True
            
    except Exception as e:
        print(f"❌ LLM服务测试失败: {e}")
        return False

if __name__ == "__main__":
    print("开始测试MindGuide后端服务...")
    print("=" * 50)
    
    # 测试LLM服务
    llm_success = test_llm_service()
    
    # 测试API端点
    api_success = test_session_update()
    
    print("\n" + "=" * 50)
    if llm_success and api_success:
        print("🎉 所有测试通过！系统应该能正确响应用户输入。")
    else:
        print("❌ 部分测试失败。请检查上述错误信息。")