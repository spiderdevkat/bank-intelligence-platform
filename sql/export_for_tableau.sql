-- Run via: psql -U postgres -d bank_intelligence -f sql/export_for_tableau.sql
-- Exports current data snapshots for Tableau Public (file-based only, no live DB connection support)

\copy (SELECT * FROM fact_transactions) TO 'data/fact_transactions.csv' WITH CSV HEADER;
\copy (SELECT * FROM dimension_customer WHERE is_current) TO 'data/dimension_customer_current.csv' WITH CSV HEADER;
\copy (SELECT * FROM dimension_account) TO 'data/dimension_account.csv' WITH CSV HEADER;