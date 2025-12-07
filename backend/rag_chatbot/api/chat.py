from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from ..ai.openai_agent import OpenAIAgent
from ..database.connection import get_db
from sqlalchemy.orm import Session


router = APIRouter()

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    history: Optional[List[dict]] = []
    selected_text: Optional[str] = None  # For selected text queries


class QueryWithSelectionRequest(BaseModel):
    question: str
    selected_text: str
    conversation_id: Optional[str] = None
    history: Optional[List[dict]] = []


class QueryWithSelectionResponse(BaseModel):
    response: str
    conversation_id: str
    sources: List[dict]


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    sources: List[dict]


class IndexRequest(BaseModel):
    force_reindex: bool = False


class IndexResponse(BaseModel):
    status: str
    documents_processed: int


@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """Handle a chat message and return AI response"""
    try:
        agent = OpenAIAgent()
        # Pass selected_text to the agent if available
        result = agent.generate_response(request.message, request.history, request.selected_text)

        # In a full implementation, you would:
        # 1. Save the conversation to the database
        # 2. Generate a conversation ID if not provided
        # 3. Track usage metrics

        return ChatResponse(
            response=result["response"],
            conversation_id=request.conversation_id or "temp_conversation_id",
            sources=result.get("sources", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat message: {str(e)}")


@router.post("/query_with_selection", response_model=QueryWithSelectionResponse)
async def query_with_selection(request: QueryWithSelectionRequest):
    """Handle a query with selected text context and return AI response"""
    try:
        agent = OpenAIAgent()
        # Combine the question with selected text context
        full_query = f"Regarding the selected text: '{request.selected_text}', {request.question}"

        result = agent.generate_response(full_query, request.history)

        return QueryWithSelectionResponse(
            response=result["response"],
            conversation_id=request.conversation_id or "temp_conversation_id",
            sources=result.get("sources", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query with selection: {str(e)}")


@router.post("/index", response_model=IndexResponse)
async def index_documents(request: IndexRequest):
    """Index textbook documents into the vector store"""
    try:
        # In a full implementation, you would:
        # 1. Process all textbook content using DocumentProcessor
        # 2. Store embeddings in Qdrant using RAGRetriever
        # 3. Track progress and return statistics

        # This is a placeholder implementation
        from ..vector_store.document_processor import DocumentProcessor
        from ..ai.rag_retriever import RAGRetriever

        processor = DocumentProcessor()
        retriever = RAGRetriever()

        # Process textbook content
        documents = processor.process_textbook_content()
        doc_ids = retriever.batch_add_documents(documents)

        return IndexResponse(
            status="completed",
            documents_processed=len(documents)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error indexing documents: {str(e)}")