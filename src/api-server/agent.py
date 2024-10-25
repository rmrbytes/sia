from datetime import datetime
import sqlite3
from sqlite3 import Connection, Cursor
from pydantic import BaseModel, field_validator, model_validator
from typing import List, Dict, Tuple, Any, Optional
#from dataclasses import dataclass, field, asdict
import json

from exceptions import DatabaseException
from config import settings
from schema import check_and_migrate_schema

# Define a dataclass for the metadata
class Meta (BaseModel):
    split_by: Optional[str] = settings.split_by
    split_length: Optional[int] = settings.split_length
    split_overlap: Optional[int] = settings.split_overlap
    split_threshold: Optional[int] = settings.split_threshold

    @model_validator(mode='before')
    def set_defaults_for_empty_values(cls, values):
        if values.get('split_by') == "":
            values['split_by'] = settings.split_by
        if values.get('split_length') in (None, 0, ""):
            values['split_length'] = settings.split_length
        if values.get('split_overlap') in (None, 0, ""):
            values['split_overlap'] = settings.split_overlap
        if values.get('split_threshold') in (None, 0, ""):
            values['split_threshold'] = settings.split_threshold
        return values

# Define a dataclass for each file, which includes filename and the metadata
class FileDetail (BaseModel):
    filename: str
    meta: Optional[Meta] = None

# Define the main Agent dataclass
class Agent (BaseModel):
    id: Optional[int] = None  # If this is assigned automatically, keep it optional
    name: str = ""
    instructions: Optional[str] = None
    welcome_message: Optional[str] = None
    suggested_prompts: Optional[List[str]] = None
    deleted_files: Optional[List[str]] = None
    files: Optional[List[FileDetail]] = None
    settings: Optional[Dict[str, Optional[str]]] = None
    status: Optional[str] = None
    embeddings_status: Optional[str] = None
    created_on: Optional[int] = None
    updated_on: Optional[int] = None

    @field_validator("suggested_prompts")
    def limit_suggested_prompts(cls, v):
        if v is not None and len(v) > 3:
            return v[:3]  # Truncate to only the first 3 items
        return v

# Get a database connection and cursor. Ensures the agents table is created if it does not exist.
def _get_db_connection() -> Tuple[Connection, Cursor]:
    try:
        conn = sqlite3.connect(settings.database_url)
        cursor = conn.cursor()
        # create agent table if necessary
        _create_tables(cursor=cursor)
        # Ensure schema version table exists and apply migrations if needed
        check_and_migrate_schema(cursor)
        return conn, cursor
    except sqlite3.Error as e:
        raise DatabaseException(detail=f"Database connection error: {str(e)}")

# Function to create an Agent instance from a database row
def create_agent_from_row(row: Tuple) -> Agent:
    (
        _id, name, instructions, welcome_message, suggested_prompts_str,
        files_str, settings_str, status, embeddings_status, created_on, updated_on
    ) = row

    # Deserialize JSON fields
    settings = json.loads(settings_str) if settings_str else {}
    suggested_prompts = json.loads(suggested_prompts_str) if suggested_prompts_str else []
    files_data = json.loads(files_str) if files_str else []
    # Convert the deserialized files data to FileDetail objects
    files = [FileDetail(**file_data) for file_data in files_data]
    # Create an Agent object
    agent = Agent(
        id=_id,
        name=name,
        instructions=instructions,
        welcome_message=welcome_message,
        suggested_prompts=suggested_prompts,
        files=files,
        settings=settings,
        status=status,
        embeddings_status=embeddings_status,
        created_on=created_on,
        updated_on=updated_on
    )
    return agent

# Create the agents and file metadata tables if they do not exist.
def _create_tables(cursor: Cursor) -> None:
    # Create agents table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS agents (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            instructions TEXT,
            welcome_message TEXT,
            suggested_prompts TEXT,
            files TEXT,
            settings TEXT,
            status TEXT,
            embeddings_status TEXT,
            created_on INTEGER,
            updated_on INTEGER
        )
        """
    )

# get all agents with file count
def get_agents() -> List[Agent]:
    conn, cursor = None, None
    try:
        conn, cursor = _get_db_connection()
        cursor.execute("SELECT * FROM agents ORDER BY created_on")
        rows = cursor.fetchall()
        agents = [create_agent_from_row(row) for row in rows]
        return agents

    except sqlite3.Error as e:
        raise DatabaseException(detail=f"Error when getting agents: {str(e)}") from e
    finally:
        if conn:
            conn.close()

# insert a new agent record
def save_agent(agent: Agent) -> Agent:
    conn, cursor = None, None
    try:
        conn, cursor = _get_db_connection()
        # Check if an agent with the same name already exists
        cursor.execute("SELECT COUNT(1) FROM agents WHERE name = ?", (agent.name,))
        if cursor.fetchone()[0] > 0:
            raise DatabaseException(detail=f"Agent: {agent.name} already exists")

        # get current time as an int
        now = int(datetime.now().timestamp())
        # convert agent to dict
        agent_dict = agent.model_dump()
        # Insert a new agent
        cursor.execute(
            """
            INSERT INTO agents (name, instructions, welcome_message, suggested_prompts, files, embeddings_status, created_on, updated_on)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (agent.name, agent.instructions, agent.welcome_message, json.dumps(agent.suggested_prompts), json.dumps(agent_dict['files']), agent.embeddings_status, now, now,)
        )
        conn.commit()
        # Retrieve the newly inserted agent data
        cursor.execute("SELECT * FROM agents WHERE name = ?", (agent.name,))
        row = cursor.fetchone()
        if row:
            return create_agent_from_row(row)
        else:
            raise DatabaseException(
                detail="Agent could not be retrieved after inserting"
            )
    except sqlite3.Error as e:
        raise DatabaseException(detail=f"Agent could not be inserted: {str(e)}")
    finally:
        if conn:
            conn.close()

