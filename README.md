# Job Market Analytics

Job Market Analytics is an end-to-end data engineering project that tracks live hiring demand for `data engineer` and `analytics engineer` roles and compares those signals with open-source data platform tool activity on GitHub.

Live app: https://job-market-analytics.streamlit.app/

## What It Does

- Pulls live job postings from the Adzuna API
- Pulls public repository metrics from the GitHub API
- Loads raw data into Snowflake
- Transforms the raw data with dbt across `RAW`, `STAGING`, and `MART` layers
- Visualizes skill demand, salary benchmarks, and tool momentum in Streamlit

## Architecture

```text
Adzuna API -----------\
                        -> Python ingestion -> Snowflake RAW -> dbt STAGING / MART -> Streamlit dashboard
GitHub API -----------/
```

## Core Outputs

- `MART.MART_SKILL_DEMAND`
  - Aggregated counts of tracked data engineering tools found in job descriptions
- `MART.MART_SALARY_BENCHMARKS`
  - Salary benchmarks by job title and location
- `MART.MART_GITHUB_REPO_MOMENTUM`
  - GitHub repository metrics for data platform and analytics engineering tools

## Tech Stack

- Python
- Snowflake
- dbt
- Streamlit
- Adzuna API
- GitHub API

## Project Structure

```text
ingestion/             Python ingestion and Snowflake load scripts
config/                Environment-backed project settings
job_market_analytics/  dbt project
streamlit/             Streamlit dashboard
```

## Dashboard Sections

- Skill Demand
  - Tracks the most frequently mentioned modern data engineering tools in current job postings
- Salary Benchmarks
  - Summarizes salary ranges by role and location
- Tool Momentum
  - Shows GitHub activity for data platform and analytics engineering repositories

## Project Highlights

- Built a live API-to-warehouse pipeline instead of relying on static datasets
- Modeled the warehouse using layered `RAW`, `STAGING`, and `MART` schemas
- Used dbt seeds and transformation models to extract tool demand from job descriptions
- Built Snowflake-backed marts for dashboard-ready skill, salary, and GitHub metrics
- Deployed the final dashboard as a public Streamlit app

## Current Findings

The current dataset is focused on `data engineer` and `analytics engineer` roles. Based on the latest modeled output:

- Tool demand is concentrated around platforms such as `dbt`, `Snowflake`, `Databricks`, cloud providers, and core query/programming skills
- Salary benchmarks show strong variation across location and role title combinations
- GitHub momentum is strongest among high-activity data platform ecosystems such as Python, Spark, Airflow, dbt, and orchestration tooling

These findings are intended as live directional signals rather than a complete labor-market census.

## Resume Bullet

Built an end-to-end job market analytics platform ingesting live Adzuna job postings and GitHub repository data into Snowflake, transforming data with dbt across staging and mart layers, and deploying a Streamlit dashboard to surface tool demand, salary benchmarks, and data engineering ecosystem momentum.

## Local Setup

1. Create and sync the environment:

```powershell
uv venv
uv sync
```

2. Add local credentials to `.env`:

```env
ADZUNA_APP_ID=...
ADZUNA_API_KEY=...
GITHUB_TOKEN=...
GITHUB_REPOSITORIES=dbt-labs/dbt-core,apache/airflow,apache/spark,delta-io/delta,databricks/databricks-sdk-py,snowflakedb/snowflake-connector-python,python/cpython,dagster-io/dagster,kedro-org/kedro,prefecthq/prefect
SNOWFLAKE_ACCOUNT=...
SNOWFLAKE_USER=...
SNOWFLAKE_PASSWORD=...
SNOWFLAKE_WAREHOUSE=JOB_MARKET_WH
SNOWFLAKE_DATABASE=JOB_MARKET_ANALYTICS
SNOWFLAKE_SCHEMA=RAW
SNOWFLAKE_ROLE=JOB_MARKET_ROLE
```

3. Reload source data:

```powershell
uv run python -m ingestion.scripts.load_adzuna_raw
uv run python -m ingestion.scripts.load_github_raw
```

4. Build dbt models:

```powershell
cd job_market_analytics
.\run_dbt.ps1 seed --select skills
.\run_dbt.ps1 run
.\run_dbt.ps1 test
```

5. Run the dashboard:

```powershell
uv run streamlit run streamlit/app.py
```

## Notes

- The deployed Streamlit app uses Snowflake-backed mart tables.
- Local secrets are intentionally excluded from Git; only `.env.example` is tracked.
- The job-skill extraction uses a curated tool-focused seed list to keep the dashboard aligned with data engineering roles.
