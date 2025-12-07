# Physical AI & Humanoid Robotics Textbook RAG Chatbot

This project implements a Retrieval-Augmented Generation (RAG) chatbot for the Physical AI & Humanoid Robotics textbook using OpenAI's Assistant API, FastAPI, Qdrant Cloud, and Neon Postgres.

## Features

- **Textbook Integration**: Full integration with the 46-chapter Physical AI & Humanoid Robotics textbook
- **RAG Functionality**: Uses OpenAI's Assistant API with file search for contextual responses
- **Dual Approach Support**: Supports both traditional embeddings and OpenAI Assistant API
- **Text Selection**: Select any text in the document to trigger a beautiful "Ask AI" ticker
- **Contextual Questions**: Type specific questions about selected text in the input field that appears
- **Source Citations**: Responses include citations to relevant textbook sections
- **Responsive Design**: Works on desktop and mobile devices

## Architecture

```
backend/
├── rag_chatbot/
│   ├── __init__.py
│   ├── main.py (FastAPI app)
│   ├── config.py (configuration settings)
│   ├── app_runner.py (application runner)
│   ├── initialize_assistant.py (Assistant setup script)
│   ├── requirements.txt (dependencies)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── chat.py (Pydantic models for chat)
│   │   ├── document.py (Pydantic models for documents)
│   │   └── database.py (SQLAlchemy models)
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py (Neon Postgres connection)
│   │   ├── models.py (SQLAlchemy models)
│   │   └── crud.py (CRUD operations)
│   ├── vector_store/
│   │   ├── __init__.py
│   │   ├── qdrant_client.py (Qdrant Cloud integration)
│   │   └── document_processor.py (document indexing)
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── openai_agent.py (OpenAI Agent integration)
│   │   ├── rag_retriever.py (RAG retrieval logic)
│   │   └── openai_assistant.py (OpenAI Assistant API integration)
│   └── api/
│       ├── __init__.py
│       ├── chat.py (chat endpoints)
│       └── documents.py (document management endpoints)
```

## Setup Instructions

### Prerequisites

1. Python 3.8+
2. OpenAI API key
3. Qdrant Cloud account (optional, for traditional RAG approach)
4. Neon Postgres database (optional, for conversation history)

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
# Create a .env file with the following variables:
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_url (optional)
QDRANT_API_KEY=your_qdrant_api_key (optional)
DATABASE_URL=your_neon_postgres_url (optional)
ASSISTANT_ID=your_assistant_id (if using OpenAI Assistant API)
VECTOR_STORE_ID=your_vector_store_id (if using OpenAI Assistant API)
```

### OpenAI Assistant Setup

If you want to use the OpenAI Assistant API (recommended), run the initialization script:

```bash
python initialize_assistant.py
```

This will:
1. Create a vector store with the textbook content
2. Upload the textbook content to OpenAI
3. Create an assistant with file search capability
4. Link the assistant to the vector store
5. Output the Assistant ID and Vector Store ID for configuration

### Running the Application

Start the backend server:

```bash
python app_runner.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /health` - Health check
- `POST /api/v1/chat/message` - Chat message endpoint
- `POST /api/v1/chat/index` - Document indexing endpoint
- `POST /api/v1/documents/search` - Document search endpoint
- `GET /api/v1/documents/status` - Document indexing status

## Frontend Integration

The chat widget is integrated into the Docusaurus site and appears on all textbook pages. It includes:

- Floating chat button in the bottom-right corner
- Text selection functionality with "Ask AI" button
- Conversation history
- Source citations
- Dark/light mode support

## Configuration

The application supports two RAG approaches:

### 1. OpenAI Assistant API (Recommended)
- Uses OpenAI's managed assistants with file search
- Better for complex document understanding
- Requires Assistant ID and Vector Store ID

### 2. Traditional RAG Approach
- Uses embeddings stored in Qdrant Cloud
- Self-managed retrieval pipeline
- Falls back if Assistant API is not configured

## Usage

1. Select any text in the textbook
2. Click the "Ask AI" button that appears
3. The chatbot will provide explanations based on the selected text
4. Alternatively, use the chat widget to ask general questions about the textbook

## Development

For development, the application is set up with hot reloading:

```bash
python app_runner.py
```

## Deployment

For production deployment:

1. Set `reload=False` in `app_runner.py`
2. Use a WSGI server like Gunicorn
3. Set up proper environment variables
4. Configure reverse proxy (nginx, Apache)

## Troubleshooting

### Common Issues

1. **OpenAI API Key**: Ensure your API key is valid and has sufficient credits
2. **Assistant Configuration**: If using Assistant API, ensure ASSISTANT_ID and VECTOR_STORE_ID are set
3. **CORS Issues**: Check that your frontend domain is allowed in the backend configuration

### Environment Variables

Required:
- `OPENAI_API_KEY`: Your OpenAI API key

Optional (for full functionality):
- `ASSISTANT_ID`: OpenAI Assistant ID
- `VECTOR_STORE_ID`: OpenAI Vector Store ID
- `QDRANT_URL`: Qdrant Cloud URL
- `QDRANT_API_KEY`: Qdrant Cloud API key
- `DATABASE_URL`: Postgres database URL

## License

This project is part of the Physical AI & Humanoid Robotics textbook implementation.