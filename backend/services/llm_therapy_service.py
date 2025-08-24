"""
LLM-based therapy service that replaces the rule-based decision maker
"""
import os
import logging
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

from models.llm_integration import get_llm
from database.models import User, UserModelSession, Choice

logger = logging.getLogger(__name__)

class LLMTherapyService:
    """
    LLM-based therapy service that handles all therapeutic conversations
    using large language models instead of rule-based logic
    """
    
    def __init__(self):
        self.llm = get_llm()
        self.conversation_histories: Dict[str, List[Dict]] = {}
        
    def initialize_session(self, user_id: int, session_id: int) -> Dict[str, Any]:
        """Initialize a new therapy session with LLM"""
        session_key = f"{user_id}_{session_id}"
        self.conversation_histories[session_key] = []
        
        # Generate initial greeting using LLM
        initial_prompt = """You are an empathetic therapeutic AI companion. 
        Greet the user warmly and introduce yourself as their therapy assistant. 
        Ask how they are feeling today and what they would like to talk about.
        Keep it warm, supportive, and professional."""
        
        greeting = self.llm.generate_response(initial_prompt, max_length=150, temperature=0.8)
        
        return {
            "response": greeting,
            "options": ["继续对话", "换个话题", "需要帮助"],
            "session_id": session_id,
            "user_id": user_id
        }
    
    def process_message(self, user_id: int, session_id: int, message: str, 
                       input_type: str = "text") -> Dict[str, Any]:
        """Process user message using LLM and return therapeutic response"""
        session_key = f"{user_id}_{session_id}"
        
        # Get or create conversation history
        if session_key not in self.conversation_histories:
            self.conversation_histories[session_key] = []
        
        conversation_history = self.conversation_histories[session_key]
        
        # Add user message to history
        conversation_history.append({
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Analyze emotion and intention
        emotion = self.llm.analyze_emotion(message)
        intention = self.llm.analyze_intention(message)
        
        # Handle critical situations
        if intention == "s":
            response = self._handle_crisis_situation(message, user_id)
            options = ["紧急求助", "继续对话", "我需要帮助"]
        else:
            # Generate therapeutic response using LLM
            enhanced_prompt = self._create_therapeutic_prompt(
                message, emotion, conversation_history, user_id
            )
            
            response = self.llm.generate_response(
                enhanced_prompt, 
                max_length=300, 
                temperature=0.7
            )
            
            # Generate context-aware options
            options = self._generate_response_options(response, emotion)
        
        # Add assistant response to history
        conversation_history.append({
            "role": "assistant", 
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 10 messages to manage context length
        if len(conversation_history) > 10:
            self.conversation_histories[session_key] = conversation_history[-10:]
        
        return {
            "response": response,
            "options": options,
            "emotion": emotion,
            "requires_followup": self._requires_followup(response, emotion),
            "session_id": session_id,
            "user_id": user_id
        }
    
    def _create_therapeutic_prompt(self, message: str, emotion: str, 
                                 conversation_history: List[Dict], user_id: int) -> str:
        """Create enhanced prompt for therapeutic response generation"""
        
        # Build conversation context
        history_context = ""
        if conversation_history:
            # Use last 3 exchanges for context
            recent_history = conversation_history[-6:]  # Last 3 user-assistant pairs
            for msg in recent_history:
                role = "User" if msg["role"] == "user" else "Assistant"
                history_context += f"{role}: {msg['content']}\n"
        
        # Get therapeutic context from RAG if available
        therapeutic_context = self._get_therapeutic_context(message, emotion, user_id)
        
        prompt = f"""You are an empathetic, professional therapeutic AI companion. 
        Your role is to provide emotional support, therapeutic guidance, and compassionate listening.
        
        Current user emotion detected: {emotion}
        
        Conversation history:
        {history_context}
        
        Therapeutic context:
        {therapeutic_context}
        
        User's current message: "{message}"
        
        Please respond in a warm, supportive, and therapeutic manner. 
        Show empathy, validate feelings, and provide helpful guidance.
        Keep your response conversational and natural.
        
        Response:"""
        
        return prompt
    
    def _get_therapeutic_context(self, message: str, emotion: str, user_id: int) -> str:
        """Get relevant therapeutic knowledge from RAG system"""
        try:
            from backend.models.rag_system import rag_system
            context = rag_system.enhance_prompt_with_context(message, user_id)
            if context and context.strip():
                logger.info(f"RAG context retrieved: {context[:100]}...")
                return context
            else:
                # Fallback therapeutic knowledge based on emotion
                emotion_contexts = {
                    "anxious": "对于焦虑情绪，建议使用深呼吸练习、正念冥想和渐进式肌肉放松技术。",
                    "sad": "对于悲伤情绪，建议进行情绪日记记录、与他人倾诉和进行轻度体育活动。",
                    "angry": "对于愤怒情绪，建议使用冷静技巧、转移注意力和建设性表达方式。",
                    "happy": "对于快乐情绪，建议享受当下、表达感激和与他人分享喜悦。"
                }
                return emotion_contexts.get(emotion, "我在这里为您提供情感支持和专业指导。")
        except Exception as e:
            logger.warning(f"RAG context unavailable: {e}")
            # Provide basic therapeutic context
            return "基于认知行为疗法和正念原则的心理健康支持。"
    
    def _generate_response_options(self, response: str, emotion: str) -> List[str]:
        """Generate context-aware response options using LLM"""
        
        prompt = f"""Based on this therapeutic response and detected emotion ({emotion}), 
        suggest 3-4 short response options that a user might want to choose next:
        
        Response: "{response}"
        
        Emotion: {emotion}
        
        Provide the options as a JSON list without any additional text:
        ["option1", "option2", "option3"]"""
        
        try:
            options_text = self.llm.generate_response(prompt, max_length=100, temperature=0.3)
            # Try to parse as JSON
            options = json.loads(options_text)
            if isinstance(options, list) and len(options) >= 2:
                return options[:4]  # Return max 4 options
        except Exception as e:
            logger.warning(f"Failed to generate options with LLM: {e}")
        
        # Fallback options based on emotion
        fallback_options = {
            "happy": ["继续分享", "讨论其他话题", "寻求建议", "结束对话"],
            "sad": ["需要安慰", "讨论原因", "寻求帮助", "换个话题"],
            "anxious": ["需要安抚", "讨论焦虑源", "放松技巧", "专业帮助"],
            "angry": ["表达感受", "讨论原因", "冷静方法", "寻求支持"],
            "neutral": ["继续对话", "换个话题", "寻求指导", "结束会话"]
        }
        
        return fallback_options.get(emotion, fallback_options["neutral"])
    
    def _requires_followup(self, response: str, emotion: str) -> bool:
        """Determine if this response requires immediate follow-up"""
        # Check for crisis indicators in response
        crisis_keywords = ["紧急", "求助", "危机", "危险", "自杀", "自伤"]
        if any(keyword in response for keyword in crisis_keywords):
            return True
        
        # Emotions that might require follow-up
        critical_emotions = ["sad", "anxious", "angry", "guilty", "ashamed"]
        return emotion in critical_emotions
    
    def _handle_crisis_situation(self, message: str, user_id: int) -> str:
        """Handle crisis situations with appropriate response"""
        
        crisis_prompt = f"""User is expressing potentially suicidal thoughts: "{message}"
        
        Respond as a compassionate mental health professional. 
        Provide immediate emotional support, validate their feelings, 
        and offer crisis resources. Be calm, empathetic, and direct.
        
        Include these elements:
        1. Immediate emotional validation
        2. Concern for their safety  
        3. Crisis hotline information
        4. Encouragement to seek professional help
        5. Offer to continue supporting them
        
        Response:"""
        
        crisis_response = self.llm.generate_response(
            crisis_prompt, 
            max_length=400, 
            temperature=0.3
        )
        
        # Log crisis situation
        logger.critical(f"CRISIS ALERT - User {user_id}: {message}")
        
        return crisis_response
    
    def get_conversation_history(self, user_id: int, session_id: int) -> List[Dict]:
        """Get conversation history for a session"""
        session_key = f"{user_id}_{session_id}"
        return self.conversation_histories.get(session_key, [])
    
    def clear_session(self, user_id: int, session_id: int):
        """Clear conversation history for a session"""
        session_key = f"{user_id}_{session_id}"
        if session_key in self.conversation_histories:
            del self.conversation_histories[session_key]
    
    def summarize_session(self, user_id: int, session_id: int) -> str:
        """Generate session summary using LLM"""
        conversation = self.get_conversation_history(user_id, session_id)
        
        if not conversation:
            return "No conversation history available."
        
        # Format conversation for summarization
        conversation_text = "\n".join([
            f"{msg['role']}: {msg['content']}" for msg in conversation
        ])
        
        summary_prompt = f"""Summarize this therapeutic conversation as a mental health professional:
        
        {conversation_text}
        
        Provide a concise summary focusing on:
        1. Main themes discussed
        2. Emotional patterns observed  
        3. Key insights or breakthroughs
        4. Recommendations for future sessions
        
        Summary:"""
        
        return self.llm.generate_response(summary_prompt, max_length=500, temperature=0.2)

# Global therapy service instance
therapy_service = LLMTherapyService()