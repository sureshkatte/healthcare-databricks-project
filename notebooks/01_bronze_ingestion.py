import sys

sys.path.append("/Workspace/Users/suresh.babu@accionlabs.com/healthcare-databricks-project")

from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

BASE_PATH = "/Workspace/Users/suresh.babu@accionlabs.com/healthcare-databricks-project"

patients_df = spark.read.format("csv").option("header", "true").load(f"{BASE_PATH}/data/patients.csv")

claims_df = spark.read.format("csv").option("header", "true").load(f"{BASE_PATH}/data/claims.csv")

payments_df = spark.read.format("csv").option("header", "true").load(f"{BASE_PATH}/data/payments.csv")

patients_df.write.mode('overwrite').saveAsTable("workspace.default.bronze_patients")
claims_df.write.mode('overwrite').saveAsTable("workspace.default.bronze_claims")
payments_df.write.mode('overwrite').saveAsTable("workspace.default.bronze_payments")

print("Bronze Layer Ingestion Completed Successfully!")