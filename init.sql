CREATE DATABASE endless_pulse;

CREATE USER dbms WITH PASSWORD 'DBMS123PASS';

ALTER ROLE dbms SET client_encoding TO 'utf8';
ALTER ROLE dbms SET default_transaction_isolation TO 'read committed';
ALTER ROLE dbms SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE endless_pulse TO dbms;
