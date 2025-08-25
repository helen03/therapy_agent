#!/usr/bin/env python3
import os
from backend import create_app
from backend.database.models import User
from backend import db
import bcrypt

# 创建应用
app = create_app()

def check_and_fix_user(username, new_password=None):
    with app.app_context():
        # 检查用户是否存在
        user = User.query.filter_by(username=username).first()
        
        if user:
            print(f"用户 '{username}' 存在。")
            print(f"用户ID: {user.id}")
            print(f"邮箱: {user.email}")
            print(f"当前密码哈希: {user.password_hash}")
            
            if new_password:
                # 重置密码
                print(f"正在重置用户 '{username}' 的密码...")
                user.set_password(new_password)
                # 手动提交更改
                try:
                    db.session.commit()
                    print(f"密码重置成功。新密码哈希: {user.password_hash}")
                except Exception as e:
                    db.session.rollback()
                    print(f"密码重置失败: {e}")
        else:
            print(f"用户 '{username}' 不存在。")
            
            if new_password:
                # 创建新用户
                print(f"正在创建新用户 '{username}'...")
                new_user = User(username=username)
                new_user.set_password(new_password)
                db.session.add(new_user)
                try:
                    db.session.commit()
                    print(f"用户创建成功。用户ID: {new_user.id}")
                except Exception as e:
                    db.session.rollback()
                    print(f"用户创建失败: {e}")

if __name__ == '__main__':
    # 检查用户'user00'
    check_and_fix_user('user00', 'password')  # 设置一个临时密码