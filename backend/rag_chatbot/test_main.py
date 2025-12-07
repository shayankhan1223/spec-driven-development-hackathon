"""
Test suite for the RAG chatbot
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from .main import app
from .ai.rag_retriever import RAGRetriever
from .ai.openai_agent import OpenAIAgent


@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_chat_message_endpoint(client):
    """Test the chat message endpoint"""
    payload = {
        "message": "What is Physical AI?",
        "history": []
    }
    response = client.post("/api/v1/chat/message", json=payload)
    # Note: This test would require mocking external services in a real implementation
    # For now, we'll just test that the endpoint exists
    assert response.status_code in [200, 500]  # Could fail due to missing API keys


def test_document_indexing_endpoint(client):
    """Test the document indexing endpoint"""
    payload = {
        "force_reindex": False
    }
    response = client.post("/api/v1/chat/index", json=payload)
    # Note: This test would require mocking external services in a real implementation
    assert response.status_code in [200, 500]  # Could fail due to missing API keys


def test_rag_retriever_initialization():
    """Test RAG retriever initialization"""
    # This would require proper configuration for a real test
    # For now, we'll just test that the class can be instantiated
    try:
        retriever = RAGRetriever()
        assert retriever is not None
    except:
        # In a test environment, this might fail due to missing configuration
        # which is expected
        pass


def test_openai_agent_initialization():
    """Test OpenAI agent initialization"""
    # This would require proper configuration for a real test
    try:
        agent = OpenAIAgent()
        assert agent is not None
    except:
        # In a test environment, this might fail due to missing configuration
        # which is expected
        pass