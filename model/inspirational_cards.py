"""
Inspirational Card System for Therapy Companion
Provides random inspirational and healing messages for users
"""

import random
from typing import Dict, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class InspirationalCardSystem:
    """System for generating inspirational healing messages"""
    
    def __init__(self):
        self.cards = self._load_inspirational_cards()
        self.user_draw_history = {}
    
    def _load_inspirational_cards(self) -> List[Dict]:
        """Load database of inspirational cards with different categories"""
        return [
            # Hope and Encouragement
            {
                "id": "hope_001",
                "message": "即使是最黑暗的夜晚也会结束，太阳将会升起。",
                "category": "hope",
                "emotional_tone": "encouraging",
                "translation": "Even the darkest night will end, and the sun will rise."
            },
            {
                "id": "hope_002", 
                "message": "你比你自己想象的更坚强。",
                "category": "hope",
                "emotional_tone": "empowering",
                "translation": "You are stronger than you think you are."
            },
            
            # Self-Compassion
            {
                "id": "compassion_001",
                "message": "对自己温柔一些，你正在尽你最大的努力。",
                "category": "self_compassion", 
                "emotional_tone": "gentle",
                "translation": "Be gentle with yourself - you're doing the best you can."
            },
            {
                "id": "compassion_002",
                "message": "允许自己感受所有情绪，它们都是你的一部分。",
                "category": "self_compassion",
                "emotional_tone": "accepting",
                "translation": "Allow yourself to feel all emotions - they are all part of you."
            },
            
            # Mindfulness
            {
                "id": "mindfulness_001",
                "message": "此时此刻，你就在这里，这就足够了。",
                "category": "mindfulness",
                "emotional_tone": "calm",
                "translation": "Right here, right now, you are here - and that is enough."
            },
            {
                "id": "mindfulness_002",
                "message": "呼吸。你就在此刻，一切都好。",
                "category": "mindfulness", 
                "emotional_tone": "peaceful",
                "translation": "Breathe. You are here now. All is well."
            },
            
            # Strength and Resilience
            {
                "id": "strength_001",
                "message": "风暴不会永远持续，你会看到晴朗的天空。",
                "category": "resilience",
                "emotional_tone": "hopeful",
                "translation": "The storm won't last forever - you will see clear skies again."
            },
            {
                "id": "strength_002",
                "message": "每一次挑战都是成长的机会。",
                "category": "resilience",
                "emotional_tone": "motivational",
                "translation": "Every challenge is an opportunity for growth."
            },
            
            # Love and Connection
            {
                "id": "love_001",
                "message": "你值得被爱，包括被你自己爱。",
                "category": "self_love",
                "emotional_tone": "loving",
                "translation": "You are worthy of love, including from yourself."
            },
            {
                "id": "love_002",
                "message": "你的存在本身就是一份礼物。",
                "category": "self_worth",
                "emotional_tone": "affirming",
                "translation": "Your existence itself is a gift."
            },
            
            # Healing and Recovery
            {
                "id": "healing_001",
                "message": "疗愈是一个过程，不是目的地。对自己有耐心。",
                "category": "healing",
                "emotional_tone": "patient",
                "translation": "Healing is a process, not a destination. Be patient with yourself."
            },
            {
                "id": "healing_002",
                "message": "小小的进步也是进步。庆祝每一个步伐。",
                "category": "progress",
                "emotional_tone": "celebratory",
                "translation": "Small progress is still progress. Celebrate every step."
            },
            
            # Additional cards for variety
            {
                "id": "hope_003",
                "message": "新的开始往往伪装成痛苦的结局。",
                "category": "hope",
                "emotional_tone": "wise",
                "translation": "New beginnings are often disguised as painful endings."
            },
            {
                "id": "compassion_003",
                "message": "今天，选择对自己友善。",
                "category": "self_compassion",
                "emotional_tone": "kind",
                "translation": "Today, choose to be kind to yourself."
            },
            {
                "id": "mindfulness_003",
                "message": "当下这一刻是你真正拥有的全部。",
                "category": "mindfulness",
                "emotional_tone": "present",
                "translation": "This present moment is all you truly have."
            }
        ]
    
    def draw_card(self, user_id: str = None, category: str = None) -> Dict:
        """Draw a random inspirational card"""
        # Filter by category if specified
        available_cards = self.cards
        if category:
            available_cards = [card for card in self.cards if card['category'] == category]
        
        if not available_cards:
            # Fallback to all cards if category has no matches
            available_cards = self.cards
        
        # Select random card
        selected_card = random.choice(available_cards)
        
        # Track user draw history
        if user_id:
            self._record_draw(user_id, selected_card['id'])
        
        logger.info(f"Card drawn for user {user_id}: {selected_card['id']}")
        return selected_card
    
    def _record_draw(self, user_id: str, card_id: str) -> None:
        """Record card draw history for user"""
        if user_id not in self.user_draw_history:
            self.user_draw_history[user_id] = []
        
        self.user_draw_history[user_id].append({
            'card_id': card_id,
            'timestamp': datetime.now().isoformat(),
            'date': datetime.now().strftime('%Y-%m-%d')
        })
        
        # Keep only last 100 draws per user
        if len(self.user_draw_history[user_id]) > 100:
            self.user_draw_history[user_id] = self.user_draw_history[user_id][-100:]
    
    def get_user_draw_history(self, user_id: str) -> List[Dict]:
        """Get user's card draw history"""
        return self.user_draw_history.get(user_id, [])
    
    def get_user_favorite_categories(self, user_id: str) -> Dict:
        """Analyze user's preferred card categories"""
        history = self.get_user_draw_history(user_id)
        if not history:
            return {}
        
        # Count category occurrences
        category_count = {}
        for draw in history:
            card = next((c for c in self.cards if c['id'] == draw['card_id']), None)
            if card:
                category = card['category']
                category_count[category] = category_count.get(category, 0) + 1
        
        return category_count
    
    def draw_personalized_card(self, user_id: str, current_emotion: str = None) -> Dict:
        """Draw a card personalized to user's current emotional state"""
        emotion_to_category = {
            'sad': 'hope',
            'anxious': 'mindfulness', 
            'angry': 'self_compassion',
            'happy': 'celebration',
            'neutral': 'inspiration'
        }
        
        # Get preferred category based on emotion
        preferred_category = emotion_to_category.get(current_emotion, None)
        
        # Also consider user's historical preferences
        user_preferences = self.get_user_favorite_categories(user_id)
        if user_preferences:
            # Weight random selection towards user's preferred categories
            preferred_category = max(user_preferences.items(), key=lambda x: x[1])[0]
        
        return self.draw_card(user_id, preferred_category)
    
    def get_daily_card(self, user_id: str) -> Dict:
        """Get today's daily card (same card for user throughout the day)"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Check if user already drew a card today
        history = self.get_user_draw_history(user_id)
        today_draws = [draw for draw in history if draw.get('date') == today]
        
        if today_draws:
            # Return today's card
            last_card_id = today_draws[-1]['card_id']
            return next((card for card in self.cards if card['id'] == last_card_id), None)
        else:
            # Draw new card for today
            return self.draw_card(user_id)
    
    def get_card_by_id(self, card_id: str) -> Dict:
        """Get specific card by ID"""
        return next((card for card in self.cards if card['id'] == card_id), None)
    
    def get_cards_by_category(self, category: str) -> List[Dict]:
        """Get all cards in a specific category"""
        return [card for card in self.cards if card['category'] == category]

# Global card system instance
card_system = InspirationalCardSystem()