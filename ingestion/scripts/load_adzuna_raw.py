"""Load Adzuna job postings into the Snowflake raw table."""

from __future__ import annotations

import json

from ingestion.scripts.fetch_adzuna import fetch_adzuna_jobs_for_roles
from ingestion.utils.snowflake import get_snowflake_connection


INSERT_JOB_POSTINGS_SQL = """
insert into RAW.JOB_POSTINGS (
    job_id,
    job_title,
    company_name,
    location_display_name,
    category_label,
    salary_min,
    salary_max,
    contract_type,
    contract_time,
    created_at,
    redirect_url,
    description,
    raw_payload
)
select
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s::timestamp_ntz,
    %s,
    %s,
    parse_json(%s)
where not exists (
    select 1
    from RAW.JOB_POSTINGS
    where job_id = %s
)
"""


def main() -> None:
    roles = ("data engineer", "analytics engineer")
    jobs = fetch_adzuna_jobs_for_roles(
        roles=roles,
        results_per_page=25,
        pages_per_role=4,
    )
    inserted_rows = 0

    with get_snowflake_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("truncate table RAW.JOB_POSTINGS")
            for job in jobs:
                cursor.execute(
                    INSERT_JOB_POSTINGS_SQL,
                    (
                        str(job.get("id", "")),
                        job.get("title"),
                        job.get("company", {}).get("display_name"),
                        job.get("location", {}).get("display_name"),
                        job.get("category", {}).get("label"),
                        job.get("salary_min"),
                        job.get("salary_max"),
                        job.get("contract_type"),
                        job.get("contract_time"),
                        job.get("created"),
                        job.get("redirect_url"),
                        job.get("description"),
                        json.dumps(job),
                        str(job.get("id", "")),
                    ),
                )
                inserted_rows += cursor.rowcount

    print(
        f"Fetched {len(jobs)} jobs for {', '.join(roles)} and inserted {inserted_rows} rows into RAW.JOB_POSTINGS."
    )


if __name__ == "__main__":
    main()
