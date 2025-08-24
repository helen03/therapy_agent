import requests
import json

def test_api_endpoint():
    # 测试认证端点
    print("Testing authentication endpoint...")
    try:
        response = requests.post(
            "http://localhost:5000/api/login",
            json={
                "user_info": {
                    "username": "testuser",
                    "password": "testpass"
                }
            },
            timeout=5
        )
        print(f"Auth Status: {response.status_code}")
        print(f"Auth Response: {response.text}")
    except Exception as e:
        print(f"Auth Error: {e}")
    
    # 测试消息处理端点
    print("\nTesting message processing endpoint...")
    try:
        response = requests.post(
            "http://localhost:5000/api/update_session",
            json={
                "user_id": 1,
                "session_id": 1,
                "user_choice": "Hello",
                "input_type": "text"
            },
            timeout=10
        )
        print(f"Message Status: {response.status_code}")
        print(f"Message Response: {response.text}")
    except Exception as e:
        print(f"Message Error: {e}")

if __name__ == "__main__":
    test_api_endpoint()