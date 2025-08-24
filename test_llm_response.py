#!/usr/bin/env python3
"""
Test script to verify LLM response to "你是谁？"
"""

import sys
import os

# Add backend to path
sys.path.insert(0, '/Users/liuyanjun/therapy_agent/backend')

from models.llm_integration import LLMIntegration

def test_llm_response():
    """Test LLM response to 你是谁？"""
    print("Testing LLM response to '你是谁？'...")
    
    # Create LLM instance that will use fallback responses
    llm = LLMIntegration(api_type='custom', api_base='http://invalid-url')
    
    # Test direct responsedan shi
    print("\n1. Direct response to '你是谁？':")
    response = llm.generate_response('你是谁？', max_length=100)
    print(f"   Response: {response}")
    
    # Test with therapeutic context
    print("\n2. Response with therapeutic context:")
    therapeutic_prompt = """用户问：你是谁？

请以治疗助手的身份回答这个问题，介绍自己是一个 empathetic therapeutic AI companion。
用中文回答，保持温暖、支持性和专业性。"""
    
    response2 = llm.generate_response(therapeutic_prompt, max_length=150)
    print(f"   Response: {response2}")
    
    # Test emotion analysis
    print("\n3. Emotion analysis of '你是谁？':")
    emotion = llm.analyze_emotion('你是谁？')
    print(f"   Emotion: {emotion}")
    
    # Test intention analysis
    print("\n4. Intention analysis of '你是谁？':")
    intention = llm.analyze_intention('你是谁？')
    print(f"   Intention: {intention}")
    
    print("\n" + "="*60)
    print("SUMMARY:")
    print("The LLM integration is currently using fallback responses")
    print("because the external API services (OpenAI/DeepSeek) are not accessible.")
    print("Fallback responses are generic therapeutic messages rather than")
    print("specific answers to identity questions like '你是谁？'")

if __name__ == "__main__":
    test_llm_response()