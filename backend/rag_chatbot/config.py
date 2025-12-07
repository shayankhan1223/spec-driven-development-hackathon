from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    # API Settings
    API_TITLE: str = "Physical AI & Humanoid Robotics Textbook RAG Chatbot"
    API_VERSION: str = "1.0.0"
    ALLOWED_ORIGINS: List[str] = ["*"]  # Should be configured properly in production

    # OpenAI Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    ASSISTANT_ID: str = os.getenv("ASSISTANT_ID", "")  # ID of the OpenAI Assistant
    VECTOR_STORE_ID: str = os.getenv("VECTOR_STORE_ID", "")  # ID of the vector store

    # Qdrant Settings
    QDRANT_URL: str = os.getenv("QDRANT_URL")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION_NAME: str = os.getenv("QDRANT_COLLECTION_NAME", "textbook_content")

    # Neon Postgres Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "20"))
    DB_POOL_OVERFLOW: int = int(os.getenv("DB_POOL_OVERFLOW", "0"))

    # Embedding Settings
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    EMBEDDING_DIMENSION: int = int(os.getenv("EMBEDDING_DIMENSION", "1536"))

    # Document Processing Settings
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "10"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # in seconds


settings = Settings()