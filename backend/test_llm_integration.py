import os
import sys
sys.path.append('.')

from backend.models.llm_integration import LLMIntegration

# 测试LLM集成
def test_llm_integration():
    llm = LLMIntegration(
        api_type="openai",
        api_key="sk-d2950dd850b34dcc960705c1d3d8b350",
        api_base="https://api.deepseek.com/v1"
    )
    
    print(f"API Base: {llm.api_base}")
    print(f"API Type: {llm.api_type}")
    
    # 测试情感分析
    print("Testing emotion analysis...")
    emotion = llm.analyze_emotion("I am feeling anxious today")
    print(f"Emotion: {emotion}")
    
    # 测试响应生成
    print("Testing response generation...")
    response = llm.generate_response("I need help with my anxiety", max_length=100)
    print(f"Response: {response}")

if __name__ == "__main__":
    test_llm_integration()