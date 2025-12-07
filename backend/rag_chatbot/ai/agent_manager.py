import openai
from typing import List, Dict, Any, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings
from .rag_retriever import RAGRetriever
from .openai_assistant import OpenAIAssistant
import json
import asyncio
from datetime import datetime


class AgentManager:
    """
    Enhanced Agent Manager that implements OpenAI Agents functionality
    with tool usage, memory management, and RAG integration
    """

    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.rag_retriever = RAGRetriever()
        self.assistant = OpenAIAssistant()
        self.tools = self._initialize_tools()

    def _initialize_tools(self) -> List[Dict[str, Any]]:
        """
        Initialize tools that the agent can use for textbook-related queries
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_textbook_content",
                    "description": "Search the Physical AI & Humanoid Robotics textbook for relevant information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query to find relevant textbook content"
                            },
                            "top_k": {
                                "type": "integer",
                                "description": "Number of results to return (default 5)",
                                "default": 5
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_chapter_outline",
                    "description": "Get the outline of a specific chapter in the textbook",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "chapter_title": {
                                "type": "string",
                                "description": "The title or partial title of the chapter to get outline for"
                            }
                        },
                        "required": ["chapter_title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_glossary_terms",
                    "description": "Get definitions for specific terms from the textbook glossary",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "terms": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "description": "List of terms to look up in the glossary"
                            }
                        },
                        "required": ["terms"]
                    }
                }
            }
        ]

    def execute_tool(self, tool_name: str, tool_args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a specific tool based on the tool name and arguments
        """
        try:
            if tool_name == "search_textbook_content":
                query = tool_args.get("query", "")
                top_k = tool_args.get("top_k", 5)

                # Use RAG retriever to search for relevant content
                results = self.rag_retriever.retrieve(query, top_k=top_k)

                return {
                    "status": "success",
                    "results": [
                        {
                            "content": doc["text"],
                            "source": doc["metadata"].get("source_file", "unknown"),
                            "page": doc["metadata"].get("page", "unknown"),
                            "relevance_score": doc.get("score", 0.0)
                        }
                        for doc in results
                    ]
                }

            elif tool_name == "get_chapter_outline":
                chapter_title = tool_args.get("chapter_title", "").lower()

                # This would be implemented based on the actual textbook structure
                # For now, returning a mock response
                return {
                    "status": "success",
                    "chapter": chapter_title,
                    "outline": [
                        "Introduction",
                        "Main Concepts",
                        "Applications",
                        "Summary",
                        "Exercises"
                    ]
                }

            elif tool_name == "get_glossary_terms":
                terms = tool_args.get("terms", [])

                # Mock glossary - in a real implementation this would come from the textbook
                glossary_results = {}
                for term in terms:
                    glossary_results[term] = f"Definition for {term} from the Physical AI & Humanoid Robotics textbook"

                return {
                    "status": "success",
                    "terms": glossary_results
                }

            else:
                return {
                    "status": "error",
                    "error": f"Unknown tool: {tool_name}"
                }

        except Exception as e:
            return {
                "status": "error",
                "error": f"Error executing tool {tool_name}: {str(e)}"
            }

    def create_agent_thread(self) -> str:
        """
        Create a new conversation thread for the agent
        """
        try:
            thread = openai.beta.threads.create()
            return thread.id
        except Exception as e:
            raise Exception(f"Error creating agent thread: {str(e)}")

    def run_agent_with_tools(self,
                           user_query: str,
                           thread_id: str = None,
                           conversation_history: List[Dict] = None,
                           selected_text: str = None) -> Dict[str, Any]:
        """
        Run the agent with tool usage capabilities
        """
        try:
            # If no thread is provided, create a new one
            if not thread_id:
                thread_id = self.create_agent_thread()

            # Prepare the user query with selected text context if available
            if selected_text:
                enhanced_query = f"Regarding the selected text: '{selected_text}', {user_query}"
            else:
                enhanced_query = user_query

            # Add the user message to the thread
            openai.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=enhanced_query
            )

            # Run the assistant with tools
            run = openai.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=settings.ASSISTANT_ID,
                tools=self.tools,
                model=self.model
            )

            # Wait for the run to complete
            run = self._wait_for_run_completion(thread_id, run.id)

            if run.status == "completed":
                # Get the messages from the thread
                messages = openai.beta.threads.messages.list(
                    thread_id=thread_id,
                    order="desc",
                    limit=1  # Get the latest message
                )

                if messages.data:
                    latest_message = messages.data[0]
                    response_content = ""

                    for content_block in latest_message.content:
                        if content_block.type == "text":
                            response_content += content_block.text.value

                    return {
                        "response": response_content,
                        "thread_id": thread_id,
                        "status": "success"
                    }
                else:
                    return {
                        "response": "No response from agent",
                        "thread_id": thread_id,
                        "status": "error"
                    }

            elif run.status == "requires_action":
                # Handle tool calls
                return self._handle_tool_calls(run, thread_id)

            else:
                return {
                    "response": f"Agent run failed with status: {run.status}",
                    "thread_id": thread_id,
                    "status": "error"
                }

        except Exception as e:
            return {
                "response": f"Error running agent: {str(e)}",
                "thread_id": thread_id,
                "status": "error"
            }

    def _wait_for_run_completion(self, thread_id: str, run_id: str, timeout: int = 300):
        """
        Wait for a run to complete with timeout
        """
        import time

        start_time = time.time()
        while time.time() - start_time < timeout:
            run = openai.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
            )

            if run.status in ["completed", "failed", "cancelled", "expired"]:
                return run

            time.sleep(1)

        raise Exception("Agent run timed out")

    def _handle_tool_calls(self, run, thread_id: str) -> Dict[str, Any]:
        """
        Handle tool calls when the agent requires action
        """
        try:
            tool_calls = []

            for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Execute the tool
                result = self.execute_tool(function_name, function_args)

                # Add to tool calls list for tracking
                tool_calls.append({
                    "id": tool_call.id,
                    "name": function_name,
                    "arguments": function_args,
                    "result": result
                })

                # Submit tool output
                openai.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread_id,
                    run_id=run.id,
                    tool_outputs=[
                        {
                            "tool_call_id": tool_call.id,
                            "output": json.dumps(result)
                        }
                    ]
                )

            # Wait for the run to complete after tool calls
            run = self._wait_for_run_completion(thread_id, run.id)

            if run.status == "completed":
                # Get the final response
                messages = openai.beta.threads.messages.list(
                    thread_id=thread_id,
                    order="desc",
                    limit=1
                )

                if messages.data:
                    latest_message = messages.data[0]
                    response_content = ""

                    for content_block in latest_message.content:
                        if content_block.type == "text":
                            response_content += content_block.text.value

                    return {
                        "response": response_content,
                        "thread_id": thread_id,
                        "tool_calls": tool_calls,
                        "status": "success"
                    }

            return {
                "response": "Error processing tool calls",
                "thread_id": thread_id,
                "status": "error"
            }

        except Exception as e:
            return {
                "response": f"Error handling tool calls: {str(e)}",
                "thread_id": thread_id,
                "status": "error"
            }

    def generate_response(self,
                         user_query: str,
                         conversation_history: List[Dict] = None,
                         selected_text: str = None) -> Dict[str, Any]:
        """
        Main method to generate a response using the agent system
        """
        # If Assistant API is configured, use the enhanced agent
        if settings.ASSISTANT_ID:
            return self.run_agent_with_tools(
                user_query,
                conversation_history=conversation_history,
                selected_text=selected_text
            )
        else:
            # Fall back to the traditional RAG approach
            return self._generate_with_traditional_rag(user_query, conversation_history, selected_text)

    def _generate_with_traditional_rag(self,
                                     user_query: str,
                                     conversation_history: List[Dict] = None,
                                     selected_text: str = None) -> Dict[str, Any]:
        """
        Traditional RAG approach when Assistant API is not available
        """
        try:
            # If selected text is provided, enhance the query
            if selected_text:
                enhanced_query = f"Regarding the selected text: '{selected_text}', {user_query}"
            else:
                enhanced_query = user_query

            # Retrieve relevant documents based on the enhanced query
            retrieved_docs = self.rag_retriever.retrieve(enhanced_query)

            # Format the context from retrieved documents
            context = self._format_context(retrieved_docs)

            # Prepare the system message with textbook context
            system_message = {
                "role": "system",
                "content": f"""You are an AI agent specialized in the Physical AI & Humanoid Robotics textbook.
Your capabilities include:
1. Searching textbook content using tools
2. Providing detailed explanations
3. Answering questions with citations

Use the provided context to answer questions accurately and comprehensively.
If the context doesn't contain the information needed, say so clearly.

Context: {context}"""
            }

            # Prepare the conversation messages
            messages = [system_message]

            # Add conversation history if available
            if conversation_history:
                messages.extend(conversation_history)

            # Add the user query
            messages.append({"role": "user", "content": enhanced_query})

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
                "sources": [doc["metadata"] for doc in retrieved_docs],
                "status": "success"
            }

        except Exception as e:
            return {
                "response": f"Error generating response: {str(e)}",
                "retrieved_docs": [],
                "token_usage": {},
                "sources": [],
                "status": "error"
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