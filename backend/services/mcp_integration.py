"""
MCP (Model Context Protocol) Integration for Therapy Agent
Enables AI model to execute tools and access external functionality
"""

import logging
import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
import requests

logger = logging.getLogger(__name__)

class MCPTool:
    """Base class for MCP tools"""
    
    def __init__(self, name: str, description: str, parameters: Dict):
        self.name = name
        self.description = description
        self.parameters = parameters
    
    def execute(self, **kwargs) -> Dict:
        """Execute the tool with given parameters"""
        raise NotImplementedError("Subclasses must implement execute method")

class TherapeuticTools:
    """Therapy-specific MCP tools"""
    
    def __init__(self):
        self.tools = self._initialize_tools()
    
    def _initialize_tools(self) -> Dict[str, MCPTool]:
        """Initialize all available therapy tools"""
        return {
            "analyze_emotion": MCPTool(
                name="analyze_emotion",
                description="Analyze emotional content of text",
                parameters={
                    "text": {"type": "string", "description": "Text to analyze"}
                }
            ),
            "generate_breathing_exercise": MCPTool(
                name="generate_breathing_exercise",
                description="Generate a guided breathing exercise",
                parameters={
                    "duration": {"type": "integer", "description": "Duration in minutes", "default": 5}
                }
            ),
            "suggest_mindfulness_activity": MCPTool(
                name="suggest_mindfulness_activity",
                description="Suggest mindfulness activities based on current state",
                parameters={
                    "current_emotion": {"type": "string", "description": "Current emotional state"},
                    "available_time": {"type": "integer", "description": "Available time in minutes"}
                }
            ),
            "get_inspirational_quote": MCPTool(
                name="get_inspirational_quote",
                description="Get an inspirational quote for motivation",
                parameters={
                    "category": {"type": "string", "description": "Quote category", "default": "general"}
                }
            ),
            "create_coping_strategy": MCPTool(
                name="create_coping_strategy",
                description="Create personalized coping strategies",
                parameters={
                    "situation": {"type": "string", "description": "Stressful situation"},
                    "emotion": {"type": "string", "description": "Current emotion"}
                }
            ),
            "schedule_self_care": MCPTool(
                name="schedule_self_care",
                description="Schedule self-care activities",
                parameters={
                    "activities": {"type": "array", "description": "List of self-care activities"},
                    "timeframe": {"type": "string", "description": "Timeframe for scheduling"}
                }
            )
        }
    
    def get_tools_list(self) -> List[Dict]:
        """Get list of available tools in MCP format"""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
            for tool in self.tools.values()
        ]
    
    def execute_tool(self, tool_name: str, parameters: Dict) -> Dict:
        """Execute a specific tool"""
        if tool_name not in self.tools:
            return {"error": f"Tool {tool_name} not found"}
        
        try:
            tool = self.tools[tool_name]
            
            # Map to actual implementation methods
            if tool_name == "analyze_emotion":
                result = self._analyze_emotion(**parameters)
            elif tool_name == "generate_breathing_exercise":
                result = self._generate_breathing_exercise(**parameters)
            elif tool_name == "suggest_mindfulness_activity":
                result = self._suggest_mindfulness_activity(**parameters)
            elif tool_name == "get_inspirational_quote":
                result = self._get_inspirational_quote(**parameters)
            elif tool_name == "create_coping_strategy":
                result = self._create_coping_strategy(**parameters)
            elif tool_name == "schedule_self_care":
                result = self._schedule_self_care(**parameters)
            else:
                result = {"error": "Tool not implemented"}
            
            return {"success": True, "result": result}
            
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return {"error": str(e)}
    
    def _analyze_emotion(self, text: str) -> Dict:
        """Analyze emotional content"""
        from backend.services.companion_enhancer import companion_enhancer
        
        emotion_scores = companion_enhancer.analyze_user_emotion(text)
        dominant_emotion = companion_enhancer.get_dominant_emotion(emotion_scores)
        
        return {
            "emotion_scores": emotion_scores,
            "dominant_emotion": dominant_emotion,
            "analysis": f"Text appears to express {dominant_emotion} emotions"
        }
    
    def _generate_breathing_exercise(self, duration: int = 5) -> Dict:
        """Generate breathing exercise"""
        exercises = [
            "4-7-8 breathing: Inhale for 4 seconds, hold for 7 seconds, exhale for 8 seconds",
            "Box breathing: Inhale 4s, hold 4s, exhale 4s, hold 4s",
            "Deep belly breathing: Focus on diaphragmatic breathing",
            "Alternate nostril breathing: Traditional pranayama technique"
        ]
        
        return {
            "exercise": random.choice(exercises),
            "duration_minutes": duration,
            "instructions": "Find a comfortable position, close your eyes, and follow the pattern",
            "benefits": "Reduces stress, improves focus, calms nervous system"
        }
    
    def _suggest_mindfulness_activity(self, current_emotion: str, available_time: int) -> Dict:
        """Suggest mindfulness activity"""
        activities = {
            "anxious": [
                "Body scan meditation",
                "Walking meditation",
                "5 senses grounding exercise"
            ],
            "sad": [
                "Loving-kindness meditation",
                "Gratitude journaling",
                "Nature connection walk"
            ],
            "angry": [
                "Vigorous exercise",
                "Progressive muscle relaxation",
                "Mindful writing"
            ],
            "happy": [
                "Mindful celebration",
                "Joyful movement",
                "Sharing gratitude"
            ]
        }
        
        suggested = activities.get(current_emotion, ["Mindful breathing", "Body awareness"])
        
        return {
            "activity": random.choice(suggested),
            "duration_minutes": available_time,
            "suitable_for": current_emotion,
            "instructions": "Focus on present moment awareness without judgment"
        }
    
    def _get_inspirational_quote(self, category: str = "general") -> Dict:
        """Get inspirational quote"""
        quotes = {
            "general": [
                "The only way out is through.",
                "This too shall pass.",
                "You are stronger than you think."
            ],
            "hope": [
                "Even the darkest night will end and the sun will rise.",
                "Hope is being able to see that there is light despite all of the darkness.",
                "New beginnings are often disguised as painful endings."
            ],
            "courage": [
                "Courage doesn't always roar. Sometimes courage is the quiet voice at the end of the day saying, 'I will try again tomorrow.'",
                "You gain strength, courage, and confidence by every experience in which you really stop to look fear in the face.",
                "Being deeply loved by someone gives you strength, while loving someone deeply gives you courage."
            ]
        }
        
        quote_list = quotes.get(category, quotes["general"])
        
        return {
            "quote": random.choice(quote_list),
            "category": category,
            "source": "Inspirational Wisdom"
        }
    
    def _create_coping_strategy(self, situation: str, emotion: str) -> Dict:
        """Create coping strategy"""
        strategies = {
            "anxious": [
                "Practice deep breathing exercises",
                "Use the 5-4-3-2-1 grounding technique",
                "Challenge catastrophic thinking with evidence"
            ],
            "sad": [
                "Reach out to supportive people",
                "Engage in gentle physical activity",
                "Practice self-compassion and acceptance"
            ],
            "angry": [
                "Take a timeout and cool down",
                "Express feelings through writing or art",
                "Use 'I feel' statements to communicate"
            ]
        }
        
        strategy_list = strategies.get(emotion, ["Practice mindfulness", "Seek social support"])
        
        return {
            "situation": situation,
            "emotion": emotion,
            "strategies": strategy_list,
            "recommendation": f"For {situation} when feeling {emotion}, try these strategies"
        }
    
    def _schedule_self_care(self, activities: List[str], timeframe: str) -> Dict:
        """Schedule self-care activities"""
        if not activities:
            activities = ["Meditation", "Exercise", "Journaling", "Nature time", "Creative expression"]
        
        schedule = {}
        for i, activity in enumerate(activities[:5]):  # Limit to 5 activities
            schedule[f"activity_{i+1}"] = {
                "activity": activity,
                "suggested_time": f"{['Morning', 'Afternoon', 'Evening'][i % 3]}",
                "duration": "15-30 minutes"
            }
        
        return {
            "timeframe": timeframe,
            "schedule": schedule,
            "reminder": "Remember to be flexible and kind to yourself"
        }

