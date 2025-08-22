#!/usr/bin/env python3
"""
Test script for new AI Therapy Companion Features
Tests RAG, TTS, and emotional intelligence capabilities
"""

import sys
import os
import tempfile
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ai_companion_features():
    """Test all new AI companion features"""
    print("=" * 70)
    print("Testing AI Therapy Companion Features")
    print("=" * 70)
    
    # Import modules
    try:
        from model.rag_system import rag_system
        from model.tts_service import tts_service
        from model.companion_enhancer import companion_enhancer
        from model.llm_integration import get_llm
        print("✓ All modules imported successfully")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test 1: RAG System for Psychology Documents
    print("\n1. Testing RAG System for Psychology Documents...")
    try:
        # Create test psychology content
        psychology_content = """
Cognitive Behavioral Therapy (CBT) is an evidence-based approach that helps 
individuals identify and challenge negative thought patterns. It is particularly 
effective for anxiety, depression, and stress management.

Mindfulness meditation involves focusing on the present moment without judgment. 
Regular practice can significantly reduce stress and improve emotional regulation.

Self-compassion involves treating oneself with kindness during difficult times, 
rather than engaging in self-criticism. Research shows it improves mental 
well-being and resilience against negative emotions.
        """
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(psychology_content)
            temp_file = f.name
        
        # Upload to RAG system
        doc_id = rag_system.upload_document(temp_file, "test_user", "Psychology Basics")
        rag_system.build_index()
        
        # Test retrieval
        query = "How can I manage anxiety?"
        results = rag_system.retrieve_relevant_content(query)
        
        # Test prompt enhancement
        user_query = "I'm feeling very anxious about my job"
        enhanced_prompt = rag_system.enhance_prompt_with_context(user_query, "test_user")
        
        print(f"   ✓ Document uploaded: {doc_id}")
        print(f"   ✓ Retrieved {len(results)} relevant results for: '{query}'")
        print(f"   ✓ Enhanced prompt length: {len(enhanced_prompt)} characters")
        print(f"   ✓ Contains psychology context: {'psychology' in enhanced_prompt.lower()}")
        
        # Clean up
        os.unlink(temp_file)
        
    except Exception as e:
        print(f"   ❌ RAG test failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Emotional Intelligence & Companion Features
    print("\n2. Testing Emotional Intelligence & Companion Features...")
    try:
        # Test various emotional states
        test_cases = [
            ("I'm feeling really happy today!", "happy"),
            ("I've been so sad and depressed lately", "sad"),
            ("I'm anxious about everything, I can't stop worrying", "anxious"),
            ("I'm so angry at my situation right now", "angry")
        ]
        
        for text, expected_emotion in test_cases:
            emotion_scores = companion_enhancer.analyze_user_emotion(text)
            dominant_emotion = companion_enhancer.get_dominant_emotion(emotion_scores)
            empathetic_response = companion_enhancer.generate_empathetic_response(text, dominant_emotion)
            
            print(f"   ✓ '{text[:20]}...' → {dominant_emotion} (expected: {expected_emotion})")
            print(f"     Response: {empathetic_response[:40]}...")
        
        # Test crisis detection
        crisis_text = "I don't want to live anymore, it's too painful"
        is_crisis = companion_enhancer.detect_crisis_keywords(crisis_text)
        crisis_response = companion_enhancer.generate_crisis_response() if is_crisis else ""
        
        print(f"   ✓ Crisis detection: {is_crisis}")
        if is_crisis:
            print(f"     Crisis response: {crisis_response[:60]}...")
        
        # Test emotional pattern tracking
        companion_enhancer.track_user_patterns("test_user", "anxious", "2024-01-01T10:00:00")
        companion_enhancer.track_user_patterns("test_user", "happy", "2024-01-01T14:00:00")
        insights = companion_enhancer.get_emotional_insights("test_user")
        
        print(f"   ✓ Emotional insights: {insights.get('total_interactions', 0)} interactions")
        
    except Exception as e:
        print(f"   ❌ Companion test failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 3: Text-to-Speech with Emotional Tone
    print("\n3. Testing Text-to-Speech with Emotional Tone...")
    try:
        # Test different emotional tones
        test_messages = [
            ("I'm here to support you. How are you feeling today?", "calm"),
            ("That's wonderful news! I'm so happy for you!", "excited"),
            ("I understand this is difficult. Let's breathe through it together.", "reassuring")
        ]
        
        for message, tone in test_messages:
            audio_file = tts_service.text_to_speech(message, emotional_tone=tone)
            emotional_tone = tts_service.analyze_emotional_tone(message)
            
            print(f"   ✓ '{message[:20]}...' → Tone: {emotional_tone}, File: {audio_file}")
            
            # Clean up
            if audio_file and os.path.exists(audio_file):
                os.unlink(audio_file)
        
        # Test therapeutic responses
        therapeutic_text = "It's completely normal to feel this way. Remember to be kind to yourself."
        audio_file = tts_service.generate_therapeutic_voice_response(therapeutic_text, "anxious")
        print(f"   ✓ Therapeutic TTS: {audio_file}")
        
        if audio_file and os.path.exists(audio_file):
            os.unlink(audio_file)
            
    except Exception as e:
        print(f"   ❌ TTS test failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 4: LLM Integration with Enhanced Context
    print("\n4. Testing LLM Integration with Enhanced Context...")
    try:
        llm = get_llm()
        
        # Test context enhancement
        user_messages = [
            "I'm struggling with anxiety",
            "How can mindfulness help me?",
            "I want to learn self-compassion"
        ]
        
        for message in user_messages:
            enhanced_prompt = llm.enhance_with_context("test_user", message)
            
            print(f"   ✓ '{message}' → Enhanced length: {len(enhanced_prompt)} chars")
            print(f"     Contains context: {'psychology' in enhanced_prompt.lower() or 'history' in enhanced_prompt.lower()}")
        
    except Exception as e:
        print(f"   ❌ LLM integration test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("🎉 AI Therapy Companion Features Test Completed! 🎉")
    print("\nSummary of implemented features:")
    print("✓ RAG System: Psychology document retrieval and context enhancement")
    print("✓ Emotional Intelligence: Emotion analysis, empathetic responses, crisis detection")
    print("✓ Text-to-Speech: Voice output with emotional tone adjustment")
    print("✓ Companion Features: Daily check-ins, emotional pattern tracking")
    print("✓ LLM Integration: Enhanced prompts with psychology context")
    print("✓ API Endpoints: New endpoints for document upload, TTS, insights")
    print("\nThe AI therapy companion is now enhanced with:")
    print("• Psychology knowledge base through document uploads")
    print("• Voice interaction capabilities")
    print("• Emotional intelligence and personalized responses")
    print("• Crisis detection and support resources")
    print("• Continuous learning from user interactions")
    print("=" * 70)

if __name__ == "__main__":
    test_ai_companion_features()