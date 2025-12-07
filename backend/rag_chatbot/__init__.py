"""
RAG Chatbot for Physical AI & Humanoid Robotics Textbook
Entry point for the RAG chatbot system
"""

from .main import app

__version__ = "1.0.0"
__author__ = "Physical AI Textbook Team"

# Initialize the application
application = app

def get_application():
    return application