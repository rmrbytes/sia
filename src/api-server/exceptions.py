# exceptions.py

from fastapi import HTTPException
from config import settings

# Base class for custom exceptions to implement common behavior based on settings.debug.
class CustomHTTPException(HTTPException):
    def __init__(self, detail: str, status_code: int):
        # Pre-fill the status_code with 400 (Bad Request) by default
        super().__init__(status_code=status_code, detail=detail)

        # You can add more custom behavior or logging here if needed
        # For example, log every error automatically
        #print(f"Custom Exception Raised: {detail}, Status Code: {status_code}")

# Raised when a database error occurs.
class DatabaseException(CustomHTTPException):
    def __init__(self, detail: str = "Database failed", status_code: int = 500):
        super().__init__(detail=detail, status_code=status_code)


# Raised when authentication or authorization fails.
class AuthenticationException(CustomHTTPException):
    def __init__(self, detail: str = "Authentication failed", status_code: int = 401):
        super().__init__(detail=detail, status_code=status_code)
        print(455, status_code)

# Raised when data validation fails.
class ValidationException(CustomHTTPException):
    def __init__(self, detail: str = "Validation failed", status_code: int = 400):
        super().__init__(detail=detail, status_code=status_code)

# Raised while saving or deleting files in the OS file storage fails.
class FileStorageException(CustomHTTPException):
    def __init__(self, detail: str = "File Storage failed", status_code: int = 502):
        super().__init__(detail=detail, status_code=status_code)

# Raised when an external API or service call fails.
class ExternalServiceException(CustomHTTPException):
    def __init__(self, detail: str = "External Service failed", status_code: int = 502):
        super().__init__(detail=detail, status_code=status_code)

# Raised when a requested resource is not found.
class NotFoundException(CustomHTTPException):
    def __init__(self, detail: str = "Resource not found", status_code: int = 402):
        super().__init__(detail=detail, status_code=status_code)