"""
Text-to-Speech Service for AI Therapy Companion
Provides voice output for therapeutic responses
"""

import os
import logging
import tempfile
from typing import Optional
import io
from gtts import gTTS
import pygame
import threading

logger = logging.getLogger(__name__)

class TTSService:
    """Text-to-Speech service using Google Text-to-Speech"""
    
    def __init__(self):
        self.enabled = True
        self.currently_playing = False
        self.pygame_initialized = False
        self._init_pygame()
    
    def _init_pygame(self) -> None:
        """Initialize pygame for audio playback"""
        try:
            pygame.mixer.init()
            self.pygame_initialized = True
            logger.info("Pygame mixer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize pygame mixer: {e}")
            self.pygame_initialized = False
    
    def text_to_speech(self, text: str, lang: str = 'en', 
                      slow: bool = False, emotional_tone: str = 'calm') -> Optional[str]:
        """Convert text to speech and return audio file path"""
        if not self.enabled or not text.strip():
            return None
        
        try:
            # Adjust speaking rate based on emotional tone
            if emotional_tone == 'calm':
                slow = True
            elif emotional_tone == 'excited':
                slow = False
            
            # Create TTS object
            tts = gTTS(text=text, lang=lang, slow=slow)
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tts.save(temp_file.name)
            
            logger.info(f"TTS audio saved to: {temp_file.name}")
            return temp_file.name
            
        except Exception as e:
            logger.error(f"TTS conversion failed: {e}")
            return None
    
    def play_audio(self, audio_file: str) -> bool:
        """Play audio file using pygame"""
        if not self.pygame_initialized or not os.path.exists(audio_file):
            return False
        
        try:
            self.currently_playing = True
            
            # Load and play audio
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            self.currently_playing = False
            
            # Clean up temporary file
            try:
                os.unlink(audio_file)
            except:
                pass
            
            return True
            
        except Exception as e:
            logger.error(f"Audio playback failed: {e}")
            self.currently_playing = False
            return False
    
    def speak_async(self, text: str, lang: str = 'en', 
                   emotional_tone: str = 'calm') -> None:
        """Convert text to speech and play asynchronously"""
        def _speak_thread():
            audio_file = self.text_to_speech(text, lang, emotional_tone=emotional_tone)
            if audio_file:
                self.play_audio(audio_file)
        
        # Start in background thread
        thread = threading.Thread(target=_speak_thread)
        thread.daemon = True
        thread.start()
    
    def analyze_emotional_tone(self, text: str) -> str:
        """Analyze text to determine appropriate emotional tone for TTS"""
        text_lower = text.lower()
        
        # Emotional tone detection
        if any(word in text_lower for word in ['sad', 'depressed', 'unhappy', 'crying', 'tears']):
            return 'gentle'
        elif any(word in text_lower for word in ['excited', 'happy', 'joy', 'great', 'wonderful']):
            return 'excited'
        elif any(word in text_lower for word in ['angry', 'mad', 'frustrated', 'upset']):
            return 'calm'  # Stay calm with angry users
        elif any(word in text_lower for word in ['anxious', 'nervous', 'worried', 'scared']):
            return 'reassuring'
        else:
            return 'calm'
    
    def generate_therapeutic_voice_response(self, therapeutic_text: str, 
                                          user_emotion: str = None) -> Optional[str]:
        """Generate voice response with therapeutic tone adjustment"""
        if not therapeutic_text.strip():
            return None
        
        # Determine emotional tone based on user emotion or text content
        if user_emotion:
            tone_map = {
                'sad': 'gentle',
                'happy': 'warm',
                'angry': 'calm',
                'anxious': 'reassuring',
                'neutral': 'calm'
            }
            emotional_tone = tone_map.get(user_emotion, 'calm')
        else:
            emotional_tone = self.analyze_emotional_tone(therapeutic_text)
        
        return self.text_to_speech(therapeutic_text, emotional_tone=emotional_tone)

# Global TTS instance
tts_service = TTSService()