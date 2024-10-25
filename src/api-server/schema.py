import sqlite3

# Define the current version of the schema
CURRENT_SCHEMA_VERSION = 3  # Update this constant whenever there's a schema change

# Function to create the schema_version table if it doesn't exist
def _create_schema_version_table(cursor: sqlite3.Cursor) -> None:
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_version (
            version INTEGER PRIMARY KEY
        )
        """
    )
    # Insert initial version if it's a new database
    cursor.execute("INSERT OR IGNORE INTO schema_version (version) VALUES (1)")

# Function to check the current schema version and apply migrations as needed
def check_and_migrate_schema(cursor: sqlite3.Cursor) -> None:
    _create_schema_version_table(cursor)  # Ensure the schema_version table exists
    # Retrieve the current schema version from the database
    cursor.execute("SELECT version FROM schema_version")
    current_version = cursor.fetchone()[0]
    # List of migrations; each function contains logic to update the schema to the next version
    migrations = [
        _migration_1_to_2,  # Migration from version 1 to 2
        _migration_2_to_3,  # Migration from version 2 to 3
    ]
    # Apply migrations sequentially if the current version is less than the target version
    '''
    while current_version < CURRENT_SCHEMA_VERSION:
        migrations[current_version - 1](cursor)  # Apply the corresponding migration
        current_version += 1
        cursor.execute("UPDATE schema_version SET version = ?", (current_version,))
    '''

# Example Migration Functions
def _migration_1_to_2(cursor: sqlite3.Cursor) -> None:
    # Example migration to add a new column to the agents table
    #cursor.execute("ALTER TABLE agents ADD COLUMN description TEXT DEFAULT ''")
    print("Migrated schema from version 1 to 2")

def _migration_2_to_3(cursor: sqlite3.Cursor) -> None:
    # Example migration to add an index to the agents table
    #cursor.execute("CREATE INDEX IF NOT EXISTS idx_agents_name ON agents (name)")
    print("Migrated schema from version 2 to 3")

