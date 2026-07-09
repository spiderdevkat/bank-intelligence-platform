CREATE TABLE fact_transactions (
    transaction_id          VARCHAR(50) PRIMARY KEY,
    customer_id             VARCHAR(50) NOT NULL,
    customer_sk             BIGINT NOT NULL REFERENCES dimension_customer(customer_sk),
    account_id              VARCHAR(50) NOT NULL REFERENCES dimension_account(account_id),
    counterparty_account_id VARCHAR(50) REFERENCES dimension_account(account_id),
    market_condition_id     BIGINT REFERENCES dimension_market_conditions(market_condition_id),
    transaction_type        VARCHAR(50) NOT NULL CHECK (transaction_type IN ('DEPOSIT', 'WITHDRAWAL', 'TRANSFER', 'PAYMENT')),
    channel                 VARCHAR(50) NOT NULL CHECK (channel IN ('ATM', 'ONLINE', 'BRANCH', 'WIRE', 'CARD')),
    amount                  NUMERIC(14, 2) NOT NULL CHECK (amount >= 0),
    currency                VARCHAR(10) NOT NULL,
    transaction_timestamp   TIMESTAMPTZ NOT NULL,
    is_fraud                BOOLEAN NOT NULL DEFAULT FALSE,
    fraud_label             VARCHAR(50),
    created_at              TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);