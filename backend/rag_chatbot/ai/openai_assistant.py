import openai
from typing import List, Dict, Any, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings
import json
try:
    from openai import AssistantEventHandler
    from typing_extensions import override
    from openai.types.beta.threads import Text, Message
except ImportError:
    # For older versions of the OpenAI library
    AssistantEventHandler = object
    def override(func):
        return func
    # Define placeholder classes
    class Text:
        pass
    class Message:
        pass


class OpenAIAssistant:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.assistant_id = settings.ASSISTANT_ID  # This would need to be configured
        self.model = settings.OPENAI_MODEL
        self.vector_store_id = settings.VECTOR_STORE_ID  # This would need to be configured

    def create_assistant(self, name: str, instructions: str) -> str:
        """Create a new OpenAI Assistant with the specified name and instructions"""
        assistant = openai.beta.assistants.create(
            name=name,
            instructions=instructions,
            model=self.model,
            tools=[{"type": "file_search"}],  # Enable file search for RAG functionality
        )
        return assistant.id

    def create_thread(self) -> str:
        """Create a new conversation thread"""
        thread = openai.beta.threads.create()
        return thread.id

    def add_message_to_thread(self, thread_id: str, message: str) -> str:
        """Add a message to a thread"""
        message_obj = openai.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message
        )
        return message_obj.id

    def run_assistant(self, thread_id: str, assistant_id: str) -> str:
        """Run the assistant on a thread and return the run ID"""
        run = openai.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        return run.id

    def wait_for_run_completion(self, thread_id: str, run_id: str):
        """Wait for a run to complete and return the result"""
        import time

        while True:
            run = openai.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
            )

            if run.status in ['completed', 'failed', 'cancelled', 'expired']:
                break

            time.sleep(1)

        return run

    def get_thread_messages(self, thread_id: str) -> List[Dict]:
        """Get all messages from a thread"""
        messages = openai.beta.threads.messages.list(
            thread_id=thread_id,
            order="asc"  # Ascending order to get chronological order
        )

        # Convert to our format
        result = []
        for msg in messages.data:
            content = ""
            sources = []

            for item in msg.content:
                if item.type == "text":
                    content += item.text.value

                    # Extract annotations as sources
                    if hasattr(item.text, 'annotations'):
                        for annotation in item.text.annotations:
                            if hasattr(annotation, 'file_citation'):
                                sources.append({
                                    'type': 'file_citation',
                                    'quote': annotation.quote,
                                    'file_id': annotation.file_citation.file_id
                                })
                            elif hasattr(annotation, 'file_path'):
                                sources.append({
                                    'type': 'file_path',
                                    'file_id': annotation.file_path.file_id
                                })

            result.append({
                "id": msg.id,
                "role": msg.role,
                "content": content,
                "timestamp": msg.created_at,
                "sources": sources
            })

        return result

    def stream_response_with_handler(self, thread_id: str, assistant_id: str):
        """Stream response using AssistantEventHandler"""
        class EventHandler(AssistantEventHandler):
            def __init__(self):
                super().__init__()
                self.content = ""
                self.sources = []

            @override
            def on_text_created(self, text: Text) -> None:
                pass

            @override
            def on_text_delta(self, delta, snapshot):
                if delta.value:
                    self.content += delta.value
                if delta.annotations:
                    for annotation in delta.annotations:
                        if hasattr(annotation, 'file_citation'):
                            self.sources.append({
                                'type': 'file_citation',
                                'quote': annotation.quote,
                                'file_id': annotation.file_citation.file_id
                            })
                        elif hasattr(annotation, 'file_path'):
                            self.sources.append({
                                'type': 'file_path',
                                'file_id': annotation.file_path.file_id
                            })

        event_handler = EventHandler()

        with openai.beta.threads.runs.stream(
            thread_id=thread_id,
            assistant_id=assistant_id,
            event_handler=event_handler
        ) as stream:
            stream.until_done()

        return {
            "content": event_handler.content,
            "sources": event_handler.sources
        }

    def process_query_with_assistant(self, query: str, thread_id: Optional[str] = None, use_streaming: bool = False) -> Dict[str, Any]:
        """Process a query using the OpenAI Assistant API"""
        try:
            # Create a thread if one isn't provided
            if not thread_id:
                thread_id = self.create_thread()

            # Add the user's message to the thread
            self.add_message_to_thread(thread_id, query)

            # Run the assistant
            run_id = self.run_assistant(thread_id, self.assistant_id)

            if use_streaming:
                # Use streaming response
                result = self.stream_response_with_handler(thread_id, self.assistant_id)

                return {
                    "response": result["content"],
                    "thread_id": thread_id,
                    "sources": result["sources"],
                    "status": "success"
                }
            else:
                # Wait for completion (traditional approach)
                run = self.wait_for_run_completion(thread_id, run_id)

                if run.status == 'completed':
                    # Get the messages from the thread
                    messages = self.get_thread_messages(thread_id)

                    # Find the assistant's latest response
                    assistant_responses = [msg for msg in messages if msg['role'] == 'assistant']

                    if assistant_responses:
                        latest_response = assistant_responses[-1]  # Get the latest response

                        return {
                            "response": latest_response['content'],
                            "thread_id": thread_id,
                            "sources": latest_response.get('sources', []),
                            "status": "success"
                        }
                    else:
                        return {
                            "response": "No response from assistant",
                            "thread_id": thread_id,
                            "sources": [],
                            "status": "error"
                        }
                else:
                    return {
                        "response": f"Error running assistant: {run.status}",
                        "thread_id": thread_id,
                        "sources": [],
                        "status": "error"
                    }

        except Exception as e:
            return {
                "response": f"Error processing query: {str(e)}",
                "thread_id": thread_id,
                "sources": [],
                "status": "error"
            }

    def upload_file_for_assistant(self, file_path: str) -> str:
        """Upload a file to be used with the assistant"""
        file_obj = openai.files.create(
            file=open(file_path, "rb"),
            purpose="assistants"
        )
        return file_obj.id

    def create_vector_store(self, name: str) -> str:
        """Create a vector store for file search"""
        vector_store = openai.beta.vector_stores.create(
            name=name
        )
        return vector_store.id

    def add_file_to_vector_store(self, vector_store_id: str, file_id: str):
        """Add a file to a vector store"""
        openai.beta.vector_stores.file_batches.create_and_poll(
            vector_store_id=vector_store_id,
            files=[file_id]
        )

    def set_assistant_vector_store(self, assistant_id: str, vector_store_id: str):
        """Update an assistant to use a vector store"""
        openai.beta.assistants.update(
            assistant_id=assistant_id,
            tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}}
        )

    def batch_add_files_to_vector_store(self, vector_store_id: str, file_ids: List[str]):
        """Add multiple files to a vector store at once"""
        openai.beta.vector_stores.file_batches.create_and_poll(
            vector_store_id=vector_store_id,
            files=file_ids
        )