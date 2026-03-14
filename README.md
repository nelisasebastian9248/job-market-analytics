# Job Market Analytics

End-to-end analytics project that combines job posting trends and GitHub activity to surface hiring demand, salary benchmarks, and skill momentum.

## Tech Stack

- Python for ingestion and utility scripts
- Snowflake for storage and analytics
- dbt for transformations
- Streamlit for dashboards
- Airflow for orchestration

## Phase 1 Status

The repository now includes the base folder structure and starter configuration for:

- `ingestion/`
- `dbt/`
- `streamlit/`
- `airflow/`
- `config/`
- `tests/`

## Setup

Activate the virtual environment in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the starter dependencies:

```powershell
pip install -r requirements.txt
```

## Next Steps

1. Add your API and Snowflake credentials to `.env`.
2. Create the Snowflake trial account and warehouse objects.
3. Build the first ingestion script in `ingestion/scripts/`.
