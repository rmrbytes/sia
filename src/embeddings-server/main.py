from fastapi import FastAPI, HTTPException, Request, Response, Body
from starlette.datastructures import Headers
from typing import List, Optional
import os
import httpx
import asyncio
from typing import Optional, Dict, Any
from config import settings
from chunker import chunk_files_in_dir
from retriever import get_chunks

# Initialize FastAPI
app = FastAPI()

# Helper function to notify app server
async def notify_api_server(agent_name: str) -> None:
    # set the url and headers
    url = f"http://{settings.api_server}:{settings.api_server_port}/api/agents/{agent_name}/update-embeddings-status"
    headers = {settings.header_name: settings.header_key}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url=url, data=None, headers=headers)
            if response.status_code == 200:
                print(f"Successfully notified app-server for agent {agent_name}")
            else:
                print(f"Failed to notify app-server: {response.status_code}")
    except Exception as e:
        print(f"Error notifying app server: {str(e)}")

# To verify api key when called from api-server
def verify_x_api_key(headers: Headers) -> str:
    x_api_key: Optional[str] = headers.get(settings.header_name)
    if x_api_key is None:
        raise HTTPException(status_code=400, detail="X-API-Key header missing")
    if x_api_key != settings.header_key:
        raise HTTPException(status_code=401, detail="Invalid X-API-Key")
    return x_api_key

# define embedding model_path 
embedding_model_path = os.path.join(settings.models_dir, settings.embedding_model_name)

# 1. Route to generate chunks and save them in the vector store
@app.post("/generate")
async def generate(
    request: Request, 
    response: Response,
    body: Dict[str, Any] = Body(...)
    ) -> Dict[str, str]:

    # verify request is from api-server
    verify_x_api_key(headers=request.headers)
    
    # set agent dir
    agent_name: str = body.get("agent_name")
    agent_dir: str = os.path.join(settings.agents_dir, agent_name)

    # check dir existance
    if not os.path.exists(agent_dir):
        raise HTTPException(status_code=404, detail="Agent directory not found")

    # get files 
    files = body.get("files")

    chunk_files_in_dir(agent_name, agent_dir, embedding_model_path, settings.store_dir, files)    
 
    # notify api server
    asyncio.create_task(notify_api_server(agent_name=agent_name))

    response.status_code = 204
    # return response with cookie and no data
    return response

# 2. Route to query the vector store based on input query and agent
@app.post("/query")
async def query(
    request: Request,
    agent_name: str = Body(...), 
    prompt: str  = Body(...)
    ):

    # verify headers
    verify_x_api_key(headers=request.headers)

    # initialize Query Handler
    chunks = get_chunks(agent_name, prompt, embedding_model_path, settings.store_dir)
    
    return {
            "status": "success",
            "agent_name": agent_name,
            "prompt": prompt,
            "results": chunks
    }

@app.get("/health")
async def health_check():
    return {"status": "OK"}