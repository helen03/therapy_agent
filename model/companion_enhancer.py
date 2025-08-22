"""
AI Companion Enhancer for Therapy Agent
Adds emotional intelligence, memory, and personalized interactions
"""

import logging
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import re

logger = logging.getLogger(__name__)

class CompanionEnhancer:
    """Enhances AI companionship with emotional intelligence and personalization"""
    
    def __init__(self):
        self.user_profiles = {}
        self.daily_checkins = {}
        self.emotional_patterns = {}
    
    def analyze_user_emotion(self, text: str) -> Dict[str, float]:
        """Analyze emotional content of user text"""
        emotion_scores = {
            'happy': 0.0,
            'sad': 0.0,
            'angry': 0.0,
            'anxious': 0.0,
            'neutral': 0.5  # Default neutral score
        }
        
        text_lower = text.lower()
        
        # Emotional keyword analysis
        emotion_keywords = {
            'happy': ['happy', 'joy', 'good', 'great', 'wonderful', 'excited', 'love'],
            'sad': ['sad', 'unhappy', 'depressed', 'cry', 'tears', 'lonely', 'miss'],
            'angry': ['angry', 'mad', 'hate', 'frustrated', 'annoyed', 'upset'],
            'anxious': ['anxious', 'worried', 'nervous', 'scared', 'afraid', 'stress']
        }
        
        for emotion, keywords in emotion_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            emotion_scores[emotion] = min(1.0, count * 0.3)  # Cap at 1.0
        
        # Adjust neutral score based on other emotions
        total_emotion = sum(emotion_scores.values()) - emotion_scores['neutral']
        emotion_scores['neutral'] = max(0.1, 1.0 - total_emotion)
        
        return emotion_scores
    
    def get_dominant_emotion(self, emotion_scores: Dict[str, float]) -> str:
        """Get the dominant emotion from scores"""
        return max(emotion_scores.items(), key=lambda x: x[1])[0]
    
    def generate_empathetic_response(self, user_text: str, user_emotion: str) -> str:
        """Generate empathetic response based on user emotion"""
        empathy_responses = {
            'happy': [
                "I'm so glad to hear you're feeling happy! 😊",
                "That's wonderful to hear! Your happiness brings me joy too.",
                "I'm smiling with you! It's beautiful to see you feeling good."
            ],
            'sad': [
                "I'm here with you during this difficult time. 💙",
                "It's okay to feel sad. I'm listening and I care about you.",
                "I understand this is hard. You're not alone in this."
            ],
            'angry': [
                "I hear your frustration. It's valid to feel angry about this.",
                "Let's breathe through this together. I'm here to support you.",
                "Your feelings are completely understandable. Would you like to talk more about what's making you angry?"
            ],
            'anxious': [
                "I sense your anxiety. Let's take a moment to breathe together. 🌬️",
                "It's okay to feel anxious. I'm here to help you through this.",
                "I understand this feels overwhelming. We can work through it step by step."
            ],
            'neutral': [
                "Thank you for sharing with me. I'm here to listen. 🤗",
                "I appreciate you opening up. How can I support you today?",
                "I'm listening carefully. Please tell me more about what's on your mind."
            ]
        }
        
        return random.choice(empathy_responses.get(user_emotion, empathy_responses['neutral']))
    
    def track_user_patterns(self, user_id: str, emotion: str, timestamp: datetime) -> None:
        """Track emotional patterns for personalized care"""
        if user_id not in self.emotional_patterns:
            self.emotional_patterns[user_id] = []
        
        self.emotional_patterns[user_id].append({
            'emotion': emotion,
            'timestamp': timestamp,
            'time_of_day': timestamp.hour
        })
        
        # Keep only last 100 entries per user
        if len(self.emotional_patterns[user_id]) > 100:
            self.emotional_patterns[user_id] = self.emotional_patterns[user_id][-100:]
    
    def get_emotional_insights(self, user_id: str) -> Dict:
        """Get insights about user's emotional patterns"""
        if user_id not in self.emotional_patterns or not self.emotional_patterns[user_id]:
            return {}
        
        patterns = self.emotional_patterns[user_id]
        
        # Analyze emotional frequency
        emotion_counts = {}
        time_patterns = {}
        
        for entry in patterns:
            emotion = entry['emotion']
            time_of_day = entry['time_of_day']
            
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            # Categorize time of day
            time_category = 'morning' if 5 <= time_of_day < 12 else \
                          'afternoon' if 12 <= time_of_day < 17 else \
                          'evening' if 17 <= time_of_day < 22 else 'night'
            
            if time_category not in time_patterns:
                time_patterns[time_category] = {}
            time_patterns[time_category][emotion] = time_patterns[time_category].get(emotion, 0) + 1
        
        # Find dominant emotion
        total_entries = len(patterns)
        dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else 'neutral'
        
        return {
            'total_interactions': total_entries,
            'emotion_distribution': {k: v/total_entries for k, v in emotion_counts.items()},
            'dominant_emotion': dominant_emotion,
            'time_patterns': time_patterns,
            'last_7_days': len([p for p in patterns if p['timestamp'] > datetime.now() - timedelta(days=7)])
        }
    
    def needs_daily_checkin(self, user_id: str) -> bool:
        """Check if user needs a daily check-in"""
        if user_id not in self.daily_checkins:
            return True
        
        last_checkin = self.daily_checkins[user_id]
        return datetime.now() - last_checkin > timedelta(hours=24)
    
    def record_checkin(self, user_id: str) -> None:
        """Record daily check-in"""
        self.daily_checkins[user_id] = datetime.now()
    
    def generate_daily_checkin(self, user_id: str) -> str:
        """Generate personalized daily check-in message"""
        insights = self.get_emotional_insights(user_id)
        
        checkin_messages = [
            "Good morning! 🌞 How are you feeling today?",
            "Hello there! I've been thinking about you. How's your day going?",
            "Just checking in on you. How are things today? 💭",
            "I'm here for you. How are you feeling right now?"
        ]
        
        # Add personalized touch based on insights
        if insights:
            dominant_emotion = insights.get('dominant_emotion')
            if dominant_emotion == 'sad':
                checkin_messages.append("I know things have been tough lately. How are you holding up today?")
            elif dominant_emotion == 'anxious':
                checkin_messages.append("I remember you've been feeling anxious. How are you managing today?")
        
        return random.choice(checkin_messages)
    
    def enhance_with_personalization(self, response: str, user_id: str) -> str:
        """Add personalization to AI responses"""
        insights = self.get_emotional_insights(user_id)
        
        if not insights:
            return response
        
        # Add occasional personalized touches
        if random.random() < 0.3:  # 30% chance to personalize
            dominant_emotion = insights.get('dominant_emotion')
            
            personalization_phrases = {
                'happy': "I always enjoy our conversations when you're feeling happy. ",
                'sad': "I know things have been difficult, and I admire your strength. ",
                'anxious': "I remember you've been working through anxiety - that takes courage. ",
                'angry': "I appreciate you sharing your frustrations with me. "
            }
            
            if dominant_emotion in personalization_phrases:
                response = personalization_phrases[dominant_emotion] + response
        
        return response
    
    def detect_crisis_keywords(self, text: str) -> bool:
        """Detect potential crisis situations"""
        crisis_keywords = [
            'suicide', 'kill myself', 'end my life', 'want to die',
            'not worth living', 'better off dead', 'no reason to live',
            'harm myself', 'self harm', 'hurting myself'
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in crisis_keywords)
    
    def generate_crisis_response(self) -> str:
        """Generate appropriate response for crisis situations"""
        crisis_responses = [
            "I'm very concerned about what you're sharing. Please know that your life is precious and there are people who care about you deeply. ",
            "This sounds very serious. Your safety is the most important thing right now. ",
            "I hear how much pain you're in, and I want to make sure you get the support you need. "
        ]
        
        resources = """
        **Immediate Resources:**
        • National Suicide Prevention Lifeline: 988 or 1-800-273-8255
        • Crisis Text Line: Text HOME to 741741
        • Emergency Services: 911
        
        Please reach out to one of these resources right now. You don't have to go through this alone.
        """
        
        return random.choice(crisis_responses) + resources

# Global companion enhancer instance
companion_enhancer = CompanionEnhancer()