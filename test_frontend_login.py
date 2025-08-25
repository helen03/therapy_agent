#!/usr/bin/env python3
"""
Test script to verify frontend login functionality
"""

import requests
import json

def test_frontend_login():
    """Test the exact login flow that the frontend Login.js component uses"""
    print("Testing Frontend Login Flow...")
    
    # Test data
    test_cases = [
        {
            'name': 'Valid User (user1)',
            'username': 'user1',
            'password': 'ph6n76gec9',
            'expected_success': True
        },
        {
            'name': 'Invalid User',
            'username': 'nonexistent',
            'password': 'wrongpassword',
            'expected_success': False
        },
        {
            'name': 'Wrong Password',
            'username': 'user1',
            'password': 'wrongpassword',
            'expected_success': False
        }
    ]
    
    api_base_url = 'http://localhost:5000'
    
    for test_case in test_cases:
        print(f"\n--- Testing: {test_case['name']} ---")
        
        try:
            # Make the exact same request as the frontend
            response = requests.post(
                f"{api_base_url}/api/login",
                json={
                    'user_info': {
                        'username': test_case['username'],
                        'password': test_case['password']
                    }
                },
                timeout=10
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
                
                # Check if response matches frontend expectations
                if data.get('success') and data.get('validID'):
                    print("✓ Login successful")
                    
                    # Check required fields for frontend
                    required_fields = ['userID', 'sessionID', 'token', 'model_prompt', 'choices']
                    for field in required_fields:
                        if field in data:
                            print(f"  ✓ {field}: present")
                        else:
                            print(f"  ✗ {field}: missing")
                    
                    # Check if this matches expected result
                    if test_case['expected_success']:
                        print("✓ Test PASSED - Expected success, got success")
                    else:
                        print("✗ Test FAILED - Expected failure, got success")
                else:
                    print("✗ Login failed")
                    if not test_case['expected_success']:
                        print("✓ Test PASSED - Expected failure, got failure")
                    else:
                        print("✗ Test FAILED - Expected success, got failure")
            else:
                print(f"✗ Request failed with status {response.status_code}")
                print(f"Response: {response.text}")
                
                if not test_case['expected_success']:
                    print("✓ Test PASSED - Expected failure, got failure")
                else:
                    print("✗ Test FAILED - Expected success, got failure")
                    
        except Exception as e:
            print(f"✗ Exception occurred: {e}")
            print("✗ Test FAILED - Exception occurred")
    
    print("\n--- Testing Session Update ---")
    
    # Test session update after successful login
    try:
        # First login
        login_response = requests.post(
            f"{api_base_url}/api/login",
            json={
                'user_info': {
                    'username': 'user1',
                    'password': 'ph6n76gec9'
                }
            },
            timeout=10
        )
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            user_id = login_data.get('userID')
            session_id = login_data.get('sessionID')
            
            print(f"Logged in - User ID: {user_id}, Session ID: {session_id}")
            
            # Test session update
            update_response = requests.post(
                f"{api_base_url}/api/update_session",
                json={
                    'choice_info': {
                        'user_id': user_id,
                        'session_id': session_id,
                        'user_choice': '我很好，谢谢',
                        'input_type': 'any'
                    }
                },
                timeout=10
            )
            
            print(f"Session Update Status: {update_response.status_code}")
            
            if update_response.status_code == 200:
                update_data = update_response.json()
                print("✓ Session update successful")
                print(f"Response: {update_data.get('chatbot_response', 'No response')}")
                
                # Check for frontend expected fields
                expected_fields = ['chatbot_response', 'user_options', 'emotion', 'requires_followup']
                for field in expected_fields:
                    if field in update_data:
                        print(f"  ✓ {field}: present")
                    else:
                        print(f"  ✗ {field}: missing")
            else:
                print(f"✗ Session update failed: {update_response.text}")
        else:
            print(f"✗ Login failed for session update test")
            
    except Exception as e:
        print(f"✗ Session update test failed: {e}")

if __name__ == '__main__':
    test_frontend_login()