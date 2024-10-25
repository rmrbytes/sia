# chat.py

import httpx
from config import settings
from fastapi import HTTPException
from exceptions import ExternalServiceException

# Helper function to compose the LLM request
def compose_request(instruction, document_chunks, history, user_prompt):
    """
    Combines the instruction, document chunks, history, and user prompt into a complete prompt
    for an LLM (vLLM, Ollama, or OpenAI-compatible API).
    
    :param instruction: The main system instruction to the LLM (e.g., "You are a Teacher...").
    :param document_chunks: A list of document chunks relevant to the conversation.
    :param history: A list of past user prompts and system responses (as a list of dictionaries).
    :param user_prompt: The latest user input or question.
    
    :return: A formatted list of messages to be used for LLM completion API.
    """
    try:
        # Start with the instruction as the system message
        messages = [
            {"role": "system", "content": instruction}
        ]
        # Add the past history of user prompts and system responses
        for entry in history:
            if "user" in entry:
                messages.append({"role": "user", "content": entry["user"]})
            if "assistant" in entry:
                messages.append({"role": "assistant", "content": entry["assistant"]})
            if "system" in entry:
                messages.append({"role": "system", "content": entry["system"]})
        rag_prompt = ""    
        # Add document chunks as a system message (summarizing or presenting document context)
        if document_chunks:
            rag_prompt += "Using the information below answer the given query:\n"
            chunked_documents = "\n\n".join(document_chunks)
            rag_prompt += chunked_documents
        rag_prompt += '\nQuery: '
        rag_prompt += user_prompt
        # Add the latest user prompt
        messages.append({"role": "user", "content": rag_prompt})
        return messages
    except Exception as e:
         raise HTTPException(detail=f"Unable to compose request", status_code=500)

# Helper function to map response length to max_tokens
def get_max_tokens_by_length(response_length: str) -> int:
    length_map = {
        "s": settings.chat_response_length_short, 
        "m": settings.chat_response_length_medium,
        "l": settings.chat_response_length_long
    }
    return length_map.get(str(response_length).lower(), settings.chat_response_length_medium)  # Default to medium if not provided

# Helper function to call the vllm server
def send_prompt_vllm(
    messages: list,
    response_length: str = settings.chat_response_length_default,  # short, medium, long
    temperature: float = settings.chat_temperature, # controls the randomness or creativity of token selection by adjusting the overall probability distribution.
    top_p: float = settings.chat_top_p, # limits the range of tokens the model can choose from by cutting off low-probability tokens.
    frequency_penalty: float = settings.chat_frequency_penalty, # It reduces the likelihood of tokens (words or phrases) being repeated based on how frequently they have already appeared in the generated text. Range is -2 to 2.
    presence_penalty: float = settings.chat_presence_penalty #  It reduces the likelihood of tokens (words or phrases) being repeated based on whether they have appeared at all in the generated text so far, without considering their frequency. This encourages the model to introduce new topics or words into the conversation. Range is -2 to 2
    ):
    try:
        max_tokens = get_max_tokens_by_length(response_length)

        # Call the vLLM API using requests
        url = f"http://{settings.llm_server}:{settings.llm_server_port}/v1/chat/completions"
        with httpx.Client(timeout=600) as client:
            response = client.post(
                url,
                json={
                    "model": settings.llm_model_name,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "top_p": top_p,
                    "frequency_penalty": frequency_penalty,
                    "presence_penalty": presence_penalty
                }
            )
        response.raise_for_status()
        response.raise_for_status()
        response_data = response.json()
        choices = response_data['choices']
        choice = choices[0]
        message = choice['message']
        resp_json = {
            "content": message['content'],
            "role": message['role']
        }
        return resp_json
        
    except Exception as e:
        raise  ExternalServiceException(detail=f"Error connecting to LLM Server: {str(e)}")
    

