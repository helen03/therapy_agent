#!/usr/bin/env python3
import os
from backend import create_app
from backend.database.models import User
from backend import db
import bcrypt

# 创建应用
app = create_app()

def verify_and_update_user_password(username, password):
    with app.app_context():
        # 检查用户是否存在
        user = User.query.filter_by(username=username).first()
        
        if user:
            print(f"用户 '{username}' 存在。")
            # 手动验证密码
            is_valid = bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8'))
            print(f"当前密码验证: {'成功' if is_valid else '失败'}")
            print(f"存储的密码哈希: {user.password_hash}")
            
            # 直接更新密码哈希
            print(f"正在直接更新用户 '{username}' 的密码...")
            salt = bcrypt.gensalt()
            new_password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
            user.password_hash = new_password_hash
            
            try:
                db.session.commit()
                print(f"密码更新成功。新密码哈希: {user.password_hash}")
                
                # 验证新密码
                new_is_valid = bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8'))
                print(f"新密码验证: {'成功' if new_is_valid else '失败'}")
                return new_is_valid
            except Exception as e:
                db.session.rollback()
                print(f"密码更新失败: {e}")
                return False
        else:
            print(f"用户 '{username}' 不存在。")
            return False

if __name__ == '__main__':
    # 验证并更新用户'user11'的密码
    verify_and_update_user_password('user11', 'password123')