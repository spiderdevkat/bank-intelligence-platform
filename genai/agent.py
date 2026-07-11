import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import joblib
import pandas as pd
from google.genai import types

from genai.gemini_client import client
from genai.text_to_sql import generate_sql, validate_sql, UnsafeQueryError
from genai.rag import rag_answer
from db.postgres_client import get_connection

rf_model = joblib.load("ml/models/fraud_random_forest.joblib")


def query_database(question: str) -> str:
    """Answer a question about transactions, customers, or accounts by
    generating and running a safe, validated SQL query against the
    banking database."""
    try:
        sql = generate_sql(question)
        validate_sql(sql)
    except UnsafeQueryError as e:
        return f"Query blocked for safety: {e}"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return f"SQL used: {sql}\nColumns: {columns}\nResults: {rows[:20]}"


def search_news(question: str) -> str:
    """Search recent scraped financial news using semantic similarity search."""
    return rag_answer(question)


def score_account_fraud_risk(account_id: str) -> str:
    """Given an account_id, compute an aggregate fraud risk score using
    the trained Random Forest model."""
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM fact_transactions WHERE account_id = %s", conn, params=(account_id,))
    conn.close()

    if df.empty:
        return f"No transactions found for account {account_id}."

    features = df[["amount"]].copy()
    features["hour_of_day"] = pd.to_datetime(df["transaction_timestamp"]).dt.hour
    features["day_of_week"] = pd.to_datetime(df["transaction_timestamp"]).dt.dayofweek
    for channel in ["ATM", "BRANCH", "CARD", "ONLINE", "WIRE"]:
        features[f"channel_{channel}"] = (df["channel"] == channel).astype(int)
    for ttype in ["DEPOSIT", "PAYMENT", "TRANSFER", "WITHDRAWAL"]:
        features[f"type_{ttype}"] = (df["transaction_type"] == ttype).astype(int)

    probs = rf_model.predict_proba(features)[:, 1]
    return (f"Account {account_id}: {len(df)} transactions analyzed. "
            f"Average fraud probability: {probs.mean():.2%}. "
            f"Highest single-transaction fraud probability: {probs.max():.2%}.")


AVAILABLE_TOOLS = {
    "query_database": query_database,
    "search_news": search_news,
    "score_account_fraud_risk": score_account_fraud_risk,
}


def investigate(question: str, max_steps: int = 5) -> str:
    """A minimal manual tool-calling loop: ask Gemini, if it wants to call
    a tool we run it and feed the result back, repeat until it gives a
    final text answer."""
    contents = [types.Content(role="user", parts=[types.Part(text=question)])]

    for step in range(max_steps):
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=contents,
            config=types.GenerateContentConfig(
                tools=[query_database, search_news, score_account_fraud_risk],
                system_instruction=(
                    "You are a fraud investigation assistant for a bank. "
                    "Use the available tools as needed, then give a clear "
                    "final summary for a bank analyst."
                ),
            ),
        )

        candidate = response.candidates[0]
        function_calls = [p.function_call for p in candidate.content.parts if p.function_call]

        if not function_calls:
            return response.text

        contents.append(candidate.content)

        function_response_parts = []
        for fc in function_calls:
            print(f"[step {step}] Calling tool: {fc.name}({dict(fc.args)})")
            tool_fn = AVAILABLE_TOOLS[fc.name]
            result = tool_fn(**fc.args)
            function_response_parts.append(
                types.Part.from_function_response(name=fc.name, response={"result": result})
            )

        contents.append(types.Content(role="user", parts=function_response_parts))

    return "Reached max steps without a final answer."