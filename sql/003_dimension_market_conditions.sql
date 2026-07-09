CREATE TABLE dimension_market_conditions (
    market_condition_id BIGSERIAL PRIMARY KEY,
    date_key             DATE NOT NULL UNIQUE,
    interest_rate         NUMERIC(6, 4),
    fx_usd_eur            NUMERIC(10, 6),
    fx_usd_gbp            NUMERIC(10, 6),
    fx_usd_inr            NUMERIC(10, 6),
    source                VARCHAR(100) NOT NULL,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);