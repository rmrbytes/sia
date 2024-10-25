# main.py

from fastapi import FastAPI, Request
from fastapi import HTTPException as FastAPIHttpException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

# Import routes and dependencies
from auth_routes import auth_router
from agent_routes import agent_router
from chat_routes import chat_router
from exceptions import (
    DatabaseException,
    AuthenticationException,
    ValidationException,
    ExternalServiceException,
    FileStorageException,
    NotFoundException
)
from config import settings
from utils import logger

# Initialize the FastAPI app
app = FastAPI()

# Middleware for CORS handling (if needed)
# Uncomment and configure based on your use case
#app.add_middleware(
#    CORSMiddleware,
#     allow_origins=["*"],  # Adjust the origins for your environment
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.get("/health")
async def health_check():
    return {"status": "OK"}

# Include the routers for modular routes
app.include_router(router=auth_router, prefix="/api/auth")
app.include_router(router=agent_router, prefix="/api/agents")
app.include_router(router=chat_router, prefix="/api/chat")

# Handle 404 Not Found Errors
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    # Log the 404 error
    detail = "Path not found" if not settings.debug else f"Path {request.url.path} does not exist"
    logger.error(f"404 error: {detail}")
    return JSONResponse(status_code=404, content={"detail": detail})


# Global exception handler for all unhandled exceptions
@app.exception_handler(FastAPIHttpException)
async def custom_exception_handler(request: Request, exc: FastAPIHttpException):
    exception_map = {
        DatabaseException: ("A database error occurred.", "Database error"),
        AuthenticationException: ("Authentication failed.", "Authentication error"),
        ValidationException: ("Invalid request.", "Validation error"),
        FileStorageException: ("File Storage Failed", "File Storage error"),
        ExternalServiceException: ("Error communicating with external service.", "External service error"),
        NotFoundException: ("Resource not found.", "Not found error"),
    }
    for exception_type, (generic_message, log_message) in exception_map.items():
        if isinstance(exc, exception_type):
            detail = exc.detail if settings.debug else generic_message
            logger.error(f"{log_message}: {exc.detail}")
            return JSONResponse(status_code=exc.status_code, content={"detail": detail})

    # Handle all other exceptions
    detail = "An unexpected error occurred." if not settings.debug else str(exc)
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(status_code=500, content={"detail": detail})
