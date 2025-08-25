#!/usr/bin/env python3
import os
from backend import create_app
from backend.database.models import User
from backend import db

# 创建应用
app = create_app()

def reset_user(username, password):
    with app.app_context():
        # 直接使用SQL删除用户
        try:
            db.session.execute(f"DELETE FROM user WHERE username = '{username}'")
            db.session.commit()
            print(f"已删除用户 '{username}'（如果存在）。")
        except Exception as e:
            db.session.rollback()
            print(f"删除用户时出错: {e}")
            
        # 创建新用户
        print(f"正在创建新用户 '{username}'...")
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        
        try:
            db.session.commit()
            print(f"用户 '{username}' 已创建。用户ID: {new_user.id}")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"创建用户失败: {e}")
            return False

if __name__ == '__main__':
    # 重置用户'user11'
    reset_user('user11', 'password123')