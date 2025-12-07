from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..ai.rag_retriever import RAGRetriever


router = APIRouter()

class DocumentQuery(BaseModel):
    query: str
    top_k: Optional[int] = 5


class DocumentResponse(BaseModel):
    results: List[dict]


@router.post("/search", response_model=DocumentResponse)
async def search_documents(query: DocumentQuery):
    """Search for documents based on query"""
    try:
        retriever = RAGRetriever()
        results = retriever.retrieve(query.query, query.top_k)

        return DocumentResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching documents: {str(e)}")


@router.get("/status")
async def documents_status():
    """Get status of document indexing"""
    try:
        # In a full implementation, you would return actual indexing status
        return {
            "status": "ready",
            "documents_count": 0,
            "last_indexed": "never"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting status: {str(e)}")