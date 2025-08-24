# Simple script to test running the app with error handling
import traceback
import sys
import os

# Add the parent directory to Python path so we can import model module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Attempting to start the app...")
try:
    from backend import create_app
    app = create_app()
    print("App created successfully")
    # Print app configuration for debugging
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print("App is ready to run.")
    # Try to run the app directly
    if __name__ == "__main__":
        print("Starting Flask server...")
        app.run(debug=True, host='0.0.0.0', port=5000)
except Exception as e:
    print(f"Error creating app: {str(e)}")
    traceback.print_exc()