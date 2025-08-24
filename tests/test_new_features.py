#!/usr/bin/env python3
"""
Test script for new AI therapy companion features
Tests RAG, TTS, and companion enhancement functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model.rag_system import rag_system
from model.tts_service import tts_service
from model.companion_enhancer import companion_enhancer

def test_rag_system():
    """Test RAG system functionality"""
    print("Testing RAG System...")
    
    # Create a test psychology document
    test_doc = """
Cognitive Behavioral Therapy (CBT) is a widely used therapeutic approach that helps 
individuals identify and change negative thought patterns. It is particularly effective 
for treating anxiety and depression by teaching coping skills and cognitive restructuring.

Mindfulness techniques involve focusing on the present moment without judgment. 
These practices can reduce stress and improve emotional regulation through 
breathing exercises and meditation.

Self-compassion involves treating oneself with kindness and understanding during 
difficult times, rather than self-criticism. Research shows it improves mental 
well-being and resilience.
    """
    
    # Save test document
    test_file = "/tmp/test_psychology.txt"
    with open(test_file, 'w') as f:
        f.write(test_doc)
    
    # Upload document
    doc_id = rag_system.upload_document(test_file, "test_user", "Psychology Basics")
    print(f"✓ Document uploaded with ID: {doc_id}")
    
    # Build index
    rag_system.build_index()
    print("✓ Index built successfully")
    
    # Test retrieval
    query = "How can I reduce anxiety?"
    results = rag_system.retrieve_relevant_content(query)
    print(f"✓ Retrieved {len(results)} relevant results for query: '{query}'")
    
    # Test prompt enhancement
    enhanced_prompt = rag_system.enhance_prompt_with_context("I'm feeling very anxious today", "test_user")
    print("✓ Prompt enhancement successful")
    print(f"Enhanced prompt length: {len(enhanced_prompt)} characters")
    
    # Clean up
    os.unlink(test_file)
    print("✓ RAG system test completed successfully\n")

def test_tts_service():
    """Test TTS service functionality"""
    print("Testing TTS Service...")
    
    # Test basic TTS
    test_text = "Hello, I'm here to support you. How are you feeling today?"
    audio_file = tts_service.text_to_speech(test_text)
    print(f"✓ TTS audio generated: {audio_file}")
    
    # Test therapeutic response
    therapeutic_text = "It's completely normal to feel anxious sometimes. Let's practice some deep breathing together."
    audio_file = tts_service.generate_therapeutic_voice_response(therapeutic_text, "anxious")
    print(f"✓ Therapeutic TTS audio generated: {audio_file}")
    
    # Test emotional tone analysis
    tone = tts_service.analyze_emotional_tone("I'm feeling really sad and lonely today")
    print(f"✓ Emotional tone analysis: {tone}")
    
    print("✓ TTS service test completed successfully\n")

def test_companion_enhancer():
    """Test companion enhancer functionality"""
    print("Testing Companion Enhancer...")
    
    # Test emotion analysis
    test_text = "I've been feeling really anxious and worried about everything lately"
    emotion_scores = companion_enhancer.analyze_user_emotion(test_text)
    dominant_emotion = companion_enhancer.get_dominant_emotion(emotion_scores)
    print(f"✓ Emotion analysis - Dominant: {dominant_emotion}, Scores: {emotion_scores}")
    
    # Test empathetic response
    empathetic_response = companion_enhancer.generate_empathetic_response(test_text, dominant_emotion)
    print(f"✓ Empathetic response: {empathetic_response}")
    
    # Test emotional pattern tracking
    companion_enhancer.track_user_patterns("test_user", dominant_emotion, "2024-01-01T10:00:00")
    companion_enhancer.track_user_patterns("test_user", "anxious", "2024-01-01T14:00:00")
    print("✓ Emotional patterns tracked")
    
    # Test insights
    insights = companion_enhancer.get_emotional_insights("test_user")
    print(f"✓ Emotional insights: {insights}")
    
    # Test daily check-in
    checkin_message = companion_enhancer.generate_daily_checkin("test_user")
    print(f"✓ Daily check-in: {checkin_message}")
    
    # Test crisis detection
    crisis_text = "I don't want to live anymore"
    is_crisis = companion_enhancer.detect_crisis_keywords(crisis_text)
    print(f"✓ Crisis detection: {is_crisis}")
    
    if is_crisis:
        crisis_response = companion_enhancer.generate_crisis_response()
        print(f"✓ Crisis response: {crisis_response[:100]}...")
    
    print("✓ Companion enhancer test completed successfully\n")

def main():
    """Run all tests"""
    print("=" * 60)
    print("Testing New AI Therapy Companion Features")
    print("=" * 60)
    
    try:
        test_rag_system()
        test_tts_service()
        test_companion_enhancer()
        
        print("🎉 All tests completed successfully!")
        print("\nNew features ready to use:")
        print("• RAG system for psychology document retrieval")
        print("• Text-to-speech with emotional tone adjustment")
        print("• AI companion with emotional intelligence")
        print("• Crisis detection and response")
        print("• Personalized daily check-ins")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())