EXPLAIN ANALYZE
SELECT * FROM fact_transactions WHERE amount > 5000;

CREATE INDEX idx_fact_transactions_amount ON fact_transactions (amount);

EXPLAIN ANALYZE
SELECT * FROM fact_transactions WHERE amount > 5000;

EXPLAIN ANALYZE
SELECT * FROM fact_transactions WHERE is_fraud = true;

EXPLAIN ANALYZE
SELECT * FROM fact_transactions WHERE is_fraud = false;
