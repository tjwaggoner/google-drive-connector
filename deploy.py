"""Deploy the ingestion file to the Databricks workspace.

Usage:
    uv run python deploy.py
"""

import os
import subprocess

from dotenv import load_dotenv

load_dotenv()

LOCAL_PATH = "ingest.py"
PROFILE = os.environ.get("DATABRICKS_PROFILE", "e2-demo-field-eng")


def get_current_user():
    result = subprocess.run(
        ["databricks", "current-user", "me", "--profile", PROFILE, "-o", "json"],
        check=True, capture_output=True, text=True,
    )
    import json
    return json.loads(result.stdout)["userName"]


def deploy():
    username = get_current_user()
    remote_path = f"/Workspace/Users/{username}/google-drive-connector/ingest"

    subprocess.run(
        ["databricks", "workspace", "mkdirs", os.path.dirname(remote_path), "--profile", PROFILE],
        check=True,
    )

    subprocess.run(
        [
            "databricks", "workspace", "import",
            remote_path,
            "--file", LOCAL_PATH,
            "--format", "SOURCE",
            "--language", "PYTHON",
            "--overwrite",
            "--profile", PROFILE,
        ],
        check=True,
    )
    print(f"Deployed {LOCAL_PATH} → {remote_path}")


if __name__ == "__main__":
    deploy()
