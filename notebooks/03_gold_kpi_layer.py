from pyspark.sql.functions import (sum, count)

silver_claims_df = spark.table("workspace.default.silver_repo_claims")

gold_kpi_df = silver_claims_df.groupBy("status").agg(
  count('*').alias("total_claims"),
  sum("claim_amount").alias("total_claim_amount")
)

gold_kpi_df.write.mode('overwrite').saveAsTable("workspace.default.gold_kpi_claims")

print("Gold KPI layer created successfully!")

