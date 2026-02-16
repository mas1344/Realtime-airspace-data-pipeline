USE ROLE SYSADMIN;

USE DATABASE opensky;

CREATE SCHEMA IF NOT EXISTS warehouse;

USE ROLE securityadmin;

GRANT ROLE opensky_dlt_role TO ROLE opensky_dbt_role;

SHOW GRANTS TO ROLE opensky_dbt_role;

GRANT USAGE, 
CREATE TABLE, 
CREATE VIEW ON SCHEMA opensky.warehouse TO ROLE opensky_dbt_role;

GRANT SELECT,
INSERT,
UPDATE,
DELETE ON ALL TABLES IN SCHEMA opensky.warehouse TO ROLE opensky_dbt_role;

GRANT SELECT ON ALL VIEWS IN SCHEMA opensky.warehouse TO ROLE opensky_dbt_role;

GRANT SELECT,
INSERT,
UPDATE,
DELETE ON FUTURE TABLES IN SCHEMA opensky.warehouse TO ROLE opensky_dbt_role;

GRANT SELECT ON FUTURE VIEWS IN SCHEMA opensky.warehouse TO ROLE opensky_dbt_role;

USE ROLE opensky_dbt_role;

USE WAREHOUSE compute_wh;
SELECT * FROM opensky.staging.opensky_data LIMIT 10;