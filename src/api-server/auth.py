# auth.py

import sqlite3
import bcrypt
from datetime import datetime, timedelta, timezone
from exceptions import DatabaseException, AuthenticationException, ValidationException
from fastapi import Header, Cookie
from starlette.datastructures import Headers
from pydantic import BaseModel
import json
from typing import Dict, Optional, Tuple
from sqlite3 import Connection, Cursor
import jwt

from config import settings
from schema import check_and_migrate_schema

class User(BaseModel):
    id: int
    username: str
    hashed_password: str
    role: str
    status: str
    created_on: int
    updated_on: int

# Helper function to hash a plaintext password
def _hash_password(password: str) -> str:
    # Generate salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# Helper function to check if the entered password matches the hashed password
def _check_password(entered_password: str, stored_hashed_password: str) -> bool:
    # Compare entered password with stored hashed password
    return bcrypt.checkpw(entered_password.encode('utf-8'), stored_hashed_password.encode('utf-8'))

# Get database connection and cursor
def _get_db_connection() -> Tuple[Connection, Cursor]:
    try:
        conn = sqlite3.connect(settings.database_url)
        cursor = conn.cursor()

        # Create users table if it doesn't exist
        _create_table(cursor=cursor)
        # Ensure schema version table exists and apply migrations if needed
        check_and_migrate_schema(cursor)

        return conn, cursor

    except sqlite3.Error as e:
        raise DatabaseException(detail="Error connecting to the database.")

# Create users table if it doesn't exist
def _create_table(cursor: sqlite3.Cursor) -> None:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            hashed_password TEXT,
            role TEXT,
            created_on INTEGER,
            updated_on INTEGER
        )
    ''')

# Function to create an Agent instance from a database row
def create_user_from_row(row: Tuple) -> User:
    (
        _id, name, hashed_password, role, status, created_on, updated_on
    ) = row

    # Create an Agent object
    agent = User(
        id=id,
        name=name,
        hashed_password=hashed_password,
        role=role,
        status=status,
        created_on=created_on,
        updated_on=updated_on
    )

    return agent

# Get user by username
def get_uffser(username: str) -> dict:
    conn, cursor = None, None
    try:
        conn, cursor = _get_db_connection()

        # Retrieve user information from the database
        cursor.execute("SELECT id, username, role, hashed_password FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if not row:
            raise AuthenticationException(detail="No admin user")

        # Return user details as a dictionary
        return create_user_from_row(row)

    except sqlite3.Error as e:
        raise DatabaseException(detail=f"Database error in getting admin: {str(e)}")

    finally:
        if conn:
            conn.close()

# Set admin password if not already set
def set_admin_password(password: str) -> None:
    conn, cursor = None, None
    try:
        conn, cursor = _get_db_connection()

        # Check if admin already exists
        cursor.execute("SELECT COUNT(1) FROM users WHERE username = 'admin'")
        if cursor.fetchone()[0] > 0:
            raise AuthenticationException(detail="Admin already created.")

        # Hash the password and insert the admin user
        hashed_password = _hash_password(password=password)
        now = int(datetime.now().timestamp())

        cursor.execute(
            "INSERT INTO users (username, hashed_password, role, created_on, updated_on) VALUES (?, ?, ?, ?, ?)",
            ("admin", hashed_password, "admin", now, now)
        )
        conn.commit()

    except sqlite3.Error as e:
        raise DatabaseException(detail=f"Database error: {str(e)}")

    finally:
        if conn:
            conn.close()

# Check if the entered admin password is correct
def check_admin_password(password: str) -> None:
    conn, cursor = None, None
    try:
        conn, cursor = _get_db_connection()

        # Get admin info
        cursor.execute("SELECT id, username, role, hashed_password FROM users WHERE username = 'admin'")
        row = cursor.fetchone()
        if not row:
            raise AuthenticationException(detail=f"Admin not yet created")

        # Verify the password
        if not _check_password(entered_password=password, stored_hashed_password=row[3]):
            raise AuthenticationException(detail=f"Passwords don't match")

    except sqlite3.Error as e:
        raise DatabaseException(detail=f"Error checking admin password: {str(e)}")

    finally:
        if conn:
            conn.close()

# Change the admin password after verifying the current one
def change_admin_password(current_password: str, new_password: str) -> None:
    conn, cursor = None, None
    try:
        conn, cursor = _get_db_connection()

        # Get admin info
        cursor.execute("SELECT id, username, role, hashed_password FROM users WHERE username = 'admin'")
        row = cursor.fetchone()
        if not row:
            raise AuthenticationException(detail="No admin user")

        # Verify the current password
        if not _check_password(entered_password=current_password, stored_hashed_password=row[3]):
            raise AuthenticationException(detail="current password wrong")

        # Hash the new password and update the admin user
        new_hashed_password = _hash_password(password=new_password)
        now = int(datetime.now().timestamp())

        cursor.execute(
            "UPDATE users SET hashed_password = ?, updated_on = ? WHERE username = 'admin'",
            (new_hashed_password, now)
        )
        conn.commit()

    except sqlite3.Error as e:
        raise DatabaseException(detail=f"Error changing admin password: {str(e)}")

    finally:
        if conn:
            conn.close()

# Check if the admin password has been set
def is_admin_password_set() -> bool:
    conn, cursor = None, None
    try:
        conn, cursor = _get_db_connection()
        # Check if admin exists
        cursor.execute("SELECT COUNT(1) FROM users WHERE username = 'admin'")
        return cursor.fetchone()[0] > 0

    except sqlite3.Error as e:
        raise DatabaseException(detail=f"Error checking admin password status: {str(e)}")

    finally:
        if conn:
            conn.close()

# Verify the X-API-Key header
def verify_x_api_key(headers: Headers) -> str:

    # Retrieve the API key from headers
    x_api_key = headers.get(settings.header_name)

    # Check if the API key exists
    if x_api_key is None:
        raise ValidationException(detail="X-API-Key is missing in header")

    # Validate the API key
    if x_api_key != settings.header_key:
        raise AuthenticationException(detail="Invalid X-API-Key")

    return x_api_key

# create access token
def create_access_token(data: Dict[str, str]) -> str:
    try:
        # Prepare the token payload
        to_encode = data.copy()
        
        # Add expiration time to the payload
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        
        # Encode the payload into a JWT token
        return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    
    except jwt.PyJWTError as e:  # Catch any JWT-related errors
        raise ValidationException(detail=f"Failed to create access token: {str(e)}")

    except KeyError as e:  # Handle missing settings
        raise ValidationException(detail=f"Missing key: {str(e)}")

    except Exception as e:  # General catch-all for unexpected errors
        raise ValidationException(detail=f"Unexpected error occurred during token creation: {str(e)}")

# verify JWT token and return user
def verify_access_token(access_token: Optional[str] = Cookie(None)) -> None:
    try:

        # Check if the access token is present
        if access_token is None:
            raise AuthenticationException(detail="Access token is missing in cookies", status_code=403)

        # Decode the JWT token
        payload = jwt.decode(access_token, settings.secret_key, algorithms=[settings.algorithm])

        # Extract the username from the token payload
        username = payload.get("sub")
        if username is None or username != 'admin':
            raise AuthenticationException(detail=f"Invalid user detected in token payload: {username}")

        # If everything is fine, just return
        return

    except jwt.ExpiredSignatureError as e:
        # Handle token expiration
        raise AuthenticationException(detail=f"Token has expired: {str(e)}")

    except jwt.InvalidTokenError as e:
        # Handle invalid token
        raise AuthenticationException(detail=f"Invalid token: {str(e)}")
