# chat_routes.py

from fastapi import APIRouter, Request, Body, HTTPException
from typing import Dict, Any
from auth import verify_x_api_key
from agent import get_agent
from chat import compose_request, send_prompt_vllm
from utils import query_embeddings
from config import settings
from agent import Agent

# Create an API Router for chat-related routes
chat_router = APIRouter()

# To get agent details
@chat_router.get("/{agent_name}")
def route_get_agent(agent_name: str, request: Request) -> Dict[str, Any]:
    try:
        verify_x_api_key(headers=request.headers)

        if not agent_name:
            raise HTTPException(status_code=400, detail="Agent name cannot be blank")

        # Get agent details
        agent: Agent = get_agent(agent_name)

        # Extract required information only
        chat_agent_info = {
            "name": agent.name,
            "welcome_message": agent.welcome_message,
            "suggested_prompts": agent.suggested_prompts
        }
        return {"agent": chat_agent_info}

    except HTTPException as e:
        raise e
    except Exception as e:
         raise HTTPException(detail=f"Unable to get agent {agent_name} in chat: {str(e)}", status_code=500)


# to generate user prompt to get LLM response
@chat_router.post("/{agent_name}")
def route_post_chat(agent_name: str, request: Request, body: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    try:
        verify_x_api_key(headers=request.headers)
        if not agent_name:
            raise HTTPException(status_code=400, detail="Agent name cannot be blank")
        # Get input details
        agent: Agent = get_agent(agent_name)
        prompt: str = body.get("prompt", "")
        messages: Dict[str, Any] = body.get("messages")
        response_length: str = body.get("response_length", settings.chat_response_length_default)
        # Get document text array via embeddings query
        document_chunks = query_embeddings(agent_name=agent_name, prompt=prompt)
        # Compose request to be sent to LLM
        messages = compose_request(
            instruction=agent.instructions, 
            document_chunks=document_chunks, 
            history=messages, 
            user_prompt=prompt
        )
        # Send request to the LLM server
        #llm_response = send_prompt_vllm(messages=messages, response_length=response_length)

        #return {"content": llm_response["content"], "role": llm_response["role"]}
        return {"content": document_chunks[0], "role": "assistant"}

    except HTTPException as e:
        raise e
    except Exception as e:
         raise HTTPException(detail=f"Unable to post chat request {agent_name}: {str(e)}", status_code=500)