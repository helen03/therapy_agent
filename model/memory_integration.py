"""
Memory Integration Module for SATbot
Pure Python implementation of memory management without external dependencies
"""

import os
from typing import Dict, List, Optional, Any
import json
import logging
from datetime import datetime
import re
from collections import defaultdict

# Configure logging
logger = logging.getLogger(__name__)

# In-memory storage for therapeutic conversations
class LocalMemoryStorage:
    """Local in-memory storage for therapeutic conversations"""
    
    def __init__(self):
        self.memories = []  # List of memory dictionaries
        self.user_memories = defaultdict(list)  # user_id -> list of memory indices
        
    def store_memory(self, memory_data: Dict[str, Any]) -> str:
        """Store a memory and return a unique ID"""
        memory_id = f"memory_{len(self.memories)}_{datetime.now().timestamp()}"
        memory_data['memory_id'] = memory_id
        memory_data['created_at'] = datetime.now().isoformat()
        memory_data['updated_at'] = datetime.now().isoformat()
        
        self.memories.append(memory_data)
        
        # Index by user
        if 'user_id' in memory_data:
            self.user_memories[memory_data['user_id']].append(len(self.memories) - 1)
        
        return memory_id
    
    def retrieve_memories(self, user_id: str, query: str = None, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve memories for a user, optionally filtered by query"""
        if user_id not in self.user_memories:
            return []
        
        user_memory_indices = self.user_memories[user_id]
        user_memories = [self.memories[i] for i in user_memory_indices]
        
        if not query:
            return user_memories[:top_k]
        
        # Simple text-based similarity scoring
        scored_memories = []
        query_words = set(re.findall(r'\w+', query.lower()))
        
        for memory in user_memories:
            content = memory.get('content', '') or memory.get('conversation_text', '')
            memory_words = set(re.findall(r'\w+', content.lower()))
            
            # Simple Jaccard similarity
            intersection = query_words.intersection(memory_words)
            union = query_words.union(memory_words)
            similarity = len(intersection) / len(union) if union else 0
            
            scored_memories.append({
                'memory': memory,
                'similarity_score': similarity
            })
        
        # Sort by similarity and return top_k
        scored_memories.sort(key=lambda x: x['similarity_score'], reverse=True)
        return [item for item in scored_memories if item['similarity_score'] > 0.1][:top_k]
    
    def get_user_insights(self, user_id: str) -> Dict[str, Any]:
        """Get therapeutic insights for a user"""
        if user_id not in self.user_memories:
            return {}
        
        user_memories = [self.memories[i] for i in self.user_memories[user_id]]
        
        # Simple pattern analysis
        emotional_patterns = []
        session_count = len(set(m.get('session_id') for m in user_memories if m.get('session_id')))
        
        # Count emotional content patterns
        emotion_keywords = {
            'happy': ['happy', 'joy', 'positive', 'good', 'great', 'wonderful'],
            'sad': ['sad', 'unhappy', 'negative', 'bad', 'difficult', 'hard'],
            'anxious': ['anxious', 'worried', 'nervous', 'scared', 'afraid'],
            'angry': ['angry', 'mad', 'frustrated', 'annoyed', 'upset']
        }
        
        emotion_counts = defaultdict(int)
        for memory in user_memories:
            content = memory.get('content', '') or memory.get('conversation_text', '')
            content_lower = content.lower()
            
            for emotion, keywords in emotion_keywords.items():
                if any(keyword in content_lower for keyword in keywords):
                    emotion_counts[emotion] += 1
        
        return {
            'total_sessions': session_count,
            'total_memories': len(user_memories),
            'emotional_patterns': dict(emotion_counts),
            'recent_activity': len([m for m in user_memories 
                                  if datetime.fromisoformat(m['created_at']).timestamp() > 
                                  (datetime.now().timestamp() - 7 * 24 * 3600)])
        }


class SATbotMemoryManager:
    """Pure Python memory manager for SATbot therapeutic conversations"""
    
    def __init__(self):
        self.enabled = True  # Always enabled for local implementation
        self.storage = LocalMemoryStorage()
        logger.info("Local memory manager initialized")
    
    def store_conversation(self, user_id: str, user_name: str, conversation_text: str, 
                          session_id: str, therapeutic_context: Dict[str, Any]) -> Optional[str]:
        """
        Store therapeutic conversation in local memory
        
        Args:
            user_id: Unique user identifier
            user_name: User's display name
            conversation_text: The therapeutic conversation text
            session_id: Current therapy session ID
            therapeutic_context: Additional context about the therapeutic interaction
            
        Returns:
            Memory ID if successful, None otherwise
        """
        if not self.enabled:
            return None
            
        try:
            # Create memory data structure
            memory_data = {
                'user_id': user_id,
                'user_name': user_name,
                'session_id': session_id,
                'content': conversation_text,
                'context': therapeutic_context,
                'agent_id': 'satbot_therapist',
                'agent_name': 'SATbot Therapist',
                'session_date': datetime.now().isoformat(),
                'type': 'therapeutic_conversation'
            }
            
            # Store in local memory
            memory_id = self.storage.store_memory(memory_data)
            
            logger.info(f"Conversation stored in local memory with ID: {memory_id}")
            return memory_id
            
        except Exception as e:
            logger.error(f"Failed to store conversation in local memory: {e}")
            return None
    
    def retrieve_relevant_memories(self, user_id: str, current_context: str, 
                                  top_k: int = 5, min_similarity: float = 0.3) -> List[Dict[str, Any]]:
        """
        Retrieve relevant past therapeutic memories
        
        Args:
            user_id: Unique user identifier
            current_context: Current therapeutic context or query
            top_k: Number of memories to retrieve
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of relevant memory items with similarity scores
        """
        if not self.enabled:
            return []
            
        try:
            # Search for relevant memories
            relevant_memories = self.storage.retrieve_memories(
                user_id=user_id,
                query=current_context,
                top_k=top_k
            )
            
            # Filter by minimum similarity
            filtered_memories = [
                mem for mem in relevant_memories 
                if mem['similarity_score'] >= min_similarity
            ]
            
            logger.info(f"Retrieved {len(filtered_memories)} relevant memories for user {user_id}")
            return filtered_memories
            
        except Exception as e:
            logger.error(f"Failed to retrieve memories: {e}")
            return []
    
    def get_therapeutic_insights(self, user_id: str) -> Dict[str, Any]:
        """
        Get therapeutic insights from user's memory history
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            Dictionary with therapeutic insights and patterns
        """
        if not self.enabled:
            return {}
            
        try:
            insights = self.storage.get_user_insights(user_id)
            logger.info(f"Generated therapeutic insights for user {user_id}")
            return insights
            
        except Exception as e:
            logger.error(f"Failed to get therapeutic insights: {e}")
            return {}
    
    def enhance_response_with_memory(self, user_id: str, proposed_response: str, 
                                    current_context: str) -> str:
        """
        Enhance SATbot's response with relevant memories
        
        Args:
            user_id: Unique user identifier
            proposed_response: SATbot's original response
            current_context: Current therapeutic context
            
        Returns:
            Enhanced response with memory context
        """
        if not self.enabled:
            return proposed_response
            
        # Retrieve relevant memories
        relevant_memories = self.retrieve_relevant_memories(
            user_id=user_id, 
            current_context=current_context,
            top_k=3,  # Use fewer memories for response enhancement
            min_similarity=0.2  # Lower threshold for therapeutic context
        )
        
        if not relevant_memories:
            return proposed_response
        
        # Create memory-enhanced response
        enhanced_response = proposed_response
        
        # Add memory context if relevant memories found
        memory_contexts = []
        for memory_info in relevant_memories[:2]:  # Use top 2 most relevant memories
            memory = memory_info['memory']
            similarity = memory_info['similarity_score']
            
            if similarity > 0.3:  # Only use reasonably relevant memories
                memory_content = memory.get('content', '')[:150]  # Truncate if too long
                if memory_content:
                    # Extract the actual conversation part (after metadata)
                    if 'Conversation:' in memory_content:
                        conversation_part = memory_content.split('Conversation:', 1)[1].strip()
                        memory_content = conversation_part
                    
                    memory_contexts.append(f"Previously: {memory_content}...")
        
        if memory_contexts:
            # Insert memory context at the beginning of the response
            memory_intro = "I recall from our previous conversations:\n" + "\n".join(memory_contexts)
            enhanced_response = f"{memory_intro}\n\n{proposed_response}"
        
        return enhanced_response


# Global memory manager instance
memory_manager = SATbotMemoryManager()