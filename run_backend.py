#!/usr/bin/env python3
"""
Script to run the Flask backend server
"""

from backend import create_app

if __name__ == "__main__":
    app = create_app()
    print("Starting Flask development server...")
    print("Server will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000)