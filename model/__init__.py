# Model Package
# This package contains the core models for the therapy agent

# Import the backend application factory
from backend import create_app

# Import core models
from .core_models import ModelDecisionMaker, LLMIntegration, DocumentProcessor, VectorStore, RAGSystem, CompanionEnhancer

# Legacy imports (for backward compatibility)
def get_llm_integration():
    """Legacy function to get LLM integration"""
    return LLMIntegration()

# Database models are now in the backend directory
# from backend.database.models import User, UserModelSession, Choice, Protocol

# Memory integration is now in the backend directory
# from backend.services.memory_integration import memory_manager

# API endpoints are now in the backend directory
# For detailed API documentation, please refer to the backend directory
