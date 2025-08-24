#!/usr/bin/env python3
"""
Script to run the Flask backend server
"""

from backend import create_app

if __name__ == "__main__":
    app = create_app()
    print("Starting Flask development server...")
    print("Server will be available at: http://localhost:5002")
    print("Press Ctrl+C to stop the server")
    app.run(debug=False, host='127.0.0.1', port=5002)