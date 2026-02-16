USE ROLE useradmin;

CREATE USER IF NOT EXISTS reporter
    PASSWORD = 'Antarevahshi00$'
    DEFAULT_WAREHOUSE = COMPUTE_WH
    LOGIN_NAME = 'reporter'
    DEFAULT_NAMESPACE = 'opensky.marts'
    COMMENT = 'reporter user making analysis and BI'
    DEFAULT_ROLE = 'opensky_reporter_role'