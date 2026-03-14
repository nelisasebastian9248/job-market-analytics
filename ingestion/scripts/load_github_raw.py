"""Load GitHub repository stats into the Snowflake raw table."""

from __future__ import annotations

import json

from ingestion.scripts.fetch_github import fetch_github_repo_stats
from ingestion.utils.snowflake import get_snowflake_connection


INSERT_GITHUB_REPOS_SQL = """
insert into RAW.GITHUB_REPOS (
    full_name,
    stargazers_count,
    forks_count,
    open_issues_count,
    subscribers_count,
    default_branch,
    updated_at,
    raw_payload
)
select
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s::timestamp_ntz,
    parse_json(%s)
"""


def main() -> None:
    repo_stats = fetch_github_repo_stats()

    with get_snowflake_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("truncate table RAW.GITHUB_REPOS")
            for repo in repo_stats:
                cursor.execute(
                    INSERT_GITHUB_REPOS_SQL,
                    (
                        repo["full_name"],
                        repo["stargazers_count"],
                        repo["forks_count"],
                        repo["open_issues_count"],
                        repo["subscribers_count"],
                        repo["default_branch"],
                        repo["updated_at"],
                        json.dumps(repo),
                    ),
                )

    print(f"Loaded {len(repo_stats)} rows into RAW.GITHUB_REPOS.")


if __name__ == "__main__":
    main()
