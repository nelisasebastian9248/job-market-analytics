select
    jp.job_id,
    jp.job_title,
    jp.company_name,
    jp.location_display_name,
    s.skill,
    jp.created_at,
    jp.ingested_at
from {{ ref('stg_job_postings') }} as jp
cross join {{ ref('skills') }} as s
where contains(lower(jp.description), lower(s.skill))
