#!/usr/bin/env python3
"""
Simple LLM integration test
"""
import sys
import os

# Add backend to path
sys.path.insert(0, '/Users/liuyanjun/therapy_agent/backend')

# Set environment variables
os.environ['PYTHONPATH'] = '/Users/liuyanjun/therapy_agent/backend'

try:
    from backend.models.llm_integration import get_llm
    
    print("Testing LLM Integration...")
    llm = get_llm()
    
    print(f"LLM Type: {llm.api_type}")
    print(f"API Base: {llm.api_base}")
    
    # Test emotion analysis
    print("\nTesting emotion analysis...")
    emotion = llm.analyze_emotion("我感到很开心今天")
    print(f"Emotion analysis result: {emotion}")
    
    # Test response generation
    print("\nTesting response generation...")
    response = llm.generate_response("Hello, how are you?", max_length=50)
    print(f"Generated response: {response}")
    
    # Test intention analysis
    print("\nTesting intention analysis...")
    intention = llm.analyze_intention("我想好好活着")
    print(f"Intention analysis result: {intention}")
    
    print("\n✅ LLM Integration test completed successfully!")
    
except Exception as e:
    print(f"❌ LLM Integration test failed: {e}")
    import traceback
    traceback.print_exc()