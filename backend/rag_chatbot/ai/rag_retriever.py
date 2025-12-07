import openai
from typing import List, Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vector_store.qdrant_client import QdrantService
from config import settings


class RAGRetriever:
    def __init__(self):
        self.qdrant_service = QdrantService()
        openai.api_key = settings.OPENAI_API_KEY

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant documents based on the query"""
        # Generate embedding for the query
        query_embedding = self._get_embedding(query)

        # Search for similar documents in the vector store
        results = self.qdrant_service.search_similar(query_embedding, limit=top_k)

        return results

    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding for text using OpenAI API"""
        try:
            response = openai.Embedding.create(
                input=text,
                model=settings.EMBEDDING_MODEL
            )
            return response['data'][0]['embedding']
        except Exception as e:
            print(f"Error generating embedding: {e}")
            # Return a zero vector in case of error (this is just a fallback)
            return [0.0] * settings.EMBEDDING_DIMENSION

    def add_document(self, text: str, metadata: Dict[str, Any]) -> str:
        """Add a document to the vector store"""
        # Generate embedding for the document
        embedding = self._get_embedding(text)

        # Store in Qdrant
        doc_id = self.qdrant_service.store_document(text, embedding, metadata)

        return doc_id

    def batch_add_documents(self, documents: List[Dict[str, Any]]) -> List[str]:
        """Add multiple documents to the vector store"""
        doc_ids = []
        for doc in documents:
            doc_id = self.add_document(doc["content"], doc["metadata"])
            doc_ids.append(doc_id)
        return doc_ids