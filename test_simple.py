#!/usr/bin/env python3
"""
Simple test to check backend functionality without model loading
"""
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

def test_backend_basics():
    """Test basic backend functionality"""
    print("🧪 Testing Backend Basics...")
    
    try:
        # Test basic imports
        from backend import create_app
        from backend.database.models import User, UserModelSession
        
        print("✅ Backend modules imported successfully")
        
        # Create app instance
        app = create_app()
        print("✅ Flask app created successfully")
        
        # Test database models
        with app.app_context():
            # Test user creation
            user = User(username="test_user", password="test_password")
            print(f"✅ User model: {user.username}")
            
            # Test session creation
            session = UserModelSession(user_id=1)
            print(f"✅ Session model: {session.id}")
        
        print("✅ Database models work correctly")
        return True
        
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_llm_fallback():
    """Test LLM fallback functionality"""
    print("\n🧪 Testing LLM Fallback...")
    
    try:
        from backend.models.llm_integration import LLMIntegration
        
        # Create LLM instance with fallback
        llm = LLMIntegration(model_type="fallback")
        print("✅ LLM fallback instance created")
        
        # Test emotion analysis (should use fallback)
        emotion = llm.analyze_emotion("我今天很开心")
        print(f"✅ Emotion analysis: {emotion}")
        
        # Test text generation (should use fallback)
        response = llm.generate_response("你好")
        print(f"✅ Text generation: {response[:50]}...")
        
        print("✅ LLM fallback functionality works")
        return True
        
    except Exception as e:
        print(f"❌ LLM fallback test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_therapy_service():
    """Test therapy service with fallback"""
    print("\n🧪 Testing Therapy Service...")
    
    try:
        from backend.services.llm_therapy_service import LLMTherapyService
        
        # Create therapy service
        service = LLMTherapyService()
        print("✅ Therapy service created")
        
        # Test message processing
        result = service.process_message(1, 1, "你好，我今天心情不好")
        print(f"✅ Response: {result['response'][:100]}...")
        print(f"✅ Options: {result['options']}")
        
        print("✅ Therapy service works correctly")
        return True
        
    except Exception as e:
        print(f"❌ Therapy service test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Simple Backend Tests")
    print("=" * 50)
    
    success = True
    success &= test_backend_basics()
    success &= test_llm_fallback()
    success &= test_therapy_service()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All basic tests passed!")
        print("\nThe backend is ready for LLM integration.")
        print("You can now start the server and test the API endpoints.")
    else:
        print("❌ Some tests failed. Please check the configuration.")
        sys.exit(1)