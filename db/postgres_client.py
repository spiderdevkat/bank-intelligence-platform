import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

PG_HOST = "localhost"
PG_PORT = 5432
PG_DATABASE = "bank_intelligence"
PG_USER = "postgres"
PG_PASSWORD = os.environ.get("POSTGRES_PASSWORD")


def get_connection():
    if not PG_PASSWORD:
        raise RuntimeError("POSTGRES_PASSWORD not found — check your .env file")

    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
    )