"""Snowflake connection helpers."""

from __future__ import annotations

import snowflake.connector
from snowflake.connector import SnowflakeConnection

from config.settings import load_settings


def get_snowflake_connection() -> SnowflakeConnection:
    settings = load_settings()
    return snowflake.connector.connect(
        account=settings.snowflake_account,
        user=settings.snowflake_user,
        password=settings.snowflake_password,
        warehouse=settings.snowflake_warehouse,
        database=settings.snowflake_database,
        schema=settings.snowflake_schema,
        role=settings.snowflake_role,
    )
