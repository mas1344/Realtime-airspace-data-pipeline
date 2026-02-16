import os
from dotenv import load_dotenv
import pandas as pd
import snowflake.connector

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
ENV_PATH = os.path.join(ROOT_DIR, ".env")

def load_from_snowflake():
    load_dotenv(ENV_PATH)
    
    conn = snowflake.connector.connect(
        user = os.getenv("SNOWFLAKE_USER"),
        password = os.getenv("SNOWFLAKE_PASSWORD"),
        account = os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse = os.getenv("SNOWFLAKE_WAREHOUSE"),
        database = os.getenv("SNOWFLAKE_DATABASE"),
        schema = os.getenv("SNOWFLAKE_SCHEMA"),
        role = os.getenv("SNOWFLAKE_ROLE"),
    )

    query = """
        SELECT
            position_id,
            icao24,
            origin_country,
            timestamp_utc,
            latitude,
            longitude,
            altitude_baro,
            velocity,
            heading,
            vertical_rate,
            on_ground
        FROM mart_flight_positions
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df

print(load_from_snowflake())
