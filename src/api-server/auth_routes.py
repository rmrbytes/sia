# auth_routes.py

from fastapi import APIRouter, Request, Response, Body, HTTPException
from typing import Dict, Any
from auth import (
    is_admin_password_set,
    set_admin_password,
    check_admin_password,
    change_admin_password,
    create_access_token,
    verify_x_api_key,
    verify_access_token
)
from config import settings

# Create router
auth_router = APIRouter()

# Check if admin password is set
@auth_router.get("/is-admin-password-set")
async def route_check_admin_password_set(request: Request) -> bool:
    try:
        # Verify X-API-Key header
        verify_x_api_key(headers=request.headers)
        # check whether password has been set
        res = is_admin_password_set()
        # return true or false
        return res
    
    except HTTPException as e:
        raise e
    except Exception as e:
        # Unexpected errors, wrap them in an HttpException with status 500
        raise HTTPException(detail=str(e), status_code=500)


# Check if token is valid
@auth_router.get("/check-token")
def route_check_jwt_token(request: Request, response: Response) -> None:
    try:
        # Verify X-API-Key header
        verify_x_api_key(headers=request.headers)

        # Verify JWT token
        access_token = request.cookies.get("access_token")
        verify_access_token(access_token=access_token)

        response.status_code = 204
        # return response with no data
        return response

    except HTTPException as e:
        raise e
    except Exception as e:
         raise HTTPException(detail=str(e), status_code=500)


# Admin login route
@auth_router.post("/login")
def route_login(request: Request, response: Response, body: Dict[str, Any] = Body(...)) -> None:
    try:
        # Verify X-API-Key header
        verify_x_api_key(headers=request.headers)

        # Extract password from request body
        password = body.get("password", "")
        if not password:
            raise HTTPException(status_code=400, detail="Password cannot be blank")

        # Check the admin password
        check_admin_password(password=password)

        # Generate access token and refresh token
        access_token = create_access_token(data={"sub": "admin"})

        # Set access token in cookies
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=settings.access_token_expire_minutes * 60,
            expires=settings.access_token_expire_minutes * 60,
            secure=settings.is_https,
            samesite="lax",
        )
        response.status_code = 204
        # return response with cookie and no data
        return response

    except HTTPException as e:
        raise e
    except Exception as e:
         raise HTTPException(detail=str(e), status_code=500)

# Route to logout
@auth_router.post("/logout")
def route_logout(response: Response) -> None:
    response.set_cookie(
        key="access_token",
        value="",
        httponly=True,
        expires=0,
        max_age=0,
    )
    response.status_code = 204
    # return response with cookie and no data
    return response


# Set admin password route
@auth_router.post("/set-admin-password")
def route_set_admin_password(request: Request, response: Response, body: Dict[str, Any] = Body(...)) -> None:
    try:
        # Verify X-API-Key header
        verify_x_api_key(headers=request.headers)

        # Extract password from request body
        password = body.get("password", "")
        # check length
        if len(password) < 6:
            raise HTTPException(status_code=400, detail="Min password length is 6 chars")

        # Set the admin password
        set_admin_password(password=password)
        
        response.status_code = 204
        # return response with no data
        return response

    except HTTPException as e:
        raise e
    except Exception as e:
         raise HTTPException(detail=str(e), status_code=500)


# Change admin password route
@auth_router.post("/change-admin-password")
def route_change_admin_password(request: Request, response: Response, body: Dict[str, Any] = Body(...)) -> None:
    try:
        # Verify X-API-Key header
        verify_x_api_key(headers=request.headers)

        # Verify JWT token
        access_token = request.cookies.get("access_token")
        verify_access_token(access_token=access_token)

        # Extract current and new password from request body
        current_password = body.get("current_password", "")
        new_password = body.get("new_password", "")
        
        if len(new_password) < 6:
            raise HTTPException(status_code=400, detail="Min password length is 6 chars")

        # Change admin password
        change_admin_password(current_password=current_password, new_password=new_password)
        

        response.status_code = 204
        # return response with no data
        return response

    except HTTPException as e:
            raise e
    except Exception as e:
         raise HTTPException(detail=str(e), status_code=500)
