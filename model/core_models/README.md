# Core Models for Therapy Agent

This directory contains the core models and algorithms used by the therapy agent. These models are designed to handle emotional analysis, decision making, and provide therapeutic responses.

## Contents

- `rule_based_model.py`: Core decision-making engine that suggests therapeutic exercises based on user input
- `llm_integration.py`: Integration with large language models for advanced text processing and generation
- `rag_system.py`: Retrieval-Augmented Generation system for psychology documents
- `classifiers.py`: Text classification tools for emotion and intent detection
- `companion_enhancer.py`: Enhances AI companionship with emotional intelligence and personalization

## Usage

To use these models in your application:

```python
from model.core_models import ModelDecisionMaker, LLMIntegration, DocumentProcessor

# Initialize the decision maker
model = ModelDecisionMaker()

# Initialize the LLM integration
llm = LLMIntegration(model_type="huggingface")

# Analyze emotion using the LLM integration
emotion_result = llm.analyze_emotion("I'm feeling very sad today")
```

## Note

These models are optimized for use within the therapy agent ecosystem. They are designed to work with the database models and services provided in the `backend` directory.