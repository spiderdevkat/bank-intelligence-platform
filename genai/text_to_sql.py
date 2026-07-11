import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import re

from db.postgres_client import get_connection
from genai.gemini_client import ask

SCHEMA_CONTEXT = """
You are a SQL assistant for a banking analytics database. Only these
tables and columns exist — never invent column names that aren't listed:

dimension_customer (customer_sk, customer_id, full_name, email, phone,
    country, risk_tier, valid_from, valid_to, is_current, created_at)

dimension_account (account_id, customer_id, parent_account_id,
    account_number, account_type, currency, status, opened_at)

fact_transactions (transaction_id, customer_id, customer_sk, account_id,
    counterparty_account_id, market_condition_id, transaction_type,
    channel, amount, currency, transaction_timestamp, is_fraud,
    fraud_label, created_at)

Generate ONLY a single PostgreSQL SELECT statement that answers the
question. Do not include any explanation, markdown formatting, or
code fences — output raw SQL only.
"""

DANGEROUS_KEYWORDS = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "GRANT", "REVOKE"]


class UnsafeQueryError(Exception):
    pass


def generate_sql(question: str) -> str:
    prompt = f"{SCHEMA_CONTEXT}\n\nQuestion: {question}\n\nSQL:"
    raw_response = ask(prompt)
    # Strip markdown code fences if the model added them despite instructions
    sql = re.sub(r"^```sql\s*|```$", "", raw_response.strip(), flags=re.MULTILINE).strip()
    return sql


def validate_sql(sql: str) -> None:
    """Raises UnsafeQueryError if the SQL fails our safety checks."""
    normalized = sql.strip().upper()

    if not normalized.startswith("SELECT"):
        raise UnsafeQueryError(f"Refusing to run non-SELECT statement: {sql}")

    for keyword in DANGEROUS_KEYWORDS:
        if re.search(rf"\b{keyword}\b", normalized):
            raise UnsafeQueryError(f"Refusing to run query containing dangerous keyword '{keyword}': {sql}")


def run_safe_query(question: str):
    sql = generate_sql(question)
    print(f"Generated SQL:\n{sql}\n")

    validate_sql(sql)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return columns, rows