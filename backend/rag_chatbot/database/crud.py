from sqlalchemy.orm import Session
from typing import List, Optional
from .models import Conversation, Message, DocumentMetadata, ChatSettings
import json


# Conversation CRUD operations
def create_conversation(db: Session, user_id: Optional[str] = None, title: Optional[str] = None):
    """Create a new conversation"""
    conversation = Conversation(user_id=user_id, title=title)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def get_conversation(db: Session, conversation_id: str):
    """Get a conversation by ID"""
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()


def get_conversations(db: Session, user_id: Optional[str] = None, skip: int = 0, limit: int = 100):
    """Get conversations for a user"""
    query = db.query(Conversation)
    if user_id:
        query = query.filter(Conversation.user_id == user_id)
    return query.offset(skip).limit(limit).all()


# Message CRUD operations
def create_message(db: Session, conversation_id: str, role: str, content: str, sources: Optional[List[dict]] = None):
    """Create a new message in a conversation"""
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        sources=json.dumps(sources) if sources else None
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_messages(db: Session, conversation_id: str):
    """Get all messages for a conversation"""
    return db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.timestamp).all()


def get_recent_messages(db: Session, conversation_id: str, limit: int = 10):
    """Get recent messages for a conversation"""
    return db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.timestamp.desc()).limit(limit).all()


# Document metadata CRUD operations
def create_document_metadata(db: Session, source_file: str, part: str, chapter: str, section: str, full_path: str,
                            chunk_id: Optional[str] = None, chunk_index: Optional[int] = None, total_chunks: Optional[int] = None,
                            indexed: bool = False, embedding_id: Optional[str] = None):
    """Create document metadata entry"""
    doc_metadata = DocumentMetadata(
        source_file=source_file,
        part=part,
        chapter=chapter,
        section=section,
        full_path=full_path,
        chunk_id=chunk_id,
        chunk_index=chunk_index,
        total_chunks=total_chunks,
        indexed=indexed,
        embedding_id=embedding_id
    )
    db.add(doc_metadata)
    db.commit()
    db.refresh(doc_metadata)
    return doc_metadata


def get_document_metadata(db: Session, source_file: str = None, indexed: Optional[bool] = None):
    """Get document metadata with optional filters"""
    query = db.query(DocumentMetadata)
    if source_file:
        query = query.filter(DocumentMetadata.source_file == source_file)
    if indexed is not None:
        query = query.filter(DocumentMetadata.indexed == indexed)
    return query.all()


def update_document_indexed_status(db: Session, doc_id: str, indexed: bool = True, embedding_id: Optional[str] = None):
    """Update the indexed status of a document"""
    doc = db.query(DocumentMetadata).filter(DocumentMetadata.id == doc_id).first()
    if doc:
        doc.indexed = indexed
        if embedding_id:
            doc.embedding_id = embedding_id
        db.commit()
        db.refresh(doc)
    return doc


# Chat settings CRUD operations
def get_chat_setting(db: Session, setting_key: str):
    """Get a specific chat setting"""
    return db.query(ChatSettings).filter(ChatSettings.setting_key == setting_key).first()


def set_chat_setting(db: Session, setting_key: str, setting_value: str, description: Optional[str] = None):
    """Set or update a chat setting"""
    setting = db.query(ChatSettings).filter(ChatSettings.setting_key == setting_key).first()
    if setting:
        setting.setting_value = setting_value
        setting.description = description
    else:
        setting = ChatSettings(setting_key=setting_key, setting_value=setting_value, description=description)
        db.add(setting)
    db.commit()
    db.refresh(setting)
    return setting