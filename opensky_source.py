import requests
import dlt

def opensky_data():
    url = "https://opensky-network.org/api/states/all"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    for state in data["states"]:
        yield {
            "icao24": state[0],
            "callsign": state[1],
            "origin_country": state[2],
            "time_position": state[3],
            "last_contact": state[4],
            "longitude": state[5],
            "latitude": state[6],
            "baro_altitude": state[7],
            "on_ground": state[8],
            "velocity": state[9],
            "heading": state[10],
            "vertical_rate": state[11],
            "geo_altitude": state[13],
        }