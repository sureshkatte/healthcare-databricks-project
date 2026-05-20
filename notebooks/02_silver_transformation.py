from pyspark.sql.functions import (col, current_timestamp, to_date)

bronze_claims_df = spark.table("workspace.default.bronze_claims")

silver_claims_df = bronze_claims_df.withColumn("claim_id", col("claim_id").cast("integer")) \
    .withColumn("patient_id", col("patient_id").cast("integer")) \
    .withColumn("claim_amount", col("claim_amount").cast("double")) \
    .withColumn("claim_date", to_date(col("claim_date"))) \
    .withColumn("created_at", current_timestamp()) \
    .dropDuplicates()

silver_claims_df.write.mode('overwrite').saveAsTable("workspace.default.silver_claims")

print("Silver Layer Transformation Completed Successfully!")