USE ROLE USERADMIN;

CREATE ROLE IF NOT EXISTS opensky_dlt_role;

CREATE ROLE IF NOT EXISTS opensky_reader_role;


USE ROLE SECURITYADMIN;

GRANT ROLE opensky_dlt_role TO USER extract_loader;

GRANT ROLE opensky_reader_role TO USER  mas1344;


GRANT USAGE ON WAREHOUSE compute_wh TO ROLE opensky_dlt_role;

GRANT USAGE ON DATABASE opensky TO ROLE opensky_dlt_role;

GRANT USAGE ON SCHEMA opensky.staging TO ROLE opensky_dlt_role;

GRANT CREATE TABLE ON SCHEMA opensky.staging TO ROLE opensky_dlt_role;

GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA opensky.staging TO ROLE opensky_dlt_role;

GRANT INSERT, UPDATE, DELETE ON FUTURE TABLES IN SCHEMA opensky.staging TO ROLE opensky_dlt_role;


GRANT USAGE ON WAREHOUSE compute_wh TO ROLE opensky_dlt_role;

GRANT USAGE ON DATABASE opensky TO ROLE opensky_dlt_role;

GRANT USAGE ON SCHEMA opensky.staging TO ROLE opensky_dlt_role;

GRANT SELECT ON ALL TABLES IN SCHEMA opensky.staging TO ROLE opensky_reader_role;

GRANT SELECT ON FUTURE TABLES IN DATABASE opensky TO ROLE opensky_reader_role;


SHOW GRANTS ON USER extract_loader;