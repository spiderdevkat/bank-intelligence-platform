import os

import requests
from dotenv import load_dotenv

from datetime import datetime

from scraper.mongo_client import get_db

load_dotenv()

API_KEY = os.environ.get("FINNHUB_API_KEY")
BASE_URL = "https://finnhub.io/api/v1"


def fetch_company_news(symbol: str, from_date: str, to_date: str):
    if not API_KEY:
        raise RuntimeError("FINNHUB_API_KEY not found — check your .env file")

    url = f"{BASE_URL}/company-news"
    params = {"symbol": symbol, "from": from_date, "to": to_date, "token": API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def save_news_to_mongo(news_items, symbol: str):
    db = get_db()
    collection = db.raw_news

    for item in news_items:
        item["symbol"] = symbol
        item["scraped_at"] = datetime.now()

    if news_items:
        result = collection.insert_many(news_items)
        return len(result.inserted_ids)
    return 0