CREATE TABLE dimension_customer (
    customer_sk   BIGSERIAL PRIMARY KEY,
    customer_id   VARCHAR(50) NOT NULL,
    full_name     VARCHAR(255) NOT NULL,
    email         VARCHAR(255) NOT NULL,
    phone         VARCHAR(30),
    country       VARCHAR(2) NOT NULL,
    risk_tier     VARCHAR(20) NOT NULL CHECK (risk_tier IN ('LOW', 'MEDIUM', 'HIGH')),
    valid_from    TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    valid_to      TIMESTAMPTZ,
    is_current    BOOLEAN NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);