"""Deploy the ingestion file to the Databricks workspace.

Usage:
    uv run python deploy.py
"""

import os
import subprocess

from dotenv import load_dotenv

load_dotenv()

LOCAL_PATH = "ingest.py"
REMOTE_PATH = "/Workspace/Shared/google-drive-connector/ingest"
PROFILE = os.environ.get("DATABRICKS_PROFILE", "e2-demo-field-eng")


def deploy():
    subprocess.run(
        ["databricks", "workspace", "mkdirs", os.path.dirname(REMOTE_PATH), "--profile", PROFILE],
        check=True,
    )

    subprocess.run(
        [
            "databricks", "workspace", "import",
            REMOTE_PATH,
            "--file", LOCAL_PATH,
            "--format", "SOURCE",
            "--language", "PYTHON",
            "--overwrite",
            "--profile", PROFILE,
        ],
        check=True,
    )
    print(f"Deployed {LOCAL_PATH} → {REMOTE_PATH}")


if __name__ == "__main__":
    deploy()
