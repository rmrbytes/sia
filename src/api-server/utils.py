# utils.py

# 1. logger functions
# 2. file functions in agents folder in the host system
# 3. calls with the embeddings_server

import os
import shutil
import re
import httpx
import logging
from config import settings
from typing import List, Dict, Any
from exceptions import FileStorageException, ExternalServiceException

# Setup logger configuration
def setup_logger() -> logging.Logger:
    # Set up the logging configuration based on the DEBUG mode in environment.
    #Logs to both console and file if enabled.
    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if settings.debug else logging.INFO)
    
    # File handler
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.DEBUG if settings.debug else logging.INFO)
    
    # Formatter for the log messages
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # Apply formatter to both handlers
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers to the logger
    logger.addHandler(console_handler)
    #logger.addHandler(file_handler)
    
    return logger

# Initialize logger
logger = setup_logger()

# Log chat activity
def log_chat_activity(agent_name: str, user_message: str, assistant_response: str) -> None:
    # Log the interaction between a user and the assistant in the chat.
    logger.info(f"Agent: {agent_name}, User: {user_message}, Assistant: {assistant_response}")

# Santize agent name
def sanitize_agent_name(name):
    # Convert to lowercase
    name = name.lower()
    # Remove any character that is not a letter, digit, or hyphen
    name = re.sub(r'[^a-z0-9-]', '', name)
    return name

# Process uploaded files and manage deletions
def process_uploaded_files(agent_name: str, new_files: List[Any] = [], deleted_files: List[str] = []) -> str:
    
    try:
        # Log the processing of files
        logger.debug(f"Processing files for agent: {agent_name}")
        # set the agent dir
        agent_dir = os.path.join(settings.agents_dir, agent_name)
        # Ensure the agent directory exists
        os.makedirs(agent_dir, exist_ok=True)  
        # Step 1: Process deleted files (remove them from the agent's directory)
        for file in deleted_files:
            file_path = os.path.join(agent_dir, file)
            if os.path.exists(file_path):
                os.remove(file_path)

        # Step 2: Process new files (add them to the agent's directory)
        for file in new_files:
            file_path = os.path.join(agent_dir, file.filename)
            with open(file_path, "wb") as f:
                f.write(file.file.read())

        return

    except Exception as e:
        raise FileStorageException(detail=f"Error processing files of {agent_name}: {str(e)}")


# Trigger embeddings generation asynchronously
async def trigger_embeddings_generation(agent_name: str, files: List[Dict[str, Any]]) -> None:
    try:
        logger.debug(f"Triggering embeddings generation for agent: {agent_name}")

        # Set the URL and headers
        url = f"http://{settings.embeddings_server}:{settings.embeddings_server_port}/generate"
        headers = {settings.header_name: settings.header_key}

        # Prepare the payload with agent name and file metadata
        payload = {
            "agent_name": agent_name,
            "files": files
        }

        # Make an asynchronous HTTP POST request
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()

    except Exception as e:
        logger.error(f"Failed to trigger embeddings generation for {agent_name}: {e}")
        raise ExternalServiceException(detail=f"Failed to trigger embeddings generation for {agent_name}")

# Delete all files of an agent and its directory
def delete_agent_files(agent_name: str) -> None:
    # set the agent dir
    agent_dir = os.path.join(settings.agents_dir, agent_name)

    # Check if the agent directory exists
    if os.path.exists(agent_dir):
        shutil.rmtree(agent_dir)

# Query embeddings from the embeddings server
def query_embeddings(agent_name: str, prompt: str) -> List[Any]:
    try:
        url = f"http://{settings.embeddings_server}:{settings.embeddings_server_port}/query"
        headers = {
            settings.header_name: settings.header_key
        }

        with httpx.Client() as client:
            response = client.post(
                url,
                json={"agent_name": agent_name, "prompt": prompt},
                headers=headers
            )    
        response.raise_for_status()  # Raises an exception for non-2xx responses
        response_json = response.json()
        # Pick the document chunks
        document_chunks = response_json.get('results', [])
        return document_chunks

    except Exception as e:
        raise ExternalServiceException(detail=f"Error querying embeddings for agent {agent_name}: {str(e)}")

# Delete embeddings from the embeddings server
def trigger_embeddings_deletion(agent_name: str) -> None:
    try:
        url = f"http://{settings.embeddings_server}:{settings.embeddings_server_port}/remove"
        headers = {
            settings.header_name: settings.header_key
        }
        with httpx.Client() as client:
            response = client.post(
                url,
                json={"agent_name": agent_name},
                headers=headers
            )    
        response.raise_for_status()  # Raises an exception for non-2xx responses
        return 

    except Exception as e:
        raise ExternalServiceException(detail=f"Error deleting embeddings for agent {agent_name}: {str(e)}")