# update an agent record, including managing file metadata
def change_agent(agent: Agent):
    conn, cursor = None, None
    try:
        conn, cursor = _get_db_connection()

        # Ensure the agent exists
        cursor.execute("SELECT * FROM agents WHERE name = ?", (agent.name,))
        if not cursor.fetchone():
            raise DatabaseException(detail=f"Agent: ${agent.name} not found")

        # time in int
        now = int(datetime.now().timestamp())

        # convert agent to dict
        agent_dict = agent.model_dump()

        # Update the agent's fields except for `name` and `created_on`
        cursor.execute(
            """
            UPDATE agents
            SET instructions = COALESCE(?, instructions),
                welcome_message = COALESCE(?, welcome_message),
                suggested_prompts = COALESCE(?, suggested_prompts),
                files = COALESCE(?, files),
                embeddings_status = COALESCE(?, embeddings_status),
                updated_on = ?
            WHERE name = ?
            """,
            (agent.instructions, agent.welcome_message, json.dumps(agent.suggested_prompts), json.dumps(agent_dict['files']), agent.embeddings_status, now, agent.name,)
        )

        conn.commit()

        # Fetch the updated agent record
        cursor.execute("SELECT * FROM agents WHERE name = ?", (agent.name,))
        row = cursor.fetchone()
        if row:
            return create_agent_from_row(row)
        else:
            raise DatabaseException(detail="Agent updated could not be retrieved")
    except sqlite3.Error as e:
        raise DatabaseException(detail=f"Error in updating agent {agent.name}: {str(e)}")
    finally:
        if conn:
            conn.close()

# delete agent and associated file metadata
def delete_agent(name: str) -> None:
    conn, cursor = None, None
    try:
        conn, cursor = _get_db_connection()

        # Ensure the agent exists
        cursor.execute("SELECT * FROM agents WHERE name = ?", (name,))
        if not cursor.fetchone():
            raise DatabaseException(detail=f"Agent: ${name} not found")

        # Delete the agent
        cursor.execute("DELETE FROM agents WHERE name = ?", (name,))

        conn.commit()

    except sqlite3.Error as e:
        raise DatabaseException(detail=f"Error in deleting agent {name}: {str(e)}")
    finally:
        if conn:
            conn.close()

# Get agent details along with associated file metadata
def get_agent(name: str) -> Agent:
    conn, cursor = None, None
    try:
        conn, cursor = _get_db_connection()
        # Fetch agent details
        cursor.execute("SELECT * FROM agents WHERE name = ?", (name,))
        row = cursor.fetchone()
        if not row:
            raise DatabaseException(detail=f"Agent {name} not found")
        return create_agent_from_row(row)
    except sqlite3.Error as e:
        raise DatabaseException(detail=f"Error in retrieving agent: {name}: {str(e)}")
    finally:
        if conn:
            conn.close()


# update embedding_status
def update_agent_embeddings_status(name: str, embeddings_status: str = "") -> None:
    conn, cursor = None, None
    try:
        conn, cursor = _get_db_connection()

        # Ensure the agent exists
        cursor.execute("SELECT * FROM agents WHERE name = ?", (name,))
        if not cursor.fetchone():
            raise DatabaseException(
                detail=f"Agent: ${name} not found in update embeddings status"
            )

        updated_on = int(datetime.now().timestamp())

        # Update the agent's fields except for `name` and `created_on`
        cursor.execute(
            """
            UPDATE agents
            SET embeddings_status = ?,
                updated_on = ?
            WHERE name = ?
            """,
            (embeddings_status, updated_on, name),
        )
        conn.commit()
    except sqlite3.Error as e:
        raise DatabaseException(detail=f"Error in updating agent: {name}: {str(e)}")
    finally:
        if conn:
            conn.close()
