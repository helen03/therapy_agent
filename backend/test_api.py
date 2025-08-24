import requests
import json

def test_api_endpoint():
    # 设置正确的后端URL和端口
    base_url = "http://localhost:5002"
    
    # 测试有效的登录凭证（user1/ph6n76gec9）
    print("Testing valid login credentials (user1/ph6n76gec9)...")
    try:
        response = requests.post(
            f"{base_url}/api/login",
            json={
                "user_info": {
                    "username": "user1",
                    "password": "ph6n76gec9"
                }
            },
            timeout=10
        )
        print(f"Auth Status: {response.status_code}")
        print(f"Auth Response: {response.text}")
        
        # 如果登录成功，尝试更新会话
        if response.status_code == 200:
            data = response.json()
            if data.get("success") or data.get("validID"):
                user_id = data.get("userID")
                session_id = data.get("sessionID")
                print(f"\nTesting session update for user {user_id}...")
                try:
                    response = requests.post(
                        f"{base_url}/api/update_session",
                        json={
                            "choice_info": {
                                "user_id": user_id,
                                "session_id": session_id,
                                "user_choice": "Hello",
                                "input_type": "text"
                            }
                        },
                        timeout=15
                    )
                    print(f"Session Update Status: {response.status_code}")
                    print(f"Session Update Response: {response.text}")
                except Exception as e:
                    print(f"Session Update Error: {e}")
    except Exception as e:
        print(f"Auth Error: {e}")
    
    # 测试无效的登录凭证
    print("\nTesting invalid login credentials...")
    try:
        response = requests.post(
            f"{base_url}/api/login",
            json={
                "user_info": {
                    "username": "invalid_user",
                    "password": "invalid_pass"
                }
            },
            timeout=5
        )
        print(f"Invalid Auth Status: {response.status_code}")
        print(f"Invalid Auth Response: {response.text}")
    except Exception as e:
        print(f"Invalid Auth Error: {e}")

if __name__ == "__main__":
    test_api_endpoint()