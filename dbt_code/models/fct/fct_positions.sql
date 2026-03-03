select
    position_id,
    icao24,
    {{ dbt_utils.generate_surrogate_key(['last_contact']) }} as time_id,
    latitude,
    longitude,
    altitude_baro,
    velocity,
    heading,
    vertical_rate,
    on_ground,
    position_time,
    last_contact
from {{ ref('stg_opensky_positions') }}
