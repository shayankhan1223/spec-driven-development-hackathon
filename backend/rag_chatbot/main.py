from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from .config import settings

def create_app():
    app = FastAPI(
        title="Physical AI & Humanoid Robotics Textbook RAG Chatbot",
        description="RAG chatbot API for the Physical AI & Humanoid Robotics textbook",
        version="1.0.0"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    from .api.chat import router as chat_router
    from .api.documents import router as documents_router
    from .api.agents import router as agents_router

    app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"])
    app.include_router(documents_router, prefix="/api/v1/documents", tags=["documents"])
    app.include_router(agents_router, prefix="/api/v1/agents", tags=["agents"])

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return app

app = create_app()