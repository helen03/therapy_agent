#!/usr/bin/env python3
import os
import bcrypt
from backend import create_app
from backend.database.models import User
from backend import db
import getpass

# 创建应用
app = create_app()

# 检查bcrypt版本
print(f"bcrypt版本: {bcrypt.__version__}")

# 获取系统上bcrypt的最大盐长度
max_salt_len = bcrypt.gensalt().decode('utf-8').split('$')[3]
print(f"bcrypt盐格式信息: $2b$12${max_salt_len}")

def reset_user_password(username):
    """Reset user password with proper error handling"""
    with app.app_context():
        # 查找用户
        user = User.query.filter_by(username=username).first()
        
        if user:
            print(f"找到用户 '{username}' (ID: {user.id})")
            
            # 打印当前密码哈希
            print(f"当前密码哈希: {user.password_hash}")
            print(f"当前密码哈希长度: {len(user.password_hash)}")
            
            # 获取新密码
            new_password = getpass.getpass("请输入新密码: ")
            confirm_password = getpass.getpass("请确认新密码: ")
            
            if new_password != confirm_password:
                print("密码不匹配!")
                return False
                
            if len(new_password) < 6:
                print("密码长度至少6位!")
                return False
                
            # 使用User模型的set_password方法设置新密码
            print(f"使用User模型的set_password方法设置新密码...")
            user.set_password(new_password)
            
            # 提交更改
            try:
                db.session.commit()
                print(f"密码重置成功")
                print(f"新密码哈希: {user.password_hash}")
                print(f"新密码哈希长度: {len(user.password_hash)}")
                
                # 验证新密码
                is_valid = user.check_password(new_password)
                print(f"新密码验证结果: {is_valid}")
                
                if is_valid:
                    print("\n✅ 密码验证成功！现在登录API应该可以正常工作了。")
                    return True
                else:
                    print("\n❌ 密码验证仍然失败！请检查bcrypt版本和实现。")
                    return False
            except Exception as e:
                db.session.rollback()
                print(f"密码重置失败: {e}")
                return False
        else:
            print(f"未找到用户 '{username}'")
            
            # 如果用户不存在，创建新用户
            print(f"创建新用户 '{username}'...")
            new_password = getpass.getpass("请输入新密码: ")
            confirm_password = getpass.getpass("请确认新密码: ")
            
            if new_password != confirm_password:
                print("密码不匹配!")
                return False
                
            if len(new_password) < 6:
                print("密码长度至少6位!")
                return False
                
            new_user = User(username=username)
            new_user.set_password(new_password)
            db.session.add(new_user)
            try:
                db.session.commit()
                print(f"用户创建成功。用户ID: {new_user.id}")
                print(f"新用户密码哈希: {new_user.password_hash}")
                
                # 验证新密码
                is_valid = new_user.check_password(new_password)
                print(f"新用户密码验证结果: {is_valid}")
                return is_valid
            except Exception as e:
                db.session.rollback()
                print(f"用户创建失败: {e}")
                return False

if __name__ == '__main__':
    # 获取用户名
    username = input("请输入用户名: ") or 'user00'
    reset_user_password(username)