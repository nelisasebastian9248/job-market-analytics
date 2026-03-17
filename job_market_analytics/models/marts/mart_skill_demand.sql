select
    skill,
    count(*) as skill_mentions,
    count(distinct job_id) as distinct_jobs,
    count(distinct company_name) as distinct_companies
from {{ ref('int_job_skills') }}
group by 1
order by 2 desc
