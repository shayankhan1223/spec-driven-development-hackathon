"""
Application runner for the RAG chatbot
This file provides the entry point for running the application
"""

import uvicorn
from main import app
from config import settings


def run_app():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Set to False in production
        log_level="info"
    )


if __name__ == "__main__":
    run_app()