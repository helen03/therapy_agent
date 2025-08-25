#!/usr/bin/env python3
"""
Direct LLM module test
"""
import sys
import os

# Add backend to path
sys.path.insert(0, '/Users/liuyanjun/therapy_agent/backend')

# Set environment variables
os.environ['PYTHONPATH'] = '/Users/liuyanjun/therapy_agent/backend'

try:
    # Import LLM integration directly
    from backend.models.llm_integration import LLMIntegration, MockLLM
    
    print("Testing LLM Integration...")
    
    # Test MockLLM first
    print("\n=== Testing MockLLM ===")
    mock_llm = MockLLM()
    
    print(f"MockLLM Type: {mock_llm.api_type}")
    print(f"MockLLM API Base: {mock_llm.api_base}")
    
    # Test emotion analysis
    print("\nTesting emotion analysis...")
    emotion = mock_llm.analyze_emotion("我感到很开心今天")
    print(f"Emotion analysis result: {emotion}")
    
    # Test response generation
    print("\nTesting response generation...")
    response = mock_llm.generate_response("Hello, how are you?", max_length=50)
    print(f"Generated response: {response}")
    
    # Test intention analysis
    print("\nTesting intention analysis...")
    intention = mock_llm.analyze_intention("我想好好活着")
    print(f"Intention analysis result: {intention}")
    
    # Test with sad emotion
    print("\nTesting sad emotion...")
    emotion_sad = mock_llm.analyze_emotion("我感到很伤心和难过")
    print(f"Sad emotion result: {emotion_sad}")
    
    # Test crisis intention
    print("\nTesting crisis intention...")
    crisis_intention = mock_llm.analyze_intention("我不想活了，想自杀")
    print(f"Crisis intention result: {crisis_intention}")
    
    print("\n✅ MockLLM test completed successfully!")
    
    # Test real LLM if available
    print("\n=== Testing Real LLM Integration ===")
    try:
        real_llm = LLMIntegration()
        print(f"Real LLM Type: {real_llm.api_type}")
        print(f"Real LLM API Base: {real_llm.api_base}")
        
        # Test if API key is available
        if real_llm.api_key:
            print("API key is available")
            
            # Test a simple API call
            print("\nTesting real API call...")
            real_response = real_llm.generate_response("Hello", max_length=20)
            print(f"Real API response: {real_response}")
        else:
            print("No API key available - using fallback mode")
            
    except Exception as e:
        print(f"Real LLM test failed: {e}")
    
    print("\n✅ All LLM tests completed!")
    
except Exception as e:
    print(f"❌ LLM test failed: {e}")
    import traceback
    traceback.print_exc()