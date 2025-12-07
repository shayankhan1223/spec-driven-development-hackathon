import sys
import os

# Add the rag_chatbot directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

# Change to the rag_chatbot directory
os.chdir(os.path.join(os.path.dirname(__file__), '.'))

# Now import and run the app
from main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)