from datetime import datetime, timezone
import dlt, requests

@dlt.resource
def opensky_data_resource():
    url = "https://opensky-network.org/api/states/all"
    resp = requests.get(url, timeout=15, headers={"Cache-Control":"no-cache"})
    resp.raise_for_status()
    data = resp.json()
    now_ts = int(datetime.now(timezone.utc).timestamp())
    for state in data.get("states", []):
        time_pos = state[3] or 0
        last_contact = state[4] or time_pos
        on_ground = state[8]
        # filtrera: inte på marken och senaste kontakt inom 5 minuter (300s)
        if on_ground is False and (last_contact >= now_ts - 300):
            yield {
                "icao24": state[0],
                "callsign": state[1],
                "origin_country": state[2],
                "position_time": time_pos,
                "last_contact": last_contact,
                "longitude": state[5],
                "latitude": state[6],
                "baro_altitude": state[7],
                "on_ground": on_ground,
                "velocity": state[9],
                "heading": state[10],
                "vertical_rate": state[11],
                "geo_altitude": state[13],
                "ingested_at": now_ts
            }

@dlt.source
def opensky_data_source():
    return opensky_data_resource()