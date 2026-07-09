import requests

from datetime import datetime

from scraper.mongo_client import get_db

BASE_URL = "https://api.frankfurter.dev/v1"


def fetch_exchange_rates(date: str, base_currency: str = "USD"):
    """date format: YYYY-MM-DD, or 'latest' for the most recent rate."""
    url = f"{BASE_URL}/{date}"
    params = {"base": base_currency}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def save_exchange_rates_to_mongo(rates_response, base_currency: str):
    db = get_db()
    collection = db.raw_market_data

    doc = {
        "source": "Frankfurter",
        "base_currency": base_currency,
        "date": rates_response["date"],
        "rates": rates_response["rates"],
        "scraped_at": datetime.now(),
    }
    result = collection.update_one(
        {"source": "Frankfurter", "date": rates_response["date"]},
        {"$set": doc},
        upsert=True,
    )
    return result.upserted_id or "updated"