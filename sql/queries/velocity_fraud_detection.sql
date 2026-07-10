SELECT
        customer_id,
        account_id,
        transaction_timestamp,
        amount,
        fraud_label,
        COUNT(*) OVER (
            PARTITION BY customer_id
            ORDER BY transaction_timestamp
            RANGE BETWEEN INTERVAL '15 minutes' PRECEDING AND CURRENT ROW
        ) AS tx_count_15m
    FROM fact_transactions
    