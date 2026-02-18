# Google Drive Connector for Databricks

Connect Google Drive to Databricks for ingesting files into Unity Catalog.

## Setup

1. Clone this repo:
   ```bash
   git clone git@github.com:tjwaggoner/google-drive-connector.git
   cd google-drive-connector
   ```

2. Copy the environment template and fill in your values:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` with your Databricks workspace URL and token:
   ```
   DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
   DATABRICKS_TOKEN=your-personal-access-token
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

All workspace-specific configuration lives in `.env`. The `.env.example` file is tracked in git as a template — your actual `.env` is gitignored to keep secrets safe.
