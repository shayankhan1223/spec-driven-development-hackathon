from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import settings
import uuid


class QdrantService:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            prefer_grpc=True
        )
        self.collection_name = settings.QDRANT_COLLECTION_NAME
        self._initialize_collection()

    def _initialize_collection(self):
        """Initialize the Qdrant collection with proper configuration"""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=settings.EMBEDDING_DIMENSION,
                    distance=models.Distance.COSINE
                )
            )

    def store_document(self, text: str, embedding: List[float], metadata: Dict):
        """Store a document with its embedding in Qdrant"""
        point_id = str(uuid.uuid4())

        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "text": text,
                        "metadata": metadata
                    }
                )
            ]
        )
        return point_id

    def search_similar(self, query_embedding: List[float], limit: int = 5) -> List[Dict]:
        """Search for similar documents based on embedding"""
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
            with_payload=True
        )

        return [
            {
                "text": result.payload["text"],
                "metadata": result.payload["metadata"],
                "score": result.score
            }
            for result in results
        ]

    def delete_document(self, document_id: str):
        """Delete a document from Qdrant"""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.PointIdsList(
                points=[document_id]
            )
        )