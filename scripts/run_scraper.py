import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scraper.edgar_scraper import fetch_filings, save_filings_to_mongo
from scraper.finnhub_client import fetch_company_news, save_news_to_mongo
from scraper.fred_client import fetch_series, save_fred_series_to_mongo
from scraper.frankfurter_client import fetch_exchange_rates, save_exchange_rates_to_mongo


def main():
    cik = "0000320193"  # Apple
    symbol = "AAPL"

    print(f"Fetching SEC filings for CIK {cik}...")
    filings = fetch_filings(cik=cik, count=10)
    filings_saved = save_filings_to_mongo(filings, cik=cik)
    print(f"  -> saved {filings_saved} filings")

    print(f"Fetching news for {symbol}...")
    news = fetch_company_news(symbol=symbol, from_date="2026-06-01", to_date="2026-07-09")
    news_saved = save_news_to_mongo(news, symbol=symbol)
    print(f"  -> saved {news_saved} news articles")

    print("Fetching Fed Funds Rate (FRED)...")
    rates = fetch_series(series_id="DFF", start_date="2026-06-01", end_date="2026-07-09")
    rates_saved = save_fred_series_to_mongo(rates, series_id="DFF")
    print(f"  -> saved {rates_saved} rate observations")

    print("Fetching FX rates (Frankfurter)...")
    fx = fetch_exchange_rates(date="latest", base_currency="USD")
    save_exchange_rates_to_mongo(fx, base_currency="USD")
    print("  -> saved FX snapshot")

    print("\nDone. All raw data landed in MongoDB (bank_intelligence database).")


if __name__ == "__main__":
    main()