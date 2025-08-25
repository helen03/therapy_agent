#!/usr/bin/env python3
"""
Script to fix password hashes in the database
Converts plain text passwords to bcrypt hashes
"""

import sys
import os
import bcrypt
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.database.models import db, User
from backend import create_app

def fix_passwords():
    """Convert plain text passwords to bcrypt hashes"""
    app = create_app()
    
    with app.app_context():
        # Get all users
        users = User.query.all()
        print(f"Found {len(users)} users")
        
        fixed_count = 0
        for user in users:
            # Check if password is already hashed (bcrypt hashes are typically 60 chars)
            if user.password_hash and len(user.password_hash) < 20:
                print(f"Fixing password for user: {user.username}")
                # Hash the plain text password
                plain_password = user.password_hash
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt).decode('utf-8')
                user.password_hash = hashed_password
                fixed_count += 1
            else:
                print(f"Password for user {user.username} appears to be already hashed")
        
        if fixed_count > 0:
            db.session.commit()
            print(f"Successfully fixed {fixed_count} passwords")
        else:
            print("No passwords needed fixing")

def test_login():
    """Test login functionality"""
    app = create_app()
    
    with app.app_context():
        # Test with user1
        user = User.query.filter_by(username='user1').first()
        if user:
            print(f"User found: {user.username}")
            print(f"Password hash length: {len(user.password_hash)}")
            
            # Test password check
            test_password = 'ph6n76gec9'
            if user.check_password(test_password):
                print("Password check successful!")
            else:
                print("Password check failed!")
        else:
            print("User not found")

if __name__ == '__main__':
    print("Fixing password hashes...")
    fix_passwords()
    
    print("\nTesting login...")
    test_login()
    
    print("\nPassword fix completed!")