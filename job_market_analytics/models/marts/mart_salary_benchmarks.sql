select
    job_title,
    location_display_name,
    count(*) as job_postings,
    avg(salary_min) as avg_salary_min,
    avg(salary_max) as avg_salary_max,
    min(salary_min) as min_salary_min,
    max(salary_max) as max_salary_max
from {{ ref('stg_job_postings') }}
where salary_min is not null
  and salary_max is not null
group by 1, 2
order by job_postings desc, avg_salary_max desc
