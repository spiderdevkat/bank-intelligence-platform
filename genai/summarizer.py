import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.postgres_client import get_connection
from genai.gemini_client import ask


def get_daily_fraud_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            COUNT(*) AS total_transactions,
            SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS fraud_count,
            SUM(amount) AS total_volume,
            SUM(CASE WHEN is_fraud THEN amount ELSE 0 END) AS fraud_volume
        FROM fact_transactions
    """)
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return {
        "total_transactions": row[0],
        "fraud_count": row[1],
        "total_volume": float(row[2]),
        "fraud_volume": float(row[3]),
    }


def generate_summary():
    stats = get_daily_fraud_stats()

    prompt = f"""
You are a risk analyst assistant. Write a brief, plain-English summary
(3-4 sentences) of this bank's current transaction/fraud snapshot for
a non-technical manager. Be factual, don't speculate beyond the numbers.

Stats:
- Total transactions: {stats['total_transactions']}
- Fraud-flagged transactions: {stats['fraud_count']}
- Total transaction volume: ${stats['total_volume']:.2f}
- Fraud transaction volume: ${stats['fraud_volume']:.2f}
"""
    return ask(prompt)


if __name__ == "__main__":
    print(generate_summary())