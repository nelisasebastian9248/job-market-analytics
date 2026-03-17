select
    full_name,
    stargazers_count,
    forks_count,
    subscribers_count,
    open_issues_count,
    updated_at,
    (stargazers_count + forks_count + subscribers_count) as momentum_score
from {{ ref('stg_github_repos') }}
