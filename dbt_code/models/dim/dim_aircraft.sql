with aircraft as (
    select distinct
        icao24,
        origin_country
    from {{ ref('stg_opensky_positions') }}
)

select
    icao24,
    origin_country
from aircraft
