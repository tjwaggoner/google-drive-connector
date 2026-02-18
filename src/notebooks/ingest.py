# Databricks notebook source
# MAGIC %md
# MAGIC # Google Drive File Ingestion
# MAGIC Reads files from Google Drive via a Unity Catalog connection
# MAGIC and writes them to a managed table.

# COMMAND ----------

dbutils.widgets.text("catalog", "main")
dbutils.widgets.text("schema", "google_drive")
dbutils.widgets.text("connection_name", "google_drive_connection")

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
connection_name = dbutils.widgets.get("connection_name")

# COMMAND ----------

spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Read files from Google Drive
# MAGIC Adjust the `url` to point at your Drive folder or file.
# MAGIC Supported formats: CSV, JSON, Parquet, etc.

# COMMAND ----------

# Example: read a CSV from a Google Drive folder
df = (
    spark.read.format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .option("databricks.connection", connection_name)
    .load("gdrive://your-folder-id")
)

display(df)

# COMMAND ----------

# Write to Unity Catalog
df.write.mode("overwrite").saveAsTable(f"{catalog}.{schema}.drive_data")
print(f"Written to {catalog}.{schema}.drive_data")
