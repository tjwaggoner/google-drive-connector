# Databricks notebook source
# MAGIC %md
# MAGIC # Google Drive → Unity Catalog Ingestion
# MAGIC Reads a Google Sheet, discovers all tabs via listSheets,
# MAGIC and writes each as a Delta table in Unity Catalog.
# MAGIC
# MAGIC Requires DBR 17.3+ and a Google Drive UC connection.

# COMMAND ----------

# ── Configuration ──────────────────────────────────────────────────────
# Update these values for your environment
catalog = "waggoner"
schema = "bronze"
connection_name = "waggoner-gdrive-connection"
gsheet_id = "your-gsheet-id"
# ───────────────────────────────────────────────────────────────────────

gsheet_url = f"https://docs.google.com/spreadsheets/d/{gsheet_id}/"

# COMMAND ----------

spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")
spark.sql(f"USE CATALOG {catalog}")
spark.sql(f"USE SCHEMA {schema}")

# COMMAND ----------

import re

def clean_name(name):
    """Convert a string to a valid Delta-compatible snake_case name."""
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Discover all tabs

# COMMAND ----------

sheets_df = (
    spark.read.format("excel")
    .option("databricks.connection", connection_name)
    .option("operation", "listSheets")
    .load(gsheet_url)
)

tab_names = [row["sheetName"] for row in sheets_df.collect()]
print(f"Found {len(tab_names)} tabs: {tab_names}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Ingest each tab as a Delta table
# MAGIC - headerRows=0 because sheet headers often have characters incompatible with Delta column names
# MAGIC - All datatypes are string as a result — cast downstream as needed

# COMMAND ----------

results = []

from pyspark.sql import functions as F

for tab_name in tab_names:
    table_name = clean_name(tab_name)
    print(f"Reading '{tab_name}' -> {catalog}.{schema}.{table_name}")

    raw = (
        spark.read.format("excel")
        .option("databricks.connection", connection_name)
        .option("headerRows", 0)
        .option("dataAddress", tab_name)
        .load(gsheet_url)
    )

    # First row is the header — extract clean column names from it
    header_row = raw.first()
    col_names = [clean_name(str(header_row[c])) for c in raw.columns]

    # Skip the header row, rename columns
    first_col = raw.columns[0]
    df = raw.filter(F.col(first_col) != header_row[first_col])
    df = df.toDF(*col_names)

    # write to delta table
    df.write.mode("overwrite").saveAsTable(table_name)

    # track progress
    row_count = df.count()
    results.append({"sheet": tab_name, "table": f"{catalog}.{schema}.{table_name}", "rows": row_count})
    print(f"  done - {row_count} rows")

