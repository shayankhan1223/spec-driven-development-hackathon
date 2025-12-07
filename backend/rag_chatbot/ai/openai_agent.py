import openai
from typing import List, Dict, Any
from ..config import settings
from .rag_retriever import RAGRetriever
from .openai_assistant import OpenAIAssistant
from .agent_manager import AgentManager


class OpenAIAgent:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.rag_retriever = RAGRetriever()
        self.assistant = OpenAIAssistant()
        self.agent_manager = AgentManager()

    def generate_response(self, user_query: str, conversation_history: List[Dict] = None, selected_text: str = None) -> Dict[str, Any]:
        """Generate a response using OpenAI API with RAG context"""
        try:
            # Use the AgentManager for enhanced functionality
            return self.agent_manager.generate_response(user_query, conversation_history, selected_text)
        except Exception as e:
            return {
                "response": f"Error generating response: {str(e)}",
                "retrieved_docs": [],
                "token_usage": {},
                "sources": [],
                "status": "error"
            }

    def _generate_with_assistant(self, user_query: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """Generate response using OpenAI Assistant API"""
        # Extract thread_id from conversation history if available
        thread_id = None
        if conversation_history:
            # In a real implementation, you would extract the thread_id from conversation metadata
            # For now, we'll just pass None to create a new thread
            pass

        result = self.assistant.process_query_with_assistant(user_query, thread_id)

        return {
            "response": result["response"],
            "retrieved_docs": [],  # Assistant handles retrieval internally
            "token_usage": {},  # Assistant doesn't provide token usage directly
            "sources": result.get("sources", []),
            "thread_id": result.get("thread_id")
        }

    def _generate_with_traditional_rag(self, user_query: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """Generate a response using traditional RAG approach with embeddings"""
        # Retrieve relevant documents based on user query
        retrieved_docs = self.rag_retriever.retrieve(user_query)

        # Format the context from retrieved documents
        context = self._format_context(retrieved_docs)

        # Prepare the system message with textbook context
        system_message = {
            "role": "system",
            "content": f"""You are an AI assistant for the Physical AI & Humanoid Robotics textbook.
            Use the following context to answer questions accurately and comprehensively.
            If the context doesn't contain the information needed, say so clearly.

            Context: {context}"""
        }

        # Prepare the conversation messages
        messages = [system_message]

        # Add conversation history if available
        if conversation_history:
            messages.extend(conversation_history)

        # Add the user query
        messages.append({"role": "user", "content": user_query})

        try:
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            # Extract the response
            ai_response = response.choices[0].message.content
            token_usage = response.usage

            # Return response with metadata
            return {
                "response": ai_response,
                "retrieved_docs": retrieved_docs,
                "token_usage": {
                    "prompt_tokens": token_usage.prompt_tokens,
                    "completion_tokens": token_usage.completion_tokens,
                    "total_tokens": token_usage.total_tokens
                },
                "sources": [doc["metadata"] for doc in retrieved_docs]
            }
        except Exception as e:
            return {
                "response": f"Error generating response: {str(e)}",
                "retrieved_docs": [],
                "token_usage": {},
                "sources": []
            }

    def _format_context(self, retrieved_docs: List[Dict]) -> str:
        """Format retrieved documents into context for the AI"""
        if not retrieved_docs:
            return "No relevant information found in the textbook."

        formatted_context = []
        for i, doc in enumerate(retrieved_docs):
            formatted_context.append(
                f"Source {i+1} (from {doc['metadata'].get('source_file', 'unknown')}): "
                f"{doc['text'][:500]}..."  # Limit length to prevent exceeding token limits
            )

        return "\n\n".join(formatted_context)