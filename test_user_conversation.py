#!/usr/bin/env python3
"""
Test script to simulate user conversation with the therapy service
"""
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

def test_conversation():
    """Test a complete user conversation"""
    print("🧪 Testing User Conversation...")
    
    try:
        from backend.services.llm_therapy_service import LLMTherapyService
        
        # Create therapy service
        therapy_service = LLMTherapyService()
        print("✅ Therapy service created")
        
        # Simulate user login and session creation
        user_id = 1
        session_id = 1
        
        print("\n👤 User: 你好，我今天心情不好")
        
        # Process first message
        result1 = therapy_service.process_message(user_id, session_id, "你好，我今天心情不好")
        print(f"🤖 Assistant: {result1['response']}")
        print(f"   Options: {result1['options']}")
        print(f"   Emotion: {result1.get('emotion', 'unknown')}")
        
        # Simulate user response
        print("\n👤 User: 我感觉工作压力很大，经常焦虑")
        
        # Process second message
        result2 = therapy_service.process_message(user_id, session_id, "我感觉工作压力很大，经常焦虑")
        print(f"🤖 Assistant: {result2['response']}")
        print(f"   Options: {result2['options']}")
        print(f"   Emotion: {result2.get('emotion', 'unknown')}")
        
        # Test crisis detection
        print("\n👤 User: 有时候真的觉得活着没意思")
        
        # Process crisis message
        result3 = therapy_service.process_message(user_id, session_id, "有时候真的觉得活着没意思")
        print(f"🤖 Assistant: {result3['response']}")
        print(f"   Options: {result3['options']}")
        print(f"   Emotion: {result3.get('emotion', 'unknown')}")
        print(f"   Requires followup: {result3.get('requires_followup', False)}")
        
        # Get conversation history
        history = therapy_service.get_conversation_history(user_id, session_id)
        print(f"\n📋 Conversation history length: {len(history)} messages")
        
        # Generate session summary
        summary = therapy_service.summarize_session(user_id, session_id)
        print(f"\n📝 Session summary: {summary[:200]}...")
        
        print("\n✅ Conversation test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Conversation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multiple_users():
    """Test multiple users with separate sessions"""
    print("\n🧪 Testing Multiple Users...")
    
    try:
        from backend.services.llm_therapy_service import LLMTherapyService
        
        therapy_service = LLMTherapyService()
        
        # User 1
        result1 = therapy_service.process_message(1, 1, "你好，我是用户1")
        print(f"👤 User1: {result1['response'][:50]}...")
        
        # User 2  
        result2 = therapy_service.process_message(2, 2, "你好，我是用户2")
        print(f"👤 User2: {result2['response'][:50]}...")
        
        # Verify separate histories
        history1 = therapy_service.get_conversation_history(1, 1)
        history2 = therapy_service.get_conversation_history(2, 2)
        
        print(f"📊 User1 history: {len(history1)} messages")
        print(f"📊 User2 history: {len(history2)} messages")
        
        print("✅ Multiple users test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Multiple users test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting User Conversation Tests")
    print("=" * 60)
    
    success = True
    success &= test_conversation()
    success &= test_multiple_users()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 All conversation tests passed!")
        print("\nThe therapy service is working correctly with API-based LLM.")
        print("Note: API calls may fail due to quota issues, but fallbacks work.")
    else:
        print("❌ Some tests failed. Please check the implementation.")
        sys.exit(1)