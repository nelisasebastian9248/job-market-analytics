"""Minimal Snowflake connectivity test."""

from __future__ import annotations

from ingestion.utils.snowflake import get_snowflake_connection


def main() -> None:
    with get_snowflake_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                select
                    current_role(),
                    current_warehouse(),
                    current_database(),
                    current_schema()
                """
            )
            role, warehouse, database, schema = cursor.fetchone()

    print("Snowflake connection successful.")
    print(f"Role: {role}")
    print(f"Warehouse: {warehouse}")
    print(f"Database: {database}")
    print(f"Schema: {schema}")


if __name__ == "__main__":
    main()
