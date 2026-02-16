{{ config(
    materialized='incremental',
    unique_key='position_id'
) }}

with fct as (
    select *
    from {{ ref('fct_positions') }}
),

aircraft as (
    select *
    from {{ ref('dim_aircraft') }}
),

time as (
    select *
    from {{ ref('dim_time') }}
),

-- källa begränsad vid inkrementell körning för prestanda
src as (
    select
      fct.position_id,
      fct.icao24,
      fct.time_id,
      fct.latitude,
      fct.longitude,
      fct.altitude_baro,
      fct.velocity,
      fct.heading,
      fct.vertical_rate,
      fct.on_ground,
      fct.position_time,
      fct.last_contact
    from fct
    {% if is_incremental() %}
      -- bearbeta bara rader som är nyare än det som redan finns i måltabellen
      where coalesce(fct.last_contact, fct.position_time) > (
        select coalesce(max(coalesce(last_contact, position_time)), 0) from {{ this }}
      )
    {% endif %}
)

select
    -- keys
    s.position_id,
    s.icao24,
    s.time_id,

    -- aircraft info
    a.origin_country,

    -- time info
    t.timestamp_utc,
    t.date,
    t.hour,
    t.weekday,

    -- position info
    s.latitude,
    s.longitude,
    s.altitude_baro,
    s.velocity,
    s.heading,
    s.vertical_rate,
    s.on_ground

from src s
left join aircraft a on s.icao24 = a.icao24
left join time t on s.time_id = t.time_id

-- slutfilter för att säkerställa att endast aktiva flyg materialiseras
where s.on_ground = false
  and coalesce(s.last_contact, s.position_time) >= dateadd(minute, -5, current_timestamp())
