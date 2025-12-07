from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .connection import Base
import uuid


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=True)  # Could be session ID or actual user ID
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    title = Column(String, nullable=True)  # Auto-generated title based on first query

    # Relationship to messages
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now())
    token_count = Column(Integer, default=0)

    # Relationship back to conversation
    conversation = relationship("Conversation", back_populates="messages")

    # Store sources for RAG responses
    sources = Column(Text, nullable=True)  # JSON string of sources used


class DocumentMetadata(Base):
    __tablename__ = "document_metadata"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_file = Column(String, nullable=False)
    part = Column(String, nullable=True)
    chapter = Column(String, nullable=True)
    section = Column(String, nullable=True)
    full_path = Column(String, nullable=False)
    chunk_id = Column(String, nullable=True)
    chunk_index = Column(Integer, nullable=True)
    total_chunks = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=func.now())
    indexed = Column(Boolean, default=False)
    embedding_id = Column(String, nullable=True)  # ID in Qdrant


class ChatSettings(Base):
    __tablename__ = "chat_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    setting_key = Column(String, unique=True, nullable=False)
    setting_value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())