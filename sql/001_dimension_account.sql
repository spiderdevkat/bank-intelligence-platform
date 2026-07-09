CREATE TABLE dimension_account (
    account_id       VARCHAR(50) PRIMARY KEY,
    customer_id      VARCHAR(50) NOT NULL,
    parent_account_id VARCHAR(50) REFERENCES dimension_account(account_id),
    account_number   VARCHAR(50) NOT NULL UNIQUE,
    account_type     VARCHAR(50) NOT NULL CHECK (account_type IN ('CHECKING', 'SAVINGS', 'BUSINESS')),
    currency         VARCHAR(10) NOT NULL,
    status           VARCHAR(20) NOT NULL CHECK (status IN ('ACTIVE', 'DORMANT', 'CLOSED')),
    opened_at        TIMESTAMPTZ NOT NULL
);