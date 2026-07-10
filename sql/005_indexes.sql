CREATE INDEX idx_dimension_customer_natural_key ON dimension_customer (customer_id);
CREATE INDEX idx_dimension_customer_current ON dimension_customer (customer_id) WHERE is_current;

CREATE INDEX idx_dimension_account_customer_id ON dimension_account (customer_id);
CREATE INDEX idx_dimension_account_parent ON dimension_account (parent_account_id);

CREATE INDEX idx_fact_transactions_customer_id ON fact_transactions (customer_id);
CREATE INDEX idx_fact_transactions_account_id ON fact_transactions (account_id);
CREATE INDEX idx_fact_transactions_timestamp ON fact_transactions (transaction_timestamp);
CREATE INDEX idx_fact_transactions_is_fraud ON fact_transactions (is_fraud);