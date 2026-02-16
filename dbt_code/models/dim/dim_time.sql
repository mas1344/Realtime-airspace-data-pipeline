with timestamps as (
    select distinct
        last_contact as timestamp_utc
    from {{ ref('stg_opensky_positions') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['timestamp_utc']) }} as time_id,
    timestamp_utc,
    to_date(timestamp_utc) as date,
    extract(hour from timestamp_utc) as hour,
    extract(dow from timestamp_utc) as weekday,
    extract(month from timestamp_utc) as month,
    extract(year from timestamp_utc) as year
from timestamps
