"""Create the Google Drive connection in Unity Catalog.

This is a one-time setup step that must run before deploying the DABs bundle.
The connection cannot be created via DABs — it requires the Databricks SDK.

Usage:
    uv run python src/setup/create_connection.py
"""

import os

from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv

load_dotenv()


def create_google_drive_connection():
    w = WorkspaceClient(
        host=os.environ["DATABRICKS_HOST"],
        token=os.environ["DATABRICKS_TOKEN"],
    )

    connection_name = os.environ.get("CONNECTION_NAME", "google_drive_connection")

    # Check if connection already exists
    for conn in w.connections.list():
        if conn.name == connection_name:
            print(f"Connection '{connection_name}' already exists (id={conn.connection_id})")
            return conn

    conn = w.connections.create(
        name=connection_name,
        connection_type="GOOGLE_DRIVE",  # Requires DBR 17.3+
        options={
            "client_id": os.environ["GOOGLE_CLIENT_ID"],
            "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
        },
    )
    print(f"Created connection '{connection_name}' (id={conn.connection_id})")
    return conn


if __name__ == "__main__":
    create_google_drive_connection()
