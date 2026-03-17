select
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
    ingested_at
from {{ source('raw', 'job_postings') }}
