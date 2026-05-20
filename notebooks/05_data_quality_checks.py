from pyspark.sql.functions import col

silver_claims_df = spark.table(
    "workspace.default.silver_claims"
)

print("===================================")
print("Null Check - claim_id")
print("===================================")

null_claims_df = silver_claims_df.filter(
    col("claim_id").isNull()
)

null_claims_df.show()

print("===================================")
print("Duplicate Check - claim_id")
print("===================================")

duplicate_claims_df = silver_claims_df.groupBy(
    "claim_id"
).count().filter(
    col("count") > 1
)

duplicate_claims_df.show()

print("===================================")
print("Negative Claim Amount Check")
print("===================================")

negative_claim_df = silver_claims_df.filter(
    col("claim_amount") < 0
)

negative_claim_df.show()

print("===================================")
print("Data Quality Checks Completed")
print("===================================")