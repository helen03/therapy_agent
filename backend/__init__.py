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
load_dotenv(os.path.join(basedir, ".env"))


# For dev logging - comment out for Gunicorn
logging.basicConfig(
    level=logging.INFO,
    format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)

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

    @app.route("/api/login", methods=["POST"])
    def login():
        user_info = json.loads(request.data)["user_info"]
        username = user_info["username"]
        password = user_info["password"]
        usernames = ["user" + str(i) for i in range(1, 31)]
        passwords = [
            "ph6n76gec9",
            "l98zjxj6vc",
            "mq577o05wz",
            "tcty170i9o",
            "1kgh4895fx",
            "ys175n9iv0",
            "0fvcfgxplj",
            "vu34rphc82",
            "hyhnyg9xob",
            "oqqct6wllc",
            "oswly1eaxq",
            "qe7inpmska",
            "7ilhsc46ox",
            "wo81yy0eci",
            "2kufnda8bs",
            "nzlljrerzt",
            "ft0jinctnm",
            "r3swsmr2rn",
            "4cbp35phhh",
            "falyezzw4r",
            "r5v0mrvpuv",
            "auee014rmj",
            "wpprodq8vb",
            "6nddssd3gg",
            "z2394iw3mq",
            "a3gkc6czb5",
            "ddxzlpkzhv",
            "2owdt20zas",
            "29uhzahhol",
            "mfhs4cyc4x",
        ]
        for i in range(len(usernames)):
            try:
                # Creates new accounts
                new_user = User(username=usernames[i], password=passwords[i])
                db.session.add(new_user)
                db.session.commit()

            except:  # noqa
                db.session.rollback()

        try:
            guest_user = User(username="guest", password="guest")
            db.session.add(guest_user)
            db.session.commit()
        except:  # noqa
            db.session.rollback()

        try:
            user = User.query.filter_by(username=username, password=password).first()
            if user:
                return {"success": True, "user_id": user.id}
            else:
                return {"success": False, "error": "Invalid username or password"}, 401
        except Exception as e:
            return {"success": False, "error": str(e)}, 500

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

    # Core therapy session update endpoint
    @app.route("/api/update_session", methods=["POST"])
    def update_session():
        """Update therapy session with user choice and get next response"""
        try:
            from backend.models.rule_based_model import decision_maker
            
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
            conversation_text = f"User choice: {user_choice}, Input type: {input_type}"
            therapeutic_context = {
                "session_id": session_id,
                "input_type": input_type,
                "exercise_phase": decision_maker.user_choices.get(user_id, {}).get("choices_made", {}).get("current_choice", "unknown")
            }
            
            memory_manager.store_conversation(
                user_id=str(user_id), 
                user_name=user.username if user else "unknown",
                conversation_text=conversation_text,
                session_id=str(session_id),
                therapeutic_context=therapeutic_context
            )

            # Process user choice and determine next response
            decision_maker.save_current_choice(
                user_id, input_type, user_choice, user_session, db.session, app
            )
            
            output = decision_maker.determine_next_choice(
                user_id, input_type, user_choice, db.session, user_session, app
            )
            
            # Enhance response with memory context if available
            if "model_prompt" in output:
                current_context = f"Therapeutic context: {input_type}, User choice: {user_choice}"
                enhanced_response = memory_manager.enhance_response_with_memory(
                    user_id=str(user_id),
                    proposed_response=output["model_prompt"],
                    current_context=current_context
                )
                output["model_prompt"] = enhanced_response
            
            # Update last accessed time
            if user:
                user.last_accessed = datetime.datetime.utcnow()
                db.session.commit()

            return {
                "chatbot_response": output["model_prompt"],
                "user_options": output["choices"],
            }
            
        except Exception as e:
            app.logger.error(f"Session update failed: {e}")
            return {"success": False, "error": str(e)}, 500

    return app