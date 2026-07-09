import os

import requests
from dotenv import load_dotenv

from datetime import datetime

from scraper.mongo_client import get_db

load_dotenv()

API_KEY = os.environ.get("FRED_API_KEY")
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"


def fetch_series(series_id: str, start_date: str, end_date: str):
    """series_id examples: DFF (Fed Funds Rate), CPIAUCSL (CPI)"""
    if not API_KEY:
        raise RuntimeError("FRED_API_KEY not found — check your .env file")

    params = {
        "series_id": series_id,
        "api_key": API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": end_date,
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()["observations"]

def save_fred_series_to_mongo(observations, series_id: str):
    db = get_db()
    collection = db.raw_market_data

    upserted_count = 0
    for obs in observations:
        doc = {
            "source": "FRED",
            "series_id": series_id,
            "date": obs["date"],
            "value": obs["value"],
            "scraped_at": datetime.now(),
        }
        result = collection.update_one(
            {"source": "FRED", "series_id": series_id, "date": obs["date"]},
            {"$set": doc},
            upsert=True,
        )
        if result.upserted_id or result.modified_count:
            upserted_count += 1
    return upserted_count