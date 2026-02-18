# Google Drive Connector for Databricks

Ingest files from Google Drive into Unity Catalog using a Databricks Asset Bundle.

## Prerequisites

- [Databricks CLI](https://docs.databricks.com/dev-tools/cli/install.html) v0.280+
- [uv](https://docs.astral.sh/uv/) for Python dependency management
- A Databricks workspace with DBR 17.3+ (required for Google Drive connections)
- Google Cloud OAuth credentials (client ID + secret) with Drive API enabled

## Setup

1. Clone and install dependencies:
   ```bash
   git clone git@github.com:tjwaggoner/google-drive-connector.git
   cd google-drive-connector
   uv sync
   ```

2. Copy the environment template and fill in your values:
   ```bash
   cp .env.example .env
   # Edit .env with your Databricks host, token, and Google OAuth credentials
   ```

3. Create the Google Drive connection in Unity Catalog (one-time):
   ```bash
   uv run python src/setup/create_connection.py
   ```

4. Deploy the ingestion job with DABs:
   ```bash
   databricks bundle deploy -t dev
   ```

5. Run the ingestion job:
   ```bash
   databricks bundle run google_drive_ingest -t dev
   ```

## Project Structure

```
google-drive-connector/
├── databricks.yml           # DABs bundle config (jobs, clusters, variables)
├── pyproject.toml           # Python project config (uv)
├── .env.example             # Template — copy to .env
├── src/
│   ├── setup/
│   │   └── create_connection.py   # One-time: create UC connection via SDK
│   └── notebooks/
│       └── ingest.py              # Databricks notebook: read Drive → write UC table
```

## Customizing for Your Workspace

1. Copy `.env.example` to `.env` and set your `DATABRICKS_HOST` and `DATABRICKS_TOKEN`
2. Update `GOOGLE_DRIVE_FOLDER_ID` with the ID of the Drive folder you want to ingest
3. Optionally change `UC_CATALOG`, `UC_SCHEMA`, and `CONNECTION_NAME`
4. In `databricks.yml`, the `targets` section uses `${DATABRICKS_HOST}` from your environment — no YAML edits needed

## Why Two Steps?

DABs cannot create Unity Catalog connections (no `connections` resource type). So:
- **`create_connection.py`** handles the connection setup via the Databricks SDK
- **`databricks.yml`** handles deploying the job/notebook that uses that connection
