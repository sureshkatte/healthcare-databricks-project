"""
Gold KPI Layer Processing Script
Computes aggregated metrics for claims based on status.
"""

# 1. Correct import syntax to prevent execution failure
import pyspark.sql.functions as F
from pyspark.sql import SparkSession

# 2. Local IDE safety net: Get or create the Spark Session if not globally injected
spark = SparkSession.builder.getOrCreate()

# 3. Read from Silver Layer Table
silver_claims_df = spark.table("workspace.default.silver_repo_claims")

# 4. Aggregate KPIs using the safe 'F.sum' wrapper to avoid built-in conflicts
gold_kpi_df = silver_claims_df.groupBy("status").agg(
    F.count('*').alias("total_claims"),
    F.sum("claim_amount").alias("total_claim_amount")
)

# 5. Write back to Gold Layer Delta Table
gold_kpi_df.write.mode('overwrite').saveAsTable("workspace.default.gold_kpi_claims")

print("Gold KPI layer created successfully!")
