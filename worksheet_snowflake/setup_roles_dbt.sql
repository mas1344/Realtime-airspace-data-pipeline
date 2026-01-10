USE ROLE USERADMIN;

CREATE ROLE IF NOT EXISTS opensky_dbt_role;

GRANT ROLE opensky_dbt_role TO USER transformer;

GRANT ROLE opensky_dbt_role TO USER mas1344;



