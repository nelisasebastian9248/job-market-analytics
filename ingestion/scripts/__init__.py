"""Executable ingestion scripts for external data sources."""

from ingestion.scripts.fetch_adzuna import fetch_adzuna_jobs
from ingestion.scripts.fetch_github import fetch_github_repo_stats
from ingestion.scripts.test_snowflake_connection import main as test_snowflake_connection

__all__ = [
    "fetch_adzuna_jobs",
    "fetch_github_repo_stats",
    "test_snowflake_connection",
]
