#!/usr/bin/env python3
"""
简单的登录API测试服务器
"""
import sys
import os
sys.path.append('/Users/liuyanjun/therapy_agent/backend')

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 模拟用户数据库
users = {
    'user1': {'password': 'ph6n76gec9', 'user_id': 1},
    'user2': {'password': 'ph6n76gec9', 'user_id': 2},
    'user3': {'password': 'ph6n76gec9', 'user_id': 3},
}

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print(f"收到登录请求: {data}")
        
        if not data or 'user_info' not in data:
            return jsonify({
                'success': False,
                'error': '请求数据格式错误'
            }), 400
        
        user_info = data['user_info']
        username = user_info.get('username')
        password = user_info.get('password')
        
        print(f"用户名: {username}, 密码: {password}")
        
        if not username or not password:
            return jsonify({
                'success': False,
                'error': '用户名和密码不能为空'
            }), 400
        
        # 验证用户
        if username in users and users[username]['password'] == password:
            user_id = users[username]['user_id']
            session_id = f"session_{user_id}_{hash(username) % 10000}"
            
            response_data = {
                'success': True,
                'validID': True,
                'userID': user_id,
                'sessionID': session_id,
                'token': f"token_{session_id}",
                'username': username,
                'model_prompt': f'欢迎 {username}！今天感觉怎么样？我想了解更多关于你的情绪状态。',
                'choices': ['我感觉很好', '我感觉不太好', '我感觉一般']
            }
            
            print(f"登录成功: {response_data}")
            return jsonify(response_data)
        else:
            print(f"登录失败: 用户名或密码错误")
            return jsonify({
                'success': False,
                'error': '用户名或密码错误'
            }), 401
    
    except Exception as e:
        print(f"登录异常: {e}")
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'message': '服务器正常运行'
    })

@app.route('/api/update_session', methods=['POST'])
def update_session():
    try:
        data = request.get_json()
        print(f"收到更新会话请求: {data}")
        
        if not data or 'choice_info' not in data:
            return jsonify({
                'error': '请求数据格式错误'
            }), 400
        
        choice_info = data['choice_info']
        user_id = choice_info.get('user_id')
        session_id = choice_info.get('session_id')
        user_choice = choice_info.get('user_choice')
        
        print(f"用户ID: {user_id}, 会话ID: {session_id}, 选择: {user_choice}")
        
        if not user_id or not session_id:
            return jsonify({
                'error': '用户ID和会话ID不能为空'
            }), 400
        
        # 根据用户选择生成回复
        response_map = {
            '我感觉很好': '很高兴听到你感觉很好！能告诉我更多关于你现在的心情吗？',
            '我感觉不太好': '听起来你心情不太好。我想了解更多关于你的感受。',
            '我感觉一般': '谢谢你分享。能详细说说你现在的状态吗？',
            'Happy': '很高兴你感到快乐！有什么特别的事情让你开心吗？',
            'Sad': '我理解你感到悲伤。这种情绪是正常的，我们可以一起面对。',
            'Angry': '愤怒是一种自然的情绪。能告诉我是什么让你感到愤怒吗？',
            'Neutral': '我明白了。让我们探索一下你现在的感受。',
            'Yes': '好的，让我们继续下一步。',
            'No': '没问题，我们可以尝试其他方法。',
            'Continue': '好的，让我们继续治疗过程。',
            'Recent': '让我们谈谈最近发生的事情。',
            'Distant': '我们可以回顾一下过去的经历。',
            'Better': '很高兴听到你感觉好多了。',
            'Worse': '我理解你可能感觉更糟了。让我们一起面对这个挑战。',
            'No change': '有时候保持稳定也是好事。让我们继续努力。'
        }
        
        # 生成回复
        if user_choice in response_map:
            chatbot_response = response_map[user_choice]
        else:
            chatbot_response = f'我理解你选择了"{user_choice}"。能告诉我更多关于这个选择的细节吗？'
        
        # 根据选择提供选项
        if user_choice in ['我感觉很好', '我感觉不太好', '我感觉一般']:
            user_options = ['continue']
        elif user_choice in ['Yes', 'No']:
            user_options = ['continue']
        elif user_choice in ['Happy', 'Sad', 'Angry', 'Neutral']:
            user_options = ['continue']
        else:
            user_options = ['open_text']
        
        response_data = {
            'chatbot_response': chatbot_response,
            'user_options': user_options
        }
        
        print(f"回复数据: {response_data}")
        return jsonify(response_data)
        
    except Exception as e:
        print(f"更新会话异常: {e}")
        return jsonify({
            'error': f'服务器错误: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("启动测试服务器...")
    print("支持的测试账号:")
    for username in users:
        print(f"  用户名: {username}, 密码: {users[username]['password']}")
    
    app.run(host='0.0.0.0', port=5001, debug=False)