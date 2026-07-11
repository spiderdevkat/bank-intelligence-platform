import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    google_api_key=os.environ.get("GEMINI_API_KEY"),
)

SCHEMA_CONTEXT = """
dimension_customer (customer_sk, customer_id, full_name, email, phone,
    country, risk_tier, valid_from, valid_to, is_current, created_at)

dimension_account (account_id, customer_id, parent_account_id,
    account_number, account_type, currency, status, opened_at)

fact_transactions (transaction_id, customer_id, customer_sk, account_id,
    counterparty_account_id, market_condition_id, transaction_type,
    channel, amount, currency, transaction_timestamp, is_fraud,
    fraud_label, created_at)
"""

sql_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a SQL assistant for a banking analytics database. "
               "Only these tables/columns exist:\n{schema}\n"
               "Generate ONLY a single PostgreSQL SELECT statement. "
               "No explanation, no markdown, no code fences."),
    ("human", "{question}"),
])

sql_chain = sql_prompt | llm | StrOutputParser()


def generate_sql_langchain(question: str) -> str:
    return sql_chain.invoke({"schema": SCHEMA_CONTEXT, "question": question})

if __name__=="__main__":
    prompt = ChatPromptTemplate.from_template("Answer in one sentence: {question}")
    chain = prompt | llm | StrOutputParser()

    result = chain.invoke({"question": "What is a recursive CTE?"})
    print(result)