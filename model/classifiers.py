import numpy as np
import os
import pandas as pd
import re
import time
from datetime import datetime
import copy
import joblib
import random

# Import the LLM integration
from .llm_integration import get_llm_integration

# Define the emotions
emotions = ['fear', 'love', 'instability', 'disgust', 'disappointment',
          'shame', 'anger', 'jealous', 'sadness', 'envy', 'joy', 'guilt']

# Define label to int mapping
label2int = {
    'not_s': 0,
    's': 1
}

class ClassificationModel:
    def __init__(self, app=None):
        # Initialise empty models
        self.llm_integration = None
        self.app = app
        # Load the LLM integration
        self.load_models()
    
    def load_models(self):
        try:
            # Load the LLM integration
            self.llm_integration = get_llm_integration()
            print("LLM integration loaded successfully")
        except Exception as e:
            # If LLM integration cannot be loaded, print error and use fallback
            print(f"LLM integration could not be loaded, using fallback: {str(e)}")
    
    def get_classification(self, text, model_type):
        # If LLM integration is not loaded, use fallback
        if self.llm_integration is None:
            if model_type == "emo":
                return random.choice(emotions)
            else:
                return "not_s"
        
        # Use LLM integration for classification
        try:
            if model_type == "emo":
                # Use LLM for emotion classification
                return self.llm_integration.analyze_emotion(text)
            else:
                # Use LLM for 's' classification (suicidal intent)
                return self.llm_integration.analyze_intention(text)
        except Exception as e:
            print(f"Error during LLM classification: {str(e)}")
            # Fallback to random choice if LLM classification fails
            if model_type == "emo":
                return random.choice(emotions)
            else:
                return "not_s"
    
    def get_distance(self, text1, text2):
        # If LLM integration is not loaded, use random distance
        if self.llm_integration is None:
            return np.random.uniform(0, 1)
        
        # Use LLM integration for distance calculation
        try:
            return self.llm_integration.get_semantic_similarity(text1, text2)
        except Exception as e:
            print(f"Error during LLM distance calculation: {str(e)}")
            # Fallback to random distance if LLM calculation fails
            return np.random.uniform(0, 1)

# Create a global instance of the model
model = ClassificationModel()

# Define helper functions to use the model
def get_classification(text, model_type):
    return model.get_classification(text, model_type)

def get_sentence_score(sentence, dataframe):
    # This function is used to score sentences based on how well they fit with previous questions
    # It's a placeholder function that always returns 0
    return 0
