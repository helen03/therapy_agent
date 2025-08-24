import sys
import os

# Add the current directory to sys.path so that model can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the app
from model import create_app
app = create_app()
app.run(debug=True)