class MCPClient:
    """MCP client for tool execution"""
    
    def __init__(self):
        self.tools = TherapeuticTools()
    
    def get_available_tools(self) -> List[Dict]:
        """Get list of available tools"""
        return self.tools.get_tools_list()
    
    def process_tool_call(self, tool_call: Dict) -> Dict:
        """Process a tool call from the AI model"""
        try:
            tool_name = tool_call.get("name")
            parameters = tool_call.get("parameters", {})
            
            if not tool_name:
                return {"error": "Tool name required"}
            
            result = self.tools.execute_tool(tool_name, parameters)
            return result
            
        except Exception as e:
            logger.error(f"Tool call processing failed: {e}")
            return {"error": str(e)}
    
    def generate_tool_prompt(self, user_query: str) -> str:
        """Generate prompt for AI model with tool capabilities"""
        tools_list = self.get_available_tools()
        
        prompt = f"""You are a therapeutic AI assistant with access to these tools:

Available Tools:
"""
        
        for tool in tools_list:
            prompt += f"- {tool['name']}: {tool['description']}\n"
            if tool['parameters']:
                prompt += f"  Parameters: {json.dumps(tool['parameters'], indent=2)}\n"
        
        prompt += f"""

User Query: {user_query}

You can use tools to enhance your response. If you need to use a tool, respond with:
{{"tool": "tool_name", "parameters": {{...}}}}

Otherwise, respond normally with therapeutic support.
"""
        
        return prompt

# Global MCP client instance
mcp_client = MCPClient()