import os
import logging
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import openai
import time

# 设置日志\logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMIntegration:
    """大语言模型集成模块，用于处理情感分析和文本生成任务"""
    
    def __init__(self, model_type="huggingface", model_name="gpt2", api_key=None):
        """
        初始化LLM集成模块
        
        Args:
            model_type: 模型类型，可以是"huggingface"或"openai"
            model_name: 模型名称
            api_key: API密钥（如果使用OpenAI）
        """
        self.model_type = model_type
        self.model_name = model_name
        self.api_key = api_key
        self.model = None
        self.tokenizer = None
        self.emotion_analyzer = None
        
        # 尝试初始化模型
        try:
            self._initialize_model()
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {str(e)}")
            self._initialize_fallback()
    
    def _initialize_model(self):
        """根据配置初始化模型"""
        if self.model_type == "huggingface":
            # 使用Hugging Face的本地模型
            if self.model_name == "gpt2":
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            else:
                # 使用更高级的Hugging Face模型
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float16,
                    low_cpu_mem_usage=True,
                    device_map="auto"
                )
            
            # 初始化情感分析pipeline
            self.emotion_analyzer = pipeline(
                "text-classification",
                model="SamLowe/roberta-base-go_emotions",
                top_k=None
            )
        
        elif self.model_type == "openai":
            # 配置OpenAI API
            if self.api_key:
                openai.api_key = self.api_key
            else:
                openai.api_key = os.getenv("OPENAI_API_KEY")
            
            if not openai.api_key:
                raise ValueError("OpenAI API key is required for OpenAI model type")
        
        logger.info(f"Successfully initialized {self.model_type} model: {self.model_name}")
    
    def _initialize_fallback(self):
        """初始化回退模型（当无法加载主模型时使用）"""
        logger.warning("Using fallback model")
        # 使用简单的文本分类pipeline作为回退
        try:
            self.emotion_analyzer = pipeline(
                "text-classification",
                model="SamLowe/roberta-base-go_emotions",
                top_k=None
            )
        except:
            # 如果连回退模型都无法加载，则设置为None
            self.emotion_analyzer = None
    
    def analyze_emotion(self, text, model_type="emo"):
        """
        分析文本中的情感
        
        Args:
            text: 要分析的文本
            model_type: 分析类型，可以是"emo"（情感）或其他
        
        Returns:
            分析结果（情感标签）
        """
        # 预处理文本
        text = text.strip().lower()
        if not text:
            return "neutral"
        
        try:
            if self.model_type == "openai":
                # 使用OpenAI API进行情感分析
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an emotion analysis assistant. Please classify the user's emotion as one of: happy, sad, angry, anxious, jealous, guilty, ashamed, envious, disgusted, disappointed, loving, insecure, neutral."},
                        {"role": "user", "content": text}
                    ],
                    max_tokens=10,
                    temperature=0
                )
                emotion = response.choices[0].message.content.strip().lower()
                return emotion
            
            elif self.emotion_analyzer:
                # 使用Hugging Face的情感分析pipeline
                results = self.emotion_analyzer(text)
                # 转换为我们系统所需的情感标签
                emotion_map = {
                    "sadness": "sad",
                    "fear": "anxious",
                    "anger": "angry",
                    "joy": "happy",
                    "love": "loving",
                    "surprise": "happy",
                    "gratitude": "happy",
                    "pride": "happy",
                    "optimism": "happy",
                    "excitement": "happy",
                    "disappointment": "disappointed",
                    "disgust": "disgusted",
                    "grief": "sad",
                    "embarrassment": "ashamed",
                    "remorse": "guilty",
                    "desire": "happy",
                    "admiration": "happy",
                    "curiosity": "happy"
                }
                
                # 获取最高置信度的情感
                top_emotion = max(results[0], key=lambda x: x['score'])['label']
                return emotion_map.get(top_emotion, "neutral")
            
            else:
                # 如果没有可用的情感分析器，返回中性
                return "neutral"
        except Exception as e:
            logger.error(f"Emotion analysis failed: {str(e)}")
            return "neutral"
    
    def generate_response(self, prompt, max_length=200, temperature=0.7):
        """
        生成文本响应
        
        Args:
            prompt: 提示文本
            max_length: 最大生成长度
            temperature: 生成温度（控制随机性）
        
        Returns:
            生成的响应文本
        """
        try:
            if self.model_type == "openai":
                # 使用OpenAI API生成响应
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_length,
                    temperature=temperature
                )
                return response.choices[0].message.content.strip()
            
            elif self.model:
                # 使用Hugging Face模型生成响应
                inputs = self.tokenizer(prompt, return_tensors="pt")
                
                # 确保在正确的设备上运行
                if torch.cuda.is_available():
                    inputs = {k: v.cuda() for k, v in inputs.items()}
                
                # 生成响应
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
                
                # 解码并返回响应
                return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            else:
                # 如果没有可用的模型，返回默认响应
                return "I'm here to help you. Please tell me more about how you're feeling."
        except Exception as e:
            logger.error(f"Response generation failed: {str(e)}")
            return "I'm sorry, I'm having trouble responding right now. Please try again later."
    
    def enhance_with_context(self, user_id, current_prompt, conversation_history=None):
        """
        使用用户历史、上下文和RAG增强提示
        
        Args:
            user_id: 用户ID
            current_prompt: 当前提示
            conversation_history: 对话历史
        
        Returns:
            增强后的提示
        """
        # Get conversation history context
        history_context = ""
        if conversation_history:
            history_context = "\n".join([f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}" for msg in conversation_history[-3:]])
        
        # Get RAG context from psychology documents
        rag_context = ""
        try:
            from backend.models.rag_system import rag_system
            rag_context = rag_system.enhance_prompt_with_context(current_prompt, user_id)
        except Exception as e:
            logger.error(f"RAG context enhancement failed: {e}")
        
        # Combine all contexts
        if history_context and rag_context:
            enhanced_prompt = f"""Conversation History:
{history_context}

Psychology Knowledge Context:
{rag_context}

Please respond to the user's current message: {current_prompt}

Respond as an empathetic therapeutic AI companion."""
        elif history_context:
            enhanced_prompt = f"Here's the conversation history:\n{history_context}\n\nBased on this, respond to: {current_prompt}"
        elif rag_context:
            enhanced_prompt = rag_context
        else:
            enhanced_prompt = current_prompt
        
        return enhanced_prompt
    
    def analyze_intention(self, text):
        """
        分析文本中的意图（特别是自杀意图）
        
        Args:
            text: 要分析的文本
        
        Returns:
            's' 表示有自杀意图，'not_s' 表示没有自杀意图
        """
        # 预处理文本
        text = text.strip().lower()
        if not text:
            return "not_s"
        
        try:
            if self.model_type == "openai":
                # 使用OpenAI API进行意图分析
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a mental health assistant. Analyze the user's text to determine if they are expressing suicidal intent. Respond with 's' if there is suicidal intent, 'not_s' if there is no suicidal intent."},
                        {"role": "user", "content": text}
                    ],
                    max_tokens=10,
                    temperature=0
                )
                result = response.choices[0].message.content.strip().lower()
                return "s" if result == "s" else "not_s"
            
            else:
                # 使用关键词匹配作为回退方法
                # 这只是一个简单的实现，实际应用中应该使用更复杂的模型
                suicidal_keywords = [
                    "suicide", "kill myself", "end my life", "want to die", 
                    "not worth living", "better off dead", "no reason to live"
                ]
                
                for keyword in suicidal_keywords:
                    if keyword in text:
                        return "s"
                
                return "not_s"
        except Exception as e:
            logger.error(f"Intention analysis failed: {str(e)}")
            return "not_s"
    
    def get_semantic_similarity(self, text1, text2):
        """
        计算两个文本之间的语义相似度
        
        Args:
            text1: 第一个文本
            text2: 第二个文本
        
        Returns:
            相似度分数（0-1之间）
        """
        try:
            if self.model_type == "openai":
                # 使用OpenAI API计算语义相似度
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a semantic similarity assistant. Rate the semantic similarity between the two texts on a scale of 0 to 1, where 0 means completely dissimilar and 1 means identical. Respond with only the numerical value."},
                        {"role": "user", "content": f"Text 1: {text1}\nText 2: {text2}"}
                    ],
                    max_tokens=10,
                    temperature=0
                )
                try:
                    similarity = float(response.choices[0].message.content.strip())
                    # 确保返回值在0-1之间
                    return max(0.0, min(1.0, similarity))
                except ValueError:
                    logger.error("Failed to parse similarity score from OpenAI response")
                    return 0.5  # 回退到中性值
            
            else:
                # 使用简单的文本相似度计算作为回退
                # 这只是一个简单的实现，实际应用中应该使用更复杂的模型
                # 例如，可以使用Sentence-BERT或其他专门的语义相似度模型
                import difflib
                return difflib.SequenceMatcher(None, text1, text2).ratio()
        except Exception as e:
            logger.error(f"Semantic similarity calculation failed: {str(e)}")
            return 0.5  # 回退到中性值

# 创建LLM集成实例
def get_llm_integration():
    """获取LLM集成实例的工厂函数"""
    # 从环境变量获取配置
    model_type = os.getenv("LLM_MODEL_TYPE", "huggingface")
    model_name = os.getenv("LLM_MODEL_NAME", "gpt2")
    api_key = os.getenv("OPENAI_API_KEY")
    
    return LLMIntegration(
        model_type=model_type,
        model_name=model_name,
        api_key=api_key
    )

# 全局LLM实例，懒加载
_llm_instance = None

def get_llm():
    """获取全局LLM实例"""
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = get_llm_integration()
    return _llm_instance