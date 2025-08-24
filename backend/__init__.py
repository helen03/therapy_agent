from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from backend.utils.config import Config
import json
from flask import Flask, request
from flask_cors import CORS
import os
import logging
import datetime
from dotenv import load_dotenv

# Memory integration
from backend.services.memory_integration import memory_manager

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"), override=True)


# For dev logging - comment out for Gunicorn
# Configure logging to both console and file
logging.basicConfig(
    level=logging.INFO,
    format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
    handlers=[
        logging.FileHandler('/Users/liuyanjun/therapy_agent/logs/backend.log'),
        logging.StreamHandler()
    ]
)

# Initialize logger
logger = logging.getLogger(__name__)

# ~ Databases ~ #
db = SQLAlchemy()  # <-Initialize database object
migrate = Migrate()  # <-Initialize migration object


def create_app():
    """Construct core application"""
    app = Flask(__name__)

    # For Gunicorn logging
    # gunicorn_logger = logging.getLogger('gunicorn.error')
    # app.logger.handlers = gunicorn_logger.handlers
    # app.logger.setLevel(gunicorn_logger.level)

    ###
    # NOTE: to print in Flask, do `app.logger.info(var_to_print)`
    ###

    # Pull from config file
    app.config.from_object(Config)
    db.init_app(app)  # <- This will get called in our models.py file
    migrate.init_app(app, db)  # <- Migration directory

    CORS(app, resources={r"/*": {"origins": "*"}})

    from backend.database import models  # noqa
    from backend.database.models import User, UserModelSession  # noqa

    # @app.route('/')
    # def home():
    #     return "ok"

    @app.route("/api/register", methods=["POST"])
    def register():
        """User registration endpoint with password hashing"""
        try:
            user_info = json.loads(request.data)["user_info"]
            username = user_info["username"]
            password = user_info["password"]
            email = user_info.get("email", "")
            
            # Validate input
            if not username or not password:
                return {"success": False, "error": "Username and password are required"}, 400
            
            if len(password) < 6:
                return {"success": False, "error": "Password must be at least 6 characters"}, 400
            
            # Check if username already exists
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return {"success": False, "error": "Username already exists"}, 400
            
            # Check if email already exists (if provided)
            if email:
                existing_email = User.query.filter_by(email=email).first()
                if existing_email:
                    return {"success": False, "error": "Email already exists"}, 400
            
            # Create new user with hashed password
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            
            # Generate JWT token for immediate login
            token = new_user.generate_auth_token()
            
            return {
                "success": True,
                "message": "User registered successfully",
                "user_id": new_user.id,
                "token": token
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Registration failed: {e}")
            return {"success": False, "error": "Registration failed"}, 500

    @app.route("/api/login", methods=["POST"])
    def login():
        """User login with JWT authentication"""
        try:
            user_info = json.loads(request.data)["user_info"]
            username = user_info["username"]
            password = user_info["password"]
            
            # Find user by username
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                # Create a new session for the user
                user_session = UserModelSession(user_id=user.id)
                db.session.add(user_session)
                db.session.commit()
                
                # Generate JWT token
                token = user.generate_auth_token()
                
                try:
                    # Try to get initial response from decision maker
                    from backend.models.rule_based_model import decision_maker
                    initial_output = decision_maker.determine_next_choice(
                        user.id, "any", None, db.session, user_session, app
                    )
                    
                    return {
                        "success": True, 
                        "validID": True,
                        "userID": user.id,
                        "sessionID": user_session.id,
                        "token": token,
                        "model_prompt": initial_output["model_prompt"],
                        "choices": initial_output["choices"]
                    }
                except Exception as e:
                    # Fallback if decision maker fails (e.g., LLM API issues)
                    logger.warning(f"Decision maker failed: {e}")
                    
                    # Provide a basic response that doesn't rely on LLM
                    return {
                        "success": True, 
                        "validID": True,
                        "userID": user.id,
                        "sessionID": user_session.id,
                        "token": token,
                        "model_prompt": "Hi, I'm MindGuide, welcome to today's session. How are you feeling today?",
                        "choices": ["我很好，谢谢", "我有点难过", "我感到焦虑", "我想聊聊心事"]
                    }
            else:
                return {"success": False, "validID": False, "error": "Invalid username or password"}, 401
        except Exception as e:
            return {"success": False, "validID": False, "error": str(e)}, 500

    # Add new API endpoints for enhanced features
    @app.route('/api/upload_document', methods=['POST'])
    def upload_document():
        """Upload psychology document for RAG system"""
        try:
            from backend.models.rag_system import rag_system
            
            if 'file' not in request.files:
                return {"success": False, "error": "No file provided"}, 400
            
            file = request.files['file']
            user_id = request.form.get('user_id')
            title = request.form.get('title', file.filename)
            if file.filename == '':
                return {"success": False, "error": "No file selected"}, 400
            
            # Save temporary file
            import tempfile
            temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1])
            file.save(temp_path.name)
            
            # Process document
            doc_id = rag_system.upload_document(temp_path.name, user_id, title)
            
            # Clean up
            os.unlink(temp_path.name)
            
            if doc_id:
                return {"success": True, "doc_id": doc_id, "message": "Document uploaded successfully"}
            else:
                return {"success": False, "error": "Failed to process document"}, 500
                
        except Exception as e:
            app.logger.error(f"Document upload failed: {e}")
            return {"success": False, "error": str(e)}, 500

    @app.route('/api/generate_speech', methods=['POST'])
    def generate_speech():
        """Generate speech from text"""
        try:
            from backend.services.tts_service import tts_service
            
            data = request.get_json()
            text = data.get('text')
            user_emotion = data.get('user_emotion')
            
            if not text:
                return {"success": False, "error": "No text provided"}, 400
            
            audio_file = tts_service.generate_therapeutic_voice_response(text, user_emotion)
            
            if audio_file:
                return {"success": True, "audio_file": audio_file}
            else:
                return {"success": False, "error": "TTS generation failed"}, 500
                
        except Exception as e:
            app.logger.error(f"Speech generation failed: {e}")
            return {"success": False, "error": str(e)}, 500

    @app.route('/api/execute_tool', methods=['POST'])
    def execute_tool():
        """Execute an MCP tool"""
        try:
            from backend.services.mcp_integration import mcp_client
            
            data = request.get_json()
            tool_name = data.get('tool_name')
            parameters = data.get('parameters', {})
            
            if not tool_name:
                return {"success": False, "error": "Tool name required"}, 400
            
            result = mcp_client.process_tool_call({
                "name": tool_name,
                "parameters": parameters
            })
            
            return {
                "success": True,
                "result": result,
                "message": "Tool executed successfully"
            }
            
        except Exception as e:
            app.logger.error(f"Tool execution failed: {e}")
            return {"success": False, "error": str(e)}, 500

    # Core therapy session update endpoint - Now using LLM
    @app.route("/api/update_session", methods=["POST"])
    def update_session():
        """Update therapy session with user message and get LLM response"""
        try:
            from backend.services.llm_therapy_service import therapy_service
            
            choice_info = json.loads(request.data)["choice_info"]
            user_id = choice_info["user_id"]
            session_id = choice_info["session_id"]
            input_type = choice_info["input_type"]
            user_choice = choice_info["user_choice"]

            # Handle input type formatting
            if type(input_type) == list and len(input_type) == 0:
                input_type = "any"
            elif type(input_type) == list and len(input_type) == 1:
                input_type = input_type[0]

            user = User.query.filter_by(id=user_id).first()
            user_session = UserModelSession.query.filter_by(id=session_id).first()

            # Store conversation in memory system
            conversation_text = f"User message: {user_choice}, Input type: {input_type}"
            therapeutic_context = {
                "session_id": session_id,
                "input_type": input_type,
                "message_type": "user_input"
            }
            
            memory_manager.store_conversation(
                user_id=str(user_id), 
                user_name=user.username if user else "unknown",
                conversation_text=conversation_text,
                session_id=str(session_id),
                therapeutic_context=therapeutic_context
            )

            # Process user message using LLM therapy service
            response_data = therapy_service.process_message(
                user_id, session_id, user_choice, input_type
            )
            
            # Update last accessed time
            if user:
                user.last_accessed = datetime.datetime.utcnow()
                db.session.commit()

            return {
                "chatbot_response": response_data["response"],
                "user_options": response_data["options"],
                "emotion": response_data.get("emotion", "neutral"),
                "requires_followup": response_data.get("requires_followup", False)
            }
            
        except Exception as e:
            app.logger.error(f"Session update failed: {e}")
            return {"success": False, "error": str(e)}, 500

    # JWT token verification middleware
    def token_required(f):
        """Decorator to verify JWT tokens"""
        from functools import wraps
        
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            
            if not token:
                return {"success": False, "error": "Token is missing"}, 401
            
            if token.startswith('Bearer '):
                token = token[7:]
            
            user = User.verify_auth_token(token)
            if not user:
                return {"success": False, "error": "Token is invalid or expired"}, 401
            
            return f(user, *args, **kwargs)
        
        return decorated

    # Mobile and mini-program chat endpoint with token authentication
    @app.route('/api/chat', methods=['POST'])
    @token_required
    def chat_endpoint(user):
        """Direct chat endpoint for mobile and mini-program clients"""
        try:
            from backend.services.llm_therapy_service import therapy_service
            
            data = request.get_json()
            message = data.get('message', '')
            session_id = data.get('session_id', '')
            
            if not message:
                return {"success": False, "error": "Message is required"}, 400
            
            # Process message using LLM therapy service
            response_data = therapy_service.process_message(
                user.id, session_id, message, "text"
            )
            
            return {
                "success": True,
                "response": response_data["response"],
                "options": response_data["options"],
                "emotion": response_data.get("emotion", "neutral"),
                "requires_followup": response_data.get("requires_followup", False),
                "session_id": session_id,
                "user_id": user.id
            }
            
        except Exception as e:
            app.logger.error(f"Chat endpoint error: {e}")
            return {"success": False, "error": "服务器内部错误"}, 500

    # Protected user profile endpoint example
    @app.route('/api/user/profile', methods=['GET'])
    @token_required
    def user_profile(user):
        """Get user profile information"""
        try:
            return {
                "success": True,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "date_created": user.date_created.isoformat() if user.date_created else None,
                    "last_accessed": user.last_accessed.isoformat() if user.last_accessed else None
                }
            }
        except Exception as e:
            app.logger.error(f"User profile error: {e}")
            return {"success": False, "error": "Failed to get user profile"}, 500
    
    # JWT token verification middleware
    def token_required(f):
        """Decorator to verify JWT tokens"""
        from functools import wraps
        
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            
            if not token:
                return {"success": False, "error": "Token is missing"}, 401
            
            if token.startswith('Bearer '):
                token = token[7:]
            
            user = User.verify_auth_token(token)
            if not user:
                return {"success": False, "error": "Token is invalid or expired"}, 401
            
            return f(user, *args, **kwargs)
        
        return decorated

    # Mobile login endpoint
    @app.route('/api/mobile_login', methods=['POST'])
    def mobile_login():
        """Mobile and mini-program login endpoint"""
        try:
            from backend.services.llm_therapy_service import therapy_service
            
            data = request.get_json()
            username = data.get('username', 'Mobile User')
            
            # Create or get user
            user = User.query.filter_by(username=username).first()
            if not user:
                # Create user with hashed password for mobile
                user = User(username=username)
                user.set_password(f'mobile_{datetime.datetime.now().timestamp()}')
                db.session.add(user)
                db.session.commit()
            
            # Create session
            user_session = UserModelSession(user_id=user.id)
            db.session.add(user_session)
            db.session.commit()
            
            # Generate JWT token
            token = user.generate_auth_token()
            
            # Initialize session with LLM
            session_data = therapy_service.initialize_session(user.id, user_session.id)
            
            return {
                "success": True,
                "token": token,
                "user_id": user.id,
                "session_id": user_session.id,
                "initial_response": session_data["response"],
                "initial_options": session_data["options"]
            }
            
        except Exception as e:
            app.logger.error(f"Mobile login error: {e}")
            return {"success": False, "error": "登录失败"}, 500
    
    return app