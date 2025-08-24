# Therapy Agent Model Components

This directory contains the core model components for the therapy agent application. The models are organized in a modular structure to separate concerns and improve maintainability.

## Directory Structure

- `core_models/`: Contains the main model implementations
  - `rule_based_model.py`: Core decision-making engine
  - `llm_integration.py`: Large language model integration
  - `rag_system.py`: Retrieval-Augmented Generation system
  - `classifiers.py`: Text classification tools
  - `companion_enhancer.py`: Emotional intelligence enhancement

## Installation

To use these models, you need to have the dependencies installed. You can install them from the `requirements.txt` file in the `backend` directory:

```bash
pip install -r ../backend/requirements.txt
```

## Usage

These models are primarily designed to be used within the context of the therapy agent backend. To import and use the models:

```python
from model.core_models import ModelDecisionMaker, LLMIntegration

# Initialize the decision maker
model = ModelDecisionMaker()

# Initialize the LLM integration
llm = LLMIntegration(model_type="huggingface")
```

## Note

This directory has been restructured to focus solely on the core model components. The database setup, API endpoints, and other backend services are now located in the `backend` directory.

For detailed information about the project structure and how to run the application, please refer to the main `README.md` file in the project root.
