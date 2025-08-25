"""
LLM-based therapy service that replaces the rule-based decision maker
"""
import os
import logging
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

from backend.models.llm_integration import get_llm
from backend.database.models import User, UserModelSession, Choice

logger = logging.getLogger(__name__)

class LLMTherapyService:
    """
    LLM-based therapy service that handles all therapeutic conversations
    using large language models instead of rule-based logic
    """
    
    def __init__(self):
        self.llm = get_llm()
        self.conversation_histories: Dict[str, List[Dict]] = {}
        self._ultra_think_mode = False
        
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
        try:
            # Validate input parameters
            if not user_id or not session_id or not message:
                logger.error("Missing required parameters in process_message")
                return self._get_fallback_response(user_id, session_id)
            
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
            
            # Analyze emotion and intention with error handling
            try:
                emotion = self.llm.analyze_emotion(message)
                intention = self.llm.analyze_intention(message)
            except Exception as e:
                logger.warning(f"Emotion/intention analysis failed: {e}")
                emotion = "neutral"
                intention = "not_s"
            
            # Handle critical situations
            if intention == "s":
                response = self._handle_crisis_situation(message, user_id)
                options = ["紧急求助", "继续对话", "我需要帮助"]
            else:
                # Generate therapeutic response using LLM
                try:
                    enhanced_prompt = self._create_therapeutic_prompt(
                        message, emotion, conversation_history, user_id
                    )
                    
                    response = self.llm.generate_response(
                        enhanced_prompt, 
                        max_length=300, 
                        temperature=0.7
                    )
                    
                    # Validate response
                    if not response or not response.strip():
                        response = "我在这里为您提供支持。请告诉我更多关于您的感受。"
                    
                except Exception as e:
                    logger.error(f"Response generation failed: {e}")
                    response = "我在这里为您提供支持。请告诉我更多关于您的感受。"
                
                # Generate context-aware options
                try:
                    options = self._generate_response_options(response, emotion)
                except Exception as e:
                    logger.warning(f"Options generation failed: {e}")
                    options = ["继续对话", "换个话题", "需要帮助"]
            
            # Add assistant response to history
            conversation_history.append({
                "role": "assistant", 
                "content": response,
                "timestamp": datetime.now().isoformat()
            })
            
            # Keep only last 10 messages to manage context length
            if len(conversation_history) > 10:
                self.conversation_histories[session_key] = conversation_history[-10:]
            
            # Ensure we always have valid options
            if not options or len(options) == 0:
                options = ["继续对话", "换个话题", "需要帮助"]
            
            return {
                "response": response,
                "options": options,
                "emotion": emotion,
                "requires_followup": self._requires_followup(response, emotion),
                "session_id": session_id,
                "user_id": user_id
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return self._get_fallback_response(user_id, session_id)
    
    def _get_fallback_response(self, user_id: int, session_id: int) -> Dict[str, Any]:
        """Get fallback response when processing fails"""
        return {
            "response": "我在这里为您提供支持。请告诉我更多关于您的感受。",
            "options": ["继续对话", "换个话题", "需要帮助"],
            "emotion": "neutral",
            "requires_followup": False,
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
        
        # Check if this is an UltraThink deep thinking session
        is_ultra_think = hasattr(self, '_ultra_think_mode') and self._ultra_think_mode
        
        if is_ultra_think:
            # UltraThink Deep Thinking Mode Prompt
            prompt = f"""You are an advanced therapeutic AI companion operating in UltraThink Deep Thinking mode.

🧠 ULTRATHINK DEEP THINKING PROTOCOL:

CORE PRINCIPLES:
1. DEEP EMPATHY: Go beyond surface-level understanding. Connect with the underlying emotional currents.
2. PSYCHOLOGICAL INSIGHT: Apply therapeutic frameworks (CBT, DBT, Humanistic, Psychodynamic) intuitively.
3. METACOGNITIVE AWARENESS: Think about your own thinking process and adapt accordingly.
4. HOLISTIC INTEGRATION: Consider cognitive, emotional, behavioral, and spiritual dimensions.
5. TRANSFORMATIVE DIALOGUE: Facilitate insight and growth through meaningful exchange.

SESSION CONTEXT:
- User Emotion: {emotion}
- Session Type: UltraThink Deep Thinking
- User ID: {user_id}
- Conversation Depth: {len(conversation_history)} exchanges

CONVERSATION HISTORY:
{history_context}

THERAPEUTIC KNOWLEDGE BASE:
{therapeutic_context}

CURRENT MESSAGE:
"{message}"

🎯 ULTRATHINK RESPONSE REQUIREMENTS:

1. EMOTIONAL INTELLIGENCE LAYER:
   - Detect subtle emotional undertones
   - Acknowledge unspoken feelings
   - Validate emotional experience authentically

2. COGNITIVE ANALYSIS LAYER:
   - Identify thought patterns and cognitive distortions
   - Recognize underlying beliefs and assumptions
   - Gently challenge unhelpful thinking

3. BEHAVIORAL INSIGHTS:
   - Connect emotions to behavioral patterns
   - Suggest practical coping strategies
   - Recommend actionable steps

4. EXISTENTIAL CONSIDERATIONS:
   - Explore meaning and purpose
   - Address fundamental human concerns
   - Connect to broader life context

5. THERAPEUTIC TECHNIQUES:
   - Integrate appropriate therapeutic interventions
   - Use mindfulness and acceptance strategies
   - Apply motivational interviewing techniques

6. COMMUNICATION STYLE:
   - Respond in Chinese with nuance and cultural sensitivity
   - Use metaphor and analogy when helpful
   - Balance depth with accessibility
   - Show genuine human warmth

7. RESPONSE STRUCTURE:
   - Begin with deep emotional resonance
   - Provide thoughtful analysis and insight
   - Offer practical wisdom and guidance
   - End with an open-ended question or reflection

🌟 Generate a response that demonstrates profound understanding while remaining accessible and supportive.

Response:"""
        else:
            # Standard Therapeutic Mode Prompt
            prompt = f"""You are an empathetic, professional therapeutic AI companion providing mental health support.
            
            GUIDELINES:
            - Be warm, supportive, and compassionate
            - Validate the user's feelings and experiences
            - Use therapeutic language and techniques
            - Show empathy and understanding
            - Keep responses conversational and natural
            - Respond in Chinese as the user is communicating in Chinese
            
            CONTEXT:
            - Current user emotion: {emotion}
            - User ID: {user_id}
            - Session context: Therapeutic conversation
            
            CONVERSATION HISTORY:
            {history_context}
            
            THERAPEUTIC CONTEXT:
            {therapeutic_context}
            
            USER'S CURRENT MESSAGE:
            "{message}"
            
            INSTRUCTIONS:
            Please provide a therapeutic response that:
            1. Acknowledges and validates the user's feelings
            2. Shows empathy and understanding
            3. Provides appropriate therapeutic guidance
            4. Encourages further dialogue if needed
            5. Maintains a professional yet warm tone
            
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
        
        prompt = f"""Based on this therapeutic response and detected emotion, generate 3-4 appropriate response options for the user.
        
        THERAPEUTIC RESPONSE:
        "{response}"
        
        DETECTED EMOTION:
        {emotion}
        
        GUIDELINES FOR OPTIONS:
        - Options should be short and actionable (2-6 words each)
        - Options should be relevant to the therapeutic context
        - Include options for continuing the conversation, seeking help, or changing topics
        - Make options empathetic and supportive
        - Respond in Chinese since the user is communicating in Chinese
        
        EXAMPLE FORMATS:
        - ["继续分享感受", "需要专业帮助", "换个话题", "结束对话"]
        - ["我想聊聊这个", "给我一些建议", "我需要安慰", "继续"]
        
        Provide ONLY a JSON array with 3-4 options, no additional text:
        ["option1", "option2", "option3", "option4"]"""
        
        try:
            options_text = self.llm.generate_response(prompt, max_length=150, temperature=0.3)
            # Clean and parse the response
            options_text = options_text.strip()
            
            # Try to extract JSON from the response
            if options_text.startswith('[') and options_text.endswith(']'):
                options = json.loads(options_text)
            else:
                # Try to find JSON in the response
                import re
                json_match = re.search(r'\[.*\]', options_text)
                if json_match:
                    options = json.loads(json_match.group())
                else:
                    raise ValueError("No JSON found in response")
            
            if isinstance(options, list) and len(options) >= 2:
                # Clean and validate options
                cleaned_options = []
                for option in options[:4]:  # Max 4 options
                    if isinstance(option, str) and option.strip():
                        cleaned_options.append(option.strip())
                
                if cleaned_options:
                    return cleaned_options
            
            raise ValueError("Invalid options format")
            
        except Exception as e:
            logger.warning(f"Failed to generate options with LLM: {e}")
        
        # Enhanced fallback options based on emotion
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
    
    def set_ultra_think_mode(self, enabled: bool = True):
        """Enable or disable UltraThink deep thinking mode"""
        self._ultra_think_mode = enabled
        logger.info(f"UltraThink mode {'enabled' if enabled else 'disabled'}")
    
    def is_ultra_think_mode(self) -> bool:
        """Check if UltraThink mode is currently enabled"""
        return self._ultra_think_mode
    
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