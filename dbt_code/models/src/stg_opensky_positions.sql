with raw as (

    select
        lower(icao24) as icao24,
        trim(callsign) as callsign,
        origin_country,

        to_timestamp(time_position) as time_position,
        to_timestamp(last_contact) as last_contact,

        cast(longitude as float) as longitude,
        cast(latitude as float) as latitude,
        cast(baro_altitude as float) as altitude_baro,
        cast(velocity as float) as velocity,
        cast(heading as float) as heading,
        cast(vertical_rate as float) as vertical_rate,
        cast(on_ground as boolean) as on_ground

    from {{ source('opensky_staging', 'stg_opensky') }}

    where latitude is not null
      and longitude is not null
)

select
    {{ dbt_utils.generate_surrogate_key(['icao24', 'last_contact']) }} as position_id,
    *
from raw
