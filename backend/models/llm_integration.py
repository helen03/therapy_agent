import os
import logging
import requests
import json
import time
from typing import Dict, Any, Optional

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMIntegration:
    """大语言模型集成模块，使用API调用代替本地模型"""
    
    def __init__(self, api_type="openai", api_key=None, api_base=None):
        """
        初始化LLM集成模块
        
        Args:
            api_type: API类型，可以是"openai"、"azure"或"custom"
            api_key: API密钥
            api_base: API基础URL（用于自定义API）
        """
        self.api_type = api_type
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.api_base = api_base or os.getenv("API_BASE_URL")
        
        # 设置默认API端点
        if self.api_type == "openai" and not self.api_base:
            self.api_base = "https://api.deepseek.com/v1"
        elif self.api_type == "azure" and not self.api_base:
            self.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
    
    def _call_api(self, endpoint: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """通用API调用方法"""
        try:
            # 检查API密钥是否有效
            if not self.api_key:
                logger.warning("Missing API key, using fallback mode")
                return None
                
            headers = {
                "Content-Type": "application/json",
            }
            
            if self.api_type == "openai":
                # DeepSeek API需要特殊处理
                if "deepseek" in self.api_base:
                    # DeepSeek使用不同的身份验证格式
                    headers["Authorization"] = f"Bearer {self.api_key}"
                    # DeepSeek使用不同的模型名称
                    if "model" in payload:
                        if payload["model"] == "gpt-3.5-turbo":
                            payload["model"] = "deepseek-chat"
                        elif payload["model"] == "text-embedding-ada-002":
                            payload["model"] = "deepseek-embed"
                else:
                    # 标准OpenAI API
                    headers["Authorization"] = f"Bearer {self.api_key}"
            elif self.api_type == "azure":
                headers["api-key"] = self.api_key
            
            url = f"{self.api_base}{endpoint}"
            
            # 减少日志信息，避免日志过多
            logger.debug(f"API Call: {url}")
            logger.debug(f"Payload model: {payload.get('model')}")
            
            # 设置合理的超时时间
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=10  # 10秒超时
            )
            
            if response.status_code == 200:
                result = response.json()
                # 验证响应格式
                if isinstance(result, dict):
                    return result
                else:
                    logger.error(f"Invalid response format: {type(result)}")
                    return None
            else:
                logger.error(f"API call failed: {response.status_code} - {response.text}")
                # 如果是认证错误，立即返回None使用回退
                if response.status_code in [401, 403]:
                    logger.warning("Authentication failed, using fallback mode")
                    return None
                # 如果是配额错误，也使用回退
                if response.status_code == 429:
                    logger.warning("Rate limit exceeded, using fallback mode")
                    return None
                return None
                
        except requests.exceptions.Timeout:
            logger.error("API call timeout")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"API request error: {e}")
            return None
        except Exception as e:
            logger.error(f"API call error: {e}")
            return None
    
    def analyze_emotion(self, text: str) -> str:
        """
        分析文本中的情感
        
        Args:
            text: 要分析的文本
        
        Returns:
            分析结果（情感标签）
        """
        if not text or not text.strip():
            return "neutral"
        
        text = text.strip().lower()
        
        try:
            if self.api_type in ["openai", "azure"]:
                # 使用OpenAI API进行情感分析
                payload = {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "system", 
                            "content": "你是一个情感分析助手。请将用户的情感分类为：happy, sad, angry, anxious, neutral。只返回情感标签，不要其他内容。"
                        },
                        {
                            "role": "user", 
                            "content": text
                        }
                    ],
                    "max_tokens": 10,
                    "temperature": 0
                }
                
                result = self._call_api("/chat/completions", payload)
                if result and "choices" in result and len(result["choices"]) > 0:
                    emotion = result["choices"][0]["message"]["content"].strip().lower()
                    # 确保返回标准的情感标签
                    valid_emotions = ["happy", "sad", "angry", "anxious", "neutral"]
                    return emotion if emotion in valid_emotions else "neutral"
                else:
                    logger.warning("No valid emotion analysis result from API")
            
            # 回退到关键词匹配
            emotion_keywords = {
                "happy": ["开心", "高兴", "快乐", "幸福", "愉快", "开心"],
                "sad": ["伤心", "难过", "悲伤", "沮丧", "失望", "伤心"],
                "angry": ["生气", "愤怒", "恼火", "烦躁", "不满", "生气"],
                "anxious": ["焦虑", "紧张", "担心", "不安", "压力", "焦虑"]
            }
            
            for emotion, keywords in emotion_keywords.items():
                if any(keyword in text for keyword in keywords):
                    return emotion
            
            return "neutral"
            
        except Exception as e:
            logger.error(f"Emotion analysis failed: {e}")
            return "neutral"
    
    def generate_response(self, prompt: str, max_length: int = 300, temperature: float = 0.7) -> str:
        """
        生成文本响应
        
        Args:
            prompt: 提示文本
            max_length: 最大生成长度
            temperature: 生成温度
        
        Returns:
            生成的响应文本
        """
        try:
            if self.api_type in ["openai", "azure"]:
                # 使用OpenAI API生成响应
                payload = {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "system",
                            "content": "你是一个富有同理心的治疗型AI助手，专门提供心理健康支持。用中文回答，保持温暖、支持性和专业性。"
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    "max_tokens": max_length,
                    "temperature": temperature
                }
                
                result = self._call_api("/chat/completions", payload)
                if result and "choices" in result and len(result["choices"]) > 0:
                    content = result["choices"][0]["message"]["content"]
                    if content and isinstance(content, str):
                        return content.strip()
                    else:
                        logger.warning("Invalid content format in API response")
                else:
                    logger.warning("No valid choices in API response")
            
            # 回退响应
            fallback_responses = [
                "我在这里为您提供支持。请告诉我更多关于您的感受。",
                "感谢您的消息。我理解这可能不容易，我会尽力帮助您。",
                "我在这里倾听您。请随时分享您的想法和感受。"
            ]
            
            import random
            return random.choice(fallback_responses)
            
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return "抱歉，我暂时无法处理您的请求。请稍后再试。"
    
    def analyze_intention(self, text: str) -> str:
        """
        分析文本中的意图（特别是自杀意图）
        
        Args:
            text: 要分析的文本
        
        Returns:
            's' 表示有自杀意图，'not_s' 表示没有自杀意图
        """
        if not text or not text.strip():
            return "not_s"
        
        text = text.strip().lower()
        
        try:
            if self.api_type in ["openai", "azure"]:
                payload = {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "system", 
                            "content": "你是心理健康助手。分析用户文本是否表达自杀意图。只返回's'或'not_s'，不要其他内容。"
                        },
                        {
                            "role": "user", 
                            "content": text
                        }
                    ],
                    "max_tokens": 5,
                    "temperature": 0
                }
                
                result = self._call_api("/chat/completions", payload)
                if result and "choices" in result and len(result["choices"]) > 0:
                    intention = result["choices"][0]["message"]["content"].strip().lower()
                    return "s" if intention == "s" else "not_s"
                else:
                    logger.warning("No valid intention analysis result from API")
            
            # 关键词匹配回退
            suicidal_keywords = [
                "自杀", "不想活了", "结束生命", "离开这个世界", 
                "活着没意思", "撑不下去了", "想死", "自残", "伤害自己"
            ]
            
            for keyword in suicidal_keywords:
                if keyword in text:
                    return "s"
            
            return "not_s"
            
        except Exception as e:
            logger.error(f"Intention analysis failed: {e}")
            return "not_s"
    
    def get_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        计算两个文本之间的语义相似度
        
        Args:
            text1: 第一个文本
            text2: 第二个文本
        
        Returns:
            相似度分数（0-1之间）
        """
        try:
            if self.api_type in ["openai", "azure"]:
                payload = {
                    "model": "text-embedding-ada-002",
                    "input": [text1, text2]
                }
                
                result = self._call_api("/embeddings", payload)
                if result and "data" in result:
                    import numpy as np
                    from numpy.linalg import norm
                    
                    # 计算余弦相似度
                    emb1 = np.array(result["data"][0]["embedding"])
                    emb2 = np.array(result["data"][1]["embedding"])
                    
                    similarity = np.dot(emb1, emb2) / (norm(emb1) * norm(emb2))
                    return float(similarity)
            
            # 简单的文本相似度回退
            import difflib
            return difflib.SequenceMatcher(None, text1, text2).ratio()
            
        except Exception as e:
            logger.error(f"Semantic similarity calculation failed: {e}")
            return 0.5
        
# 创建LLM集成实例
def get_llm_integration():
    """获取LLM集成实例的工厂函数"""
    # 从环境变量获取配置
    api_type = os.getenv("LLM_API_TYPE", "openai")
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("API_BASE_URL")
    
    return LLMIntegration(
        api_type=api_type,
        api_key=api_key,
        api_base=api_base
    )

class MockLLM:
    """模拟LLM类，用于API不可用时的回退"""
    
    def __init__(self):
        self.api_type = "mock"
        self.api_base = "mock://localhost"
    
    def analyze_emotion(self, text: str) -> str:
        """模拟情感分析"""
        text = text.strip().lower()
        if not text:
            return "neutral"
        
        emotion_keywords = {
            "happy": ["开心", "高兴", "快乐", "幸福", "愉快"],
            "sad": ["伤心", "难过", "悲伤", "沮丧", "失望"],
            "angry": ["生气", "愤怒", "恼火", "烦躁", "不满"],
            "anxious": ["焦虑", "紧张", "担心", "不安", "压力"]
        }
        
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text for keyword in keywords):
                return emotion
        
        return "neutral"
    
    def generate_response(self, prompt: str, max_length: int = 300, temperature: float = 0.7) -> str:
        """模拟响应生成"""
        fallback_responses = [
            "我在这里为您提供支持。请告诉我更多关于您的感受。",
            "感谢您的消息。我理解这可能不容易，我会尽力帮助您。",
            "我在这里倾听您。请随时分享您的想法和感受。"
        ]
        
        import random
        return random.choice(fallback_responses)
    
    def analyze_intention(self, text: str) -> str:
        """模拟意图分析"""
        text = text.strip().lower()
        if not text:
            return "not_s"
        
        suicidal_keywords = [
            "自杀", "不想活了", "结束生命", "离开这个世界", 
            "活着没意思", "撑不下去了", "想死"
        ]
        
        for keyword in suicidal_keywords:
            if keyword in text:
                return "s"
        
        return "not_s"
    
    def get_semantic_similarity(self, text1: str, text2: str) -> float:
        """模拟语义相似度"""
        import difflib
        return difflib.SequenceMatcher(None, text1, text2).ratio()

# 全局LLM实例，懒加载
_llm_instance = None

def get_llm():
    """获取全局LLM实例"""
    global _llm_instance
    if _llm_instance is None:
        print("Initializing LLM instance...")
        try:
            # 配置LLM参数
            # 这里应该有从环境变量或配置文件读取API密钥和其他参数的代码
            # 由于没有具体的LLM提供商信息，我们先使用一个通用的实现
            _llm_instance = get_llm_integration()
            print("LLM instance initialized successfully!")
        except Exception as e:
            print(f"Failed to initialize LLM instance: {e}")
            # 在实际应用中，这里可能会设置一个回退机制或使用模拟的LLM响应
            # 为了演示，我们创建一个简单的模拟LLM实例
            _llm_instance = MockLLM()
    return _llm_instance

