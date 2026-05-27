"""
Gold Dashboard Tables Creation
This script creates aggregated tables in the Gold layer for dashboarding purposes.
"""
spark.sql("""
          CREATE OR REPLACE TABLE workspace.default.gold_claim_status_kpis AS
          SELECT
          status,
          COUNT(*) AS total_claims,
          SUM(claim_amount) AS total_claim_amount
          FROM workspace.default.silver_repo_claims
          GROUP BY status
          """)


print("Gold Claim Status KPIs table created successfully!")

spark.sql("""
          CREATE OR REPLACE TABLE workspace.default.gold_hospital_summary AS
          SELECT
          hospital,
          COUNT(*) AS total_claims,
          SUM(claim_amount) AS total_claim_amount
          FROM workspace.default.silver_repo_claims
          GROUP BY hospital 

          """)

print ("Gold Hospital Summary table created successfully!")

spark.sql("""
          CREATE OR REPLACE TABLE workspace.default.gold_daily_claim_trend AS
          SELECT
          claim_date,
          COUNT(*) AS total_claims,
          SUM(claim_amount) AS total_claim_amount
          FROM workspace.default.silver_repo_claims
          GROUP BY claim_date 

          """)

print("Gold Daily Claim Trend table created successfully!")

spark.sql("""
          CREATE OR REPLACE TABLE workspace.default.gold_payment_summary AS
          SELECT
          COUNT(*) AS total_claims,
          SUM(claim_amount) AS total_claim_amount,
          AVG(claim_amount) AS average_claim_amount,
          MAX(claim_amount) AS max_claim_amount,
          MIN(claim_amount) AS min_claim_amount
          FROM workspace.default.silver_repo_claims 
          """)

print("Gold Payment Summary table created successfully!")



print("All Gold Dashboard Tables Created Successfully!")
