# Google Drive Connector for Databricks

Reads a Google Sheet into Unity Catalog Delta tables. Discovers all tabs automatically via `listSheets`, cleans column names for Delta compatibility, and writes each tab as its own table.

## Reference

- [Google Drive connector setup](https://docs.databricks.com/gcp/en/ingestion/google-drive)
- [Excel format options (dataAddress, listSheets, etc.)](https://docs.databricks.com/aws/en/query/formats/excel)

## Prerequisites

- Databricks workspace with DBR 17.3+
- [uv](https://docs.astral.sh/uv/) and [Databricks CLI](https://docs.databricks.com/dev-tools/cli/install.html)

## Setup

1. Clone and install:
   ```bash
   git clone git@github.com:tjwaggoner/google-drive-connector.git
   cd google-drive-connector
   uv sync
   ```

2. Create Google OAuth credentials in [GCP Console](https://console.cloud.google.com/apis/credentials):
   - '+ Create Credentials' -> 'OAuth Client ID'
   - Application type: Web application
   - Authorized redirect URI: `https://<your-workspace>.cloud.databricks.com/login/oauth/google.html`
   - Add scope `https://www.googleapis.com/auth/drive.readonly` to the OAuth consent screen

3. Enable the Google Drive connector preview in your workspace (Settings > Previews)
   - Requires workspace admin
   - See: https://docs.databricks.com/gcp/en/ingestion/google-drive

4. Create the Google Drive connection in Catalog Explorer UI (Catalog > Connections > Create)
   - **IMPORTANT**: per the [Google Drive connector setup](https://docs.databricks.com/gcp/en/ingestion/google-drive), use `https://www.googleapis.com/auth/drive.readonly` as the `oauth_scope` name
   - This requires interactive OAuth consent and cannot be automated

5. Update the configuration variables in `ingest.py`:
   ```python
   catalog = "your-catalog"
   schema = "your-schema"
   connection_name = "your-gdrive-connection"
   gsheet_id = "your-google-sheet-id"  # the ID from the Sheet URL: docs.google.com/spreadsheets/d/<this-part>/edit
   ```

6. Deploy to your workspace (deploys to `/Workspace/Users/<your-email>/google-drive-connector/`):
   ```bash
   uv run python deploy.py
   ```

7. Open the notebook in your workspace and run on a DBR 17.3+ cluster

## How it works

- Uses `listSheets` to discover all tabs in the Google Sheet, then loops through each one and writes it as a separate Delta table
- `headerRows=0` reads everything as strings to avoid Delta column name restrictions
- First row is extracted as header, cleaned to snake_case, and applied as column names
- All data types are string as a result — cast downstream as needed
- If you wish to change how schemas are detected, reference the docs under [Reference](#reference)
