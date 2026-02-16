USE ROLE useradmin;
CREATE ROLE IF NOT EXISTS opensky_reporter_role;

USE ROLE securityadmin;

GRANT USAGE ON WAREHOUSE compute_wh TO ROLE opensky_reporter_role;
GRANT USAGE ON DATABASE opensky TO ROLE opensky_reporter_role;
GRANT USAGE ON SCHEMA opensky.marts TO ROLE opensky_reporter_role;
GRANT SELECT ON ALL TABLES IN SCHEMA opensky.marts TO ROLE opensky_reporter_role;
GRANT SELECT ON ALL VIEWS IN SCHEMA opensky.marts TO ROLE opensky_reporter_role;
GRANT SELECT ON FUTURE TABLES IN SCHEMA opensky.marts TO ROLE opensky_reporter_role;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA opensky.marts TO ROLE opensky_reporter_role;


GRANT ROLE opensky_reporter_role TO USER reporter;
GRANT ROLE opensky_reporter_role TO USER mas1344;

USE ROLE opensky_reporter_role;

SHOW GRANTS TO ROLE opensky_reporter_role;

-- test querying a mart
USE WAREHOUSE compute_wh;
SELECT * FROM opensky.marts.mart_flight_positions;