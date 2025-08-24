#!/usr/bin/env python3
"""
Test script to verify LLM integration is working
"""
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_llm_integration():
    """Test basic LLM functionality"""
    print("🧪 Testing LLM Integration...")
    
    try:
        from backend.models.llm_integration import get_llm
        from backend.services.llm_therapy_service import LLMTherapyService
        
        # Test LLM instance creation
        llm = get_llm()
        print("✅ LLM instance created successfully")
        
        # Test emotion analysis
        test_text = "我今天感觉非常开心"
        emotion = llm.analyze_emotion(test_text)
        print(f"✅ Emotion analysis: '{test_text}' -> {emotion}")
        
        # Test text generation
        response = llm.generate_response("你好，请介绍一下你自己", max_length=100)
        print(f"✅ Text generation: {response[:100]}...")
        
        # Test therapy service
        therapy_service = LLMTherapyService()
        test_response = therapy_service.process_message(1, 1, "你好，我今天心情不好")
        print(f"✅ Therapy service response: {test_response['response'][:100]}...")
        print(f"✅ Therapy service options: {test_response['options']}")
        
        print("\n🎉 All LLM integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ LLM integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_backend_api():
    """Test backend API endpoints"""
    print("\n🧪 Testing Backend API...")
    
    try:
        # This would require a running Flask app
        # For now, just check that the modules can be imported
        from backend import create_app
        from backend.database.models import User, UserModelSession
        
        print("✅ Backend modules imported successfully")
        print("✅ Database models available")
        
        # Test that we can create app instance
        app = create_app()
        print("✅ Flask app created successfully")
        
        print("✅ Backend API test completed (basic imports)")
        return True
        
    except Exception as e:
        print(f"❌ Backend API test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting LLM Integration Tests")
    print("=" * 50)
    
    success = True
    success &= test_llm_integration()
    success &= test_backend_api()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! LLM integration is working.")
        print("\nNext steps:")
        print("1. Start the backend server: flask run")
        print("2. Test the API endpoints with curl or Postman")
        print("3. Run the mobile apps to verify integration")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)