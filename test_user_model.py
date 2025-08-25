#!/usr/bin/env python3
import os
from backend import create_app
from backend.database.models import User
from backend import db
import bcrypt

# 创建应用
app = create_app()

def test_user_model(username, password):
    with app.app_context():
        # 检查用户是否存在
        user = User.query.filter_by(username=username).first()
        
        if user:
            print(f"用户 '{username}' 存在。")
            print(f"用户ID: {user.id}")
            print(f"密码哈希: {user.password_hash}")
            
            # 测试User模型的check_password方法
            is_valid = user.check_password(password)
            print(f"User模型密码验证: {'成功' if is_valid else '失败'}")
            
            # 手动验证密码
            manual_valid = bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8'))
            print(f"手动密码验证: {'成功' if manual_valid else '失败'}")
            
            # 打印密码哈希的长度和类型
            print(f"密码哈希长度: {len(user.password_hash)}")
            print(f"密码哈希类型: {type(user.password_hash)}")
            
            return is_valid
        else:
            print(f"用户 '{username}' 不存在。")
            return False

if __name__ == '__main__':
    # 测试用户'user11'
    test_user_model('user11', 'password123')