# Healthcare Databricks Project

This repository contains a sample healthcare claims data pipeline built for Databricks using PySpark and Delta-style managed tables. The project demonstrates a simple medallion architecture that ingests raw CSV data, transforms it into a cleaned silver layer, builds gold KPI tables, and runs basic data quality checks.

## Project Overview

The pipeline processes healthcare claims, patient, and payment data through the following layers:

| Layer | Purpose | Output Tables |
| --- | --- | --- |
| Bronze | Load raw CSV files into Databricks tables | `workspace.default.bronze_patients`, `workspace.default.bronze_claims`, `workspace.default.bronze_payments` |
| Silver | Clean and standardize claims data | `workspace.default.silver_repo_claims` |
| Gold | Create KPI and dashboard-ready aggregates | `workspace.default.gold_kpi_claims`, `workspace.default.gold_claim_status_kpis`, `workspace.default.gold_hospital_summary`, `workspace.default.gold_daily_claim_trend`, `workspace.default.gold_payment_summary` |

## Repository Structure

```text
healthcare-databricks-project/
├── configs/
│   └── config.py
├── data/
│   ├── claims.csv
│   ├── patients.csv
│   └── payments.csv
├── jobs/
│   └── healthcare_job.json
├── notebooks/
│   ├── 01_bronze_ingestion.py
│   ├── 02_silver_transformation.py
│   ├── 03_gold_kpi_layer.py
│   ├── 04_gold_dashboard_tables.py
│   └── 05_data_quality_checks.py
└── README.md
```

## Data Sources

The sample input files are stored in the `data/` directory:

- `patients.csv`: Patient demographic data such as patient ID, name, gender, age, and state.
- `claims.csv`: Healthcare claim details such as claim ID, patient ID, hospital, claim amount, status, and claim date.
- `payments.csv`: Payment details such as payment ID, claim ID, payment method, and payment status.

## Pipeline Flow

1. **Bronze ingestion**
   - Notebook: `notebooks/01_bronze_ingestion.py`
   - Reads raw CSV files from the project `data/` folder.
   - Writes raw tables to the `workspace.default` catalog/schema.

2. **Silver transformation**
   - Notebook: `notebooks/02_silver_transformation.py`
   - Reads `workspace.default.bronze_claims`.
   - Casts columns to appropriate data types.
   - Converts `claim_date` to a date field.
   - Adds a `created_at` timestamp.
   - Removes duplicate rows.
   - Writes the cleaned table as `workspace.default.silver_repo_claims`.

3. **Data quality checks**
   - Notebook: `notebooks/05_data_quality_checks.py`
   - Checks for null `claim_id` values.
   - Checks for duplicate `claim_id` values.
   - Checks for negative claim amounts.

4. **Gold KPI layer**
   - Notebook: `notebooks/03_gold_kpi_layer.py`
   - Aggregates claim count and total claim amount by claim status.
   - Writes the result as `workspace.default.gold_kpi_claims`.

5. **Gold dashboard tables**
   - Notebook: `notebooks/04_gold_dashboard_tables.py`
   - Creates dashboard-ready summary tables by claim status, hospital, claim date, and payment summary metrics.

## Prerequisites

- Databricks workspace
- Spark cluster or serverless compute with PySpark support
- Access to the `workspace.default` catalog/schema
- Repository imported into Databricks Repos or uploaded to the workspace

## Configuration

The project includes a basic configuration file at `configs/config.py`:

```python
BASE_PATH = "/Workspace/Repos/sureshkatte/healthcare-databricks-project"
DATA_PATH = f"{BASE_PATH}/data"
DATABASE = "workspace.default"
```

Before running the notebooks, update workspace paths if your Databricks repo location is different. The notebooks currently reference:

```text
/Workspace/Users/suresh.babu@accionlabs.com/healthcare-databricks-project
```

Keep the notebook paths and `BASE_PATH` values aligned with the actual location of this repository in your Databricks workspace.

## How to Run

Run the notebooks in this order:

```text
01_bronze_ingestion.py
02_silver_transformation.py
05_data_quality_checks.py
03_gold_kpi_layer.py
04_gold_dashboard_tables.py
```

After the run completes, validate that the expected tables were created in `workspace.default`.

Example validation queries:

```sql
SELECT * FROM workspace.default.bronze_claims;
SELECT * FROM workspace.default.silver_repo_claims;
SELECT * FROM workspace.default.gold_claim_status_kpis;
SELECT * FROM workspace.default.gold_hospital_summary;
SELECT * FROM workspace.default.gold_daily_claim_trend;
SELECT * FROM workspace.default.gold_payment_summary;
```

## Databricks Job

The `jobs/healthcare_job.json` file defines a Databricks job named `healthcare_claims_pipeline`.

Task order:

```text
bronze_ingestion
silver_transformation
data_quality_checks
gold_kpi_layer
gold_dashboard_tables
```

The job is scheduled to run daily at 9:00 AM Asia/Kolkata using the following cron expression:

```text
0 0 9 * * ?
```

## Outputs

The pipeline creates the following tables:

| Table | Description |
| --- | --- |
| `workspace.default.bronze_patients` | Raw patient data |
| `workspace.default.bronze_claims` | Raw claims data |
| `workspace.default.bronze_payments` | Raw payment data |
| `workspace.default.silver_repo_claims` | Cleaned and typed claims data |
| `workspace.default.gold_kpi_claims` | Claim count and amount by status |
| `workspace.default.gold_claim_status_kpis` | Dashboard KPI table by claim status |
| `workspace.default.gold_hospital_summary` | Claim summary by hospital |
| `workspace.default.gold_daily_claim_trend` | Daily claim count and amount trend |
| `workspace.default.gold_payment_summary` | Overall claim amount summary metrics |

## Data Quality Checks

The data quality notebook validates:

- Missing claim IDs
- Duplicate claim IDs
- Negative claim amounts

These checks help confirm that the silver claims table is usable before gold-level aggregations are created.

## Notes

- The current silver layer focuses on claims data only.
- Patient and payment data are ingested into bronze tables and can be joined into future silver or gold models.
- The sample dataset is intentionally small and designed for pipeline demonstration and development.
