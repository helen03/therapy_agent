# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SATbot is an empathetic dialogue agent for guiding users through Self-Attachment Technique psychotherapy. It's a web application with a React frontend and Flask backend that provides therapeutic conversation guidance.

**Key Architecture Components:**
- **Flask Backend** (`model/`): Python backend with rule-based decision making and database
- **React Frontend** (`view/`): Chatbot interface using react-chatbot-kit
- **Database**: SQLite with SQLAlchemy ORM for user sessions and choices
- **Rule-based Model**: Therapeutic decision making logic

## Development Commands

### Quick Start Scripts
```bash
# Start both backend and frontend (check scripts first)
bash start_all.sh

# Start backend only
python start_backend.py
```

### Backend Setup & Execution
```bash
# Navigate to model directory
cd model

# Install dependencies
python3 -m pip install -r requirements.txt

# Set environment variables
export FLASK_APP=flask_backend_with_aws.py
export FLASK_DEBUG=1

# Initialize database
flask db init
flask db migrate -m "initial migration"
flask db upgrade

# Run backend server
flask run --eager-loading
# Server runs on http://localhost:5000
```

### Frontend Setup & Execution
```bash
# Navigate to view directory
cd view

# Install dependencies
npm install

# Start development server
npm start
# Frontend runs on http://localhost:3000
```

### Database Management
```bash
# View database schema
sqlite3 app.db .schema

# Query users
sqlite3 app.db "SELECT * FROM user;"

# Query sessions
sqlite3 app.db "SELECT * FROM model_session;"
```

## Key File Locations

- **Backend Entry**: `model/flask_backend_with_aws.py:11` - Flask app creation
- **Main Application**: `model/__init__.py:27` - Flask app factory function
- **Database Models**: `model/models.py:12` - SQLAlchemy ORM models
- **Decision Logic**: `model/rule_based_model.py:15` - Rule-based therapeutic model with 26+ exercises
- **Memory Integration**: `model/memory_integration.py` - Memory management system
- **LLM Integration**: `model/llm_integration.py` - Large language model integration
- **RAG System**: `model/rag_system.py` - Psychology document retrieval and processing
- **TTS Service**: `model/tts_service.py` - Text-to-speech with emotional tone
- **Companion Enhancer**: `model/companion_enhancer.py` - AI emotional intelligence
- **Inspirational Cards**: `model/inspirational_cards.py` - Healing message card system
- **Classifiers**: `model/classifiers.py` - Text classification utilities
- **Frontend Config**: `view/src/config.js:24` - Chatbot configuration
- **Frontend App**: `view/src/App.js:8` - Main React component
- **Message Parser**: `view/src/MessageParser.js` - Handles user messages
- **Action Provider**: `view/src/ActionProvider.js` - Handles bot responses

## Environment Configuration

Required environment variables (set in `model/.env`):
```bash
DATABASE_URL="sqlite:////absolute/path/to/satbot-master/model/app.db"
FLASK_APP=flask_backend_with_aws.py
FLASK_DEBUG=1
```

## API Endpoints

Key endpoints (see `model/__init__.py`):
- `POST /api/login` - User authentication and session creation
- `POST /api/update_session` - Process user choices and get next therapeutic step
- `POST /api/upload_document` - Upload psychology documents for RAG system
- `POST /api/generate_speech` - Generate speech from therapeutic text
- `GET /api/user_insights` - Get emotional insights and patterns
- `GET /api/daily_checkin` - Get personalized daily check-in messages
- `GET /api/draw_card` - Draw inspirational healing card
- `GET /api/daily_card` - Get user's daily card
- `GET /api/card_history` - Get card draw history

## Database Schema

Main tables:
- `user` - User accounts and credentials
- `model_session` - Therapy sessions
- `choice` - User choices during sessions
- `protocol` - Therapeutic protocols selected
- `model_run` - Model execution runs

## Therapeutic Framework

The system uses 26+ therapeutic exercises (see `model/rule_based_model.py:21`):
- Exercise 1: Recalling childhood memories
- Exercise 2: Embracing and comforting the Child
- Exercise 3: Singing a song of affection
- ... up to Exercise 26: Discovering your true self

## Frontend Widgets

Custom React components in `view/src/widgets/options/GeneralOptions/`:
- `YesNoOptions.jsx` - Yes/No decision points
- `ProtocolOptions.jsx` - Protocol selection
- `ContinueOptions.jsx` - Continue/stop options
- `EmotionOptions.jsx` - Emotion selection
- `FeedbackOptions.jsx` - Feedback collection
- `EventOptions.jsx` - Recent/distant event selection

## Model Files Required

**Note**: The project requires two external model files:
1. Download from: https://drive.google.com/file/d/1cycrYd0S3Go7j3W2A50bJKQBn-oCdgZs/view
2. Download from: https://drive.google.com/file/d/1HGmTFL-P4cXIInszLM3QjnuCVLj6zz7C/view
3. Place both in the `model/` directory

## Testing & Development

### Backend Testing
```bash
# Navigate to model directory
cd model

# Run integration tests
python test_run.py              # Basic app startup test
python test_add_data.py         # Database population test
python test_add_data_flask.py   # Flask-specific data test
python test_integration_simple.py  # Simple integration test
python test_final_integration.py   # Comprehensive integration test
python test_memory_integration.py  # Memory system test
python test_satbot_memory.py      # SATbot memory functionality test

# Test database connection
python -c "from model.models import db; print('DB connected')"
```

### Frontend Testing
```bash
# Navigate to view directory
cd view

# Run React tests
npm test

# Build for production
npm run build
```

## Code Style & Standards

- **Python**: PEP 8, Flask conventions, SQLAlchemy patterns
- **JavaScript**: React best practices, ES6+ syntax
- **Database**: SQLAlchemy ORM with proper migrations
- **Frontend**: React components with proper state management

## Common Development Tasks

1. **Adding new therapeutic exercises**: Update `EXERCISE_TITLES` in `rule_based_model.py:21`
2. **Modifying decision logic**: Update `ModelDecisionMaker` class methods
3. **Adding database fields**: Create new migration with `flask db migrate`
4. **Extending frontend widgets**: Add new components in `widgets/options/`
5. **API endpoint changes**: Modify routes in `__init__.py`

## Troubleshooting

### Common Issues

1. **Database connection errors**:
   - Check `DATABASE_URL` in `.env` file
   - Ensure `app.db` file exists and is writable

2. **Model file missing errors**:
   - Download required model files from Google Drive links
   - Place in `model/` directory

3. **CORS issues**:
   - Backend configured with `CORS(app, resources={r"/*": {"origins": "*"}})`
   - Ensure frontend and backend ports match (3000 vs 5000)

4. **React build issues**:
   - Clear node_modules: `rm -rf node_modules && npm install`
   - Check React version compatibility

### Debug Mode

Enable debug logging:
```bash
export FLASK_DEBUG=1
flask run --eager-loading
```

Check backend logs for detailed error information and decision flow.

## Deployment Considerations

- For production, use Gunicorn instead of Flask development server
- Set `FLASK_DEBUG=0` in production
- Use proper database (PostgreSQL/MySQL) instead of SQLite for production
- Configure proper CORS origins for security
- Set up HTTPS for production deployment