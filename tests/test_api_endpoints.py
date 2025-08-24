#!/usr/bin/env python3
"""
Test script for new API endpoints
"""

import requests
import json
import tempfile
import os

def test_api_endpoints():
    """Test the new API endpoints"""
    base_url = "http://localhost:5000"
    
    print("Testing API Endpoints...")
    
    # Test 1: Generate speech endpoint
    print("1. Testing /api/generate_speech...")
    try:
        response = requests.post(
            f"{base_url}/api/generate_speech",
            json={
                "text": "Hello, I'm here to support you. How are you feeling today?",
                "user_emotion": "neutral"
            }
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: User insights endpoint
    print("\n2. Testing /api/user_insights...")
    try:
        response = requests.get(
            f"{base_url}/api/user_insights?user_id=test_user"
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Daily check-in endpoint
    print("\n3. Testing /api/daily_checkin...")
    try:
        response = requests.get(
            f"{base_url}/api/daily_checkin?user_id=test_user"
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\nAPI endpoint tests completed!")

if __name__ == "__main__":
    test_api_endpoints()