select
    full_name,
    stargazers_count,
    forks_count,
    open_issues_count,
    subscribers_count,
    default_branch,
    updated_at,
    ingested_at
from {{ source('raw', 'github_repos') }}
