import requests
import json

# 设置API基础URL
base_url = 'http://localhost:5002/api'

# 测试登录功能
def test_login():
    login_endpoint = f'{base_url}/login'
    
    # 测试用的用户名和密码
    # API期望数据格式为 {"user_info": {"username": "...", "password": "..."}}
    credentials = {
        'user_info': {
            'username': 'user00',
            'password': 'password'
        }
    }
    
    print(f'测试登录API: {login_endpoint}')
    print(f'使用凭证: {credentials}')
    
    try:
        # 发送POST请求
        response = requests.post(
            login_endpoint,
            data=json.dumps(credentials),
            headers={'Content-Type': 'application/json'}
        )
        
        # 打印响应状态码
        print(f'响应状态码: {response.status_code}')
        
        # 尝试解析JSON响应
        try:
            response_data = response.json()
            print(f'响应内容: {json.dumps(response_data, indent=2)}')
            
            # 检查登录是否成功
            if response.status_code == 200 and response_data.get('success'):
                print('✅ 登录成功!')
                return True
            else:
                print('❌ 登录失败!')
                return False
        except json.JSONDecodeError:
            print(f'❌ 无法解析响应为JSON: {response.text}')
            return False
    except requests.exceptions.RequestException as e:
        print(f'❌ 请求异常: {e}')
        return False

if __name__ == '__main__':
    print('===== 开始测试登录API =====')
    success = test_login()
    print('===== 测试结束 =====')
    
    if success:
        print('\n🎉 测试成功! 您可以尝试在浏览器中访问 http://localhost:3000 进行登录。')
    else:
        print('\n❌ 测试失败! 请检查后端服务器是否运行，以及用户名和密码是否正确。')