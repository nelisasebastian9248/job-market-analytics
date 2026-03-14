"""Centralized project settings loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


DEFAULT_GITHUB_REPOSITORIES = (
    "dbt-labs/dbt-core",
    "apache/airflow",
    "apache/spark",
    "snowflakedb/snowflake-connector-python",
    "apache/kafka",
)


@dataclass(frozen=True)
class Settings:
    adzuna_app_id: str
    adzuna_api_key: str
    adzuna_country: str
    github_token: str
    github_repositories: tuple[str, ...]
    snowflake_account: str
    snowflake_user: str
    snowflake_password: str
    snowflake_warehouse: str
    snowflake_database: str
    snowflake_schema: str
    snowflake_role: str


def _split_csv(value: str) -> tuple[str, ...]:
    items = [item.strip() for item in value.split(",")]
    return tuple(item for item in items if item)


def load_settings() -> Settings:
    load_dotenv()

    github_repositories = _split_csv(
        os.getenv("GITHUB_REPOSITORIES", ",".join(DEFAULT_GITHUB_REPOSITORIES))
    )

    return Settings(
        adzuna_app_id=os.getenv("ADZUNA_APP_ID", ""),
        adzuna_api_key=os.getenv("ADZUNA_API_KEY", ""),
        adzuna_country=os.getenv("ADZUNA_COUNTRY", "us"),
        github_token=os.getenv("GITHUB_TOKEN", ""),
        github_repositories=github_repositories,
        snowflake_account=os.getenv("SNOWFLAKE_ACCOUNT", ""),
        snowflake_user=os.getenv("SNOWFLAKE_USER", ""),
        snowflake_password=os.getenv("SNOWFLAKE_PASSWORD", ""),
        snowflake_warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", ""),
        snowflake_database=os.getenv("SNOWFLAKE_DATABASE", ""),
        snowflake_schema=os.getenv("SNOWFLAKE_SCHEMA", ""),
        snowflake_role=os.getenv("SNOWFLAKE_ROLE", ""),
    )
