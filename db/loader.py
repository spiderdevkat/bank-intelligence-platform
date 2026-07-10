from db.postgres_client import get_connection


def load_customers(customers):
    """Insert customers, return a {customer_id: customer_sk} mapping."""
    conn = get_connection()
    cursor = conn.cursor()
    customer_id_to_sk = {}

    for c in customers:
        cursor.execute(
            """
            INSERT INTO dimension_customer
                (customer_id, full_name, email, phone, country, risk_tier, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING customer_sk
            """,
            (c.customer_id, c.full_name, c.email, c.phone, c.country, c.risk_tier.value, c.created_at),
        )
        customer_sk = cursor.fetchone()[0]
        customer_id_to_sk[c.customer_id] = customer_sk

    conn.commit()
    cursor.close()
    conn.close()
    return customer_id_to_sk

def load_accounts(accounts):
    conn = get_connection()
    cursor = conn.cursor()

    for a in accounts:
        cursor.execute(
            """
            INSERT INTO dimension_account
                (account_id, customer_id, parent_account_id, account_number,
                 account_type, currency, status, opened_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (a.account_id, a.customer_id, a.parent_account_id, a.account_number,
             a.account_type.value, a.currency, a.status.value, a.opened_at),
        )

    conn.commit()
    cursor.close()
    conn.close()


def load_transactions(transactions, customer_id_to_sk):
    conn = get_connection()
    cursor = conn.cursor()

    for t in transactions:
        customer_sk = customer_id_to_sk.get(t.customer_id)
        if customer_sk is None:
            raise ValueError(f"No customer_sk found for customer_id={t.customer_id}")

        cursor.execute(
            """
            INSERT INTO fact_transactions
                (transaction_id, customer_id, customer_sk, account_id,
                 counterparty_account_id, transaction_type, channel,
                 amount, currency, transaction_timestamp, is_fraud, fraud_label)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (t.transaction_id, t.customer_id, customer_sk, t.account_id,
             t.counterparty_account_id, t.transaction_type.value, t.channel.value,
             t.amount, t.currency, t.transaction_timestamp, t.is_fraud,
             t.fraud_label.value if t.fraud_label else None),
        )

    conn.commit()
    cursor.close()
    conn.close()