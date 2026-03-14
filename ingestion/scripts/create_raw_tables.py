"""Create Snowflake raw tables for API ingestion."""

from __future__ import annotations

from ingestion.utils.snowflake import get_snowflake_connection


JOB_POSTINGS_DDL = """
create table if not exists RAW.JOB_POSTINGS (
    job_id string,
    job_title string,
    company_name string,
    location_display_name string,
    category_label string,
    salary_min number(12, 2),
    salary_max number(12, 2),
    contract_type string,
    contract_time string,
    created_at timestamp_ntz,
    redirect_url string,
    description string,
    raw_payload variant,
    ingested_at timestamp_ntz default current_timestamp()
)
"""


GITHUB_REPOS_DDL = """
create table if not exists RAW.GITHUB_REPOS (
    full_name string,
    stargazers_count number,
    forks_count number,
    open_issues_count number,
    subscribers_count number,
    default_branch string,
    updated_at timestamp_ntz,
    raw_payload variant,
    ingested_at timestamp_ntz default current_timestamp()
)
"""


def main() -> None:
    with get_snowflake_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(JOB_POSTINGS_DDL)
            cursor.execute(GITHUB_REPOS_DDL)

    print("Created RAW.JOB_POSTINGS and RAW.GITHUB_REPOS.")


if __name__ == "__main__":
    main()
