"""
Initialization script for OpenAI Assistant and Vector Store
This script helps set up the OpenAI Assistant with the textbook content
"""
import os
import openai
from dotenv import load_dotenv
from config import settings
from ai.openai_assistant import OpenAIAssistant
from vector_store.document_processor import DocumentProcessor
import tempfile
import json


def initialize_assistant_with_textbook():
    """
    Initialize the OpenAI Assistant with the textbook content
    This function creates an assistant, vector store, and uploads textbook content
    """
    # Load environment variables
    load_dotenv()

    # Initialize the assistant manager
    assistant_manager = OpenAIAssistant()

    # Set the OpenAI API key
    openai.api_key = settings.OPENAI_API_KEY

    print("Starting OpenAI Assistant initialization...")

    # Step 1: Create a vector store for the textbook content
    print("Creating vector store...")
    vector_store_id = assistant_manager.create_vector_store("Physical AI & Humanoid Robotics Textbook")
    print(f"Vector store created with ID: {vector_store_id}")

    # Step 2: Process textbook content and prepare files
    print("Processing textbook content...")
    processor = DocumentProcessor()
    documents = processor.process_textbook_content()

    # Create temporary files for each document chunk and upload them
    uploaded_file_ids = []

    # Create a temporary directory to store processed chunks
    with tempfile.TemporaryDirectory() as temp_dir:
        for i, doc in enumerate(documents):
            # Create a temporary file for each document chunk
            temp_file_path = os.path.join(temp_dir, f"chunk_{i}.txt")

            with open(temp_file_path, 'w', encoding='utf-8') as f:
                f.write(f"Source: {doc['metadata']['source_file']}\n\n")
                f.write(doc['content'])

            # Upload the file to OpenAI
            print(f"Uploading chunk {i+1}/{len(documents)}...")
            file_id = assistant_manager.upload_file_for_assistant(temp_file_path)
            uploaded_file_ids.append(file_id)

    print(f"Uploaded {len(uploaded_file_ids)} files to OpenAI")

    # Step 3: Add files to the vector store
    print("Adding files to vector store...")
    assistant_manager.batch_add_files_to_vector_store(vector_store_id, uploaded_file_ids)
    print("Files added to vector store successfully")

    # Step 4: Create the assistant with file search capability
    print("Creating assistant with file search capability...")
    assistant_id = assistant_manager.create_assistant(
        name="Physical AI & Humanoid Robotics Textbook Assistant",
        instructions="""You are an AI assistant for the Physical AI & Humanoid Robotics textbook.
        Use the provided textbook content to answer questions accurately and comprehensively.
        Always cite the specific parts of the textbook that you reference in your answers."""
    )

    print(f"Assistant created with ID: {assistant_id}")

    # Step 5: Link the assistant to the vector store
    print("Linking assistant to vector store...")
    assistant_manager.set_assistant_vector_store(assistant_id, vector_store_id)
    print("Assistant linked to vector store successfully")

    # Step 6: Update settings with the created IDs
    print("\nInitialization complete!")
    print(f"Vector Store ID: {vector_store_id}")
    print(f"Assistant ID: {assistant_id}")
    print("\nTo use these in your application, set the following environment variables:")
    print(f"  ASSISTANT_ID={assistant_id}")
    print(f"  VECTOR_STORE_ID={vector_store_id}")

    # Create a .env file with the IDs if it doesn't exist
    env_file_path = ".env"
    if not os.path.exists(env_file_path):
        with open(env_file_path, 'w') as f:
            f.write(f"# OpenAI Assistant Configuration\n")
            f.write(f"ASSISTANT_ID={assistant_id}\n")
            f.write(f"VECTOR_STORE_ID={vector_store_id}\n")
        print(f"\nConfiguration saved to {env_file_path}")

    return {
        "assistant_id": assistant_id,
        "vector_store_id": vector_store_id,
        "uploaded_files_count": len(uploaded_file_ids)
    }


def test_assistant():
    """
    Test the assistant with a sample query
    """
    print("\nTesting the assistant...")

    # Initialize the assistant manager
    assistant_manager = OpenAIAssistant()

    # Test query
    test_query = "What is Physical AI and why is it important?"

    # Process the query
    result = assistant_manager.process_query_with_assistant(test_query)

    print(f"Query: {test_query}")
    print(f"Response: {result['response']}")
    print(f"Sources: {result['sources']}")

    return result


if __name__ == "__main__":
    print("OpenAI Assistant Initialization Script")
    print("=" * 50)

    # Initialize the assistant
    result = initialize_assistant_with_textbook()

    # Optionally test the assistant
    try:
        test_result = test_assistant()
        print("\nTest completed successfully!")
    except Exception as e:
        print(f"\nTest failed (this is expected if the assistant isn't fully configured yet): {e}")

    print("\nThe OpenAI Assistant has been initialized with the textbook content.")
    print("Remember to set the ASSISTANT_ID and VECTOR_STORE_ID environment variables in your deployment.")