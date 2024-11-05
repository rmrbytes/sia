# agent_routes.py

from typing import Dict, Any, List, Optional, Union
from fastapi import APIRouter, Request, Response, Form, File, UploadFile, HTTPException
import asyncio
import json
import os
from auth import verify_x_api_key, verify_access_token

from pydantic import BaseModel
import json

from agent import (
    Agent,
    FileDetail,
    Meta,
    save_agent,
    change_agent,
    delete_agent,
    get_agents,
    get_agent,
    update_agent_embeddings_status,
)
from utils import (
    sanitize_agent_name,
    process_uploaded_files,
    trigger_embeddings_generation,
    delete_agent_files,
    trigger_embeddings_deletion
)

from config import settings

agent_router = APIRouter()


# Route to fetch all agents
@agent_router.get("/")
def route_agents(request: Request):
    try:
        # verify API Key
        verify_x_api_key(headers=request.headers)
        # verify token
        access_token = request.cookies.get("access_token")
        verify_access_token(access_token=access_token)

        # fetch agents and return
        agents = get_agents()
        return agents

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(detail=f"Unable to get agents: {str(e)}", status_code=500)


# Route to create agent and upload optional files
@agent_router.post("/")
async def route_save_agent(
    request: Request,
    name: str = Form(...),
    instructions: str = Form(None),
    welcome_message: str = Form(None),
    suggested_prompts: List[str] = Form(None),
    deleted_files: List[str] = Form(None),
    files: str = Form(None),
    new_files: List[Union[UploadFile, None]] = File(None),
):
    try:
        # Log incoming request data to see what's actually coming in
        # Verify API Key and JWT Token
        verify_x_api_key(headers=request.headers)
        access_token = request.cookies.get("access_token")
        verify_access_token(access_token=access_token)

        # Check for agent name
        if not name:
            raise HTTPException(status_code=400, detail="Agent name is missing")

        # Sanitize the name
        sanitized_name = sanitize_agent_name(name)

        # Parse the files JSON string into a list of dictionaries
        files_list = json.loads(files)
        # Convert the list of dictionaries into a list of FileDetail objects
        files_data = [FileDetail(**file) for file in files_list]

        # create agent object
        agent = Agent(
            name=sanitized_name,
            instructions=instructions,
            welcome_message=welcome_message,
            suggested_prompts=suggested_prompts,
            files=files_data,
        )

        # Process and save files to agent directory
        process_uploaded_files(agent_name=sanitized_name, new_files=new_files)

        # set embedding status
        embeddings_status = ""
        # Trigger embeddings generation if files are added
        if new_files:
            if agent.files:
                # Convert each FileDetail instance to a dictionary
                files_dict_list = [file.model_dump() for file in agent.files]
            else:
                files_dict_list = []
            asyncio.create_task(trigger_embeddings_generation(agent_name=agent.name, files=files_dict_list))
            embeddings_status = "I"
        # update embedding_status in agent
        agent.embeddings_status = embeddings_status
        # Save agent data
        agent = save_agent(agent)
        # return to client
        return agent

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(detail=f"Unable to create agent: {str(e)}", status_code=500)


# Route to update an agent, handling both field updates and file uploads
@agent_router.put("/{agent_name}")
async def route_update_agent(
    request: Request,
    agent_name: str,
    name: str = Form(...),
    instructions: str = Form(None),
    welcome_message: str = Form(None),
    suggested_prompts: List[str] = Form(None),
    deleted_files: List[str] = Form(None),
    files: str = Form(None),
    new_files: List[Union[UploadFile, None]] = File(None),
):
    try:
        # Verify API Key and JWT Token
        access_token = request.cookies.get("access_token")
        verify_access_token(access_token=access_token)

        # Check for agent name
        if not name:
            raise HTTPException(status_code=400, detail="Agent name is missing")

        if name != agent_name:
            raise HTTPException(
                status_code=400,
                detail="Agent name in agent_details does not match the agent_name in the path",
            )

        # get the existing agent info
        existing_agent = get_agent(agent_name)
        if files and files.strip() not in ["", "null"]:
            # Parse the files JSON string into a list of dictionaries
            files_list = json.loads(files) 
            # Convert the list of dictionaries into a list of FileDetail objects
            files_data = [FileDetail(**file) for file in files_list]
        else:
            files_data = []

        # create agent object
        agent = Agent(
            name=name,
            instructions=instructions,
            welcome_message=welcome_message,
            suggested_prompts=suggested_prompts,
            deleted_files=deleted_files,
            files=files_data,
        )
        # Process uploaded files
        if new_files or agent.deleted_files:
            process_uploaded_files(
                agent_name=agent_name,
                new_files=new_files,
                deleted_files=agent.deleted_files,
            )

        # Remove FileDetail objects from existing_agent.files if filename matches deleted_files
        if agent.deleted_files:
            existing_agent.files = [
                file
                for file in existing_agent.files
                if file.filename not in agent.deleted_files
            ]
        # Append existing agent.files to agent.files
        agent.files = existing_agent.files + agent.files

        embeddings_status = ""
        # Trigger embeddings generation if files were modified
        if new_files or agent.deleted_files:
            # Check if files exist in the agent instance
            if agent.files:
                # Convert each FileDetail instance to a dictionary
                files_dict_list = [file.model_dump() for file in agent.files]
            else:
                files_dict_list = []
            asyncio.create_task(trigger_embeddings_generation(agent_name=agent.name, files=files_dict_list))
            embeddings_status = "I"

        # update embeddings_status
        agent.embeddings_status = embeddings_status
        # Update agent in the database
        agent = change_agent(agent)
        return agent

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            detail=f"Unable to update agent {agent_name}: {str(e)}", status_code=500
        )


# Route to fetch a specific agent by name
@agent_router.get("/{agent_name}")
def route_get_agent(agent_name: str, request: Request):
    try:
        # Verify API Key and JWT Token
        access_token = request.cookies.get("access_token")
        verify_access_token(access_token=access_token)

        # Ensure agent_name is provided
        if not agent_name:
            raise HTTPException(status_code=400, detail="Agent name cannot be blank")
        # Get agent details
        agent = get_agent(agent_name)
        return agent

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            detail=f"Unable to retrieve agent {agent_name}: {str(e)}", status_code=500
        )


# Route to delete an agent by name, along with its associated files
@agent_router.delete("/{agent_name}")
def route_delete_agent(request: Request, response: Response, agent_name: str) -> None:
    try:
        # Verify API Key and JWT Token
        verify_x_api_key(headers=request.headers)
        access_token = request.cookies.get("access_token")
        verify_access_token(access_token=access_token)

        # Delete agent files
        delete_agent_files(agent_name=agent_name)

        # Delete agent from the database
        delete_agent(name=agent_name)

        # Delete embeddings from embeddings-server
        trigger_embeddings_deletion(agent_name)
        response.status_code = 204
        return response

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            detail=f"Unable to delete agent {agent_name}: {str(e)}", status_code=500
        )


# Route to update embeddings status of an agent
@agent_router.post("/{agent_name}/update-embeddings-status")
def route_update_embeddings_status(agent_name: str, request: Request) -> Dict[str, str]:
    try:
        # Verify API Key which has been set in embeddings-server
        verify_x_api_key(headers=request.headers)

        # Check if agent_name is provided
        if not agent_name:
            raise HTTPException(status_code=400, detail="Agent name missing")

        # Update embeddings status
        update_agent_embeddings_status(name=agent_name, embeddings_status="")
        return {"message": "Embeddings status updated successfully"}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            detail=f"Unable to update embeddings_status in {agent_name}: {str(e)}",
            status_code=500,
        )
