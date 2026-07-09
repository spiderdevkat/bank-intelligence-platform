import re

import requests
from bs4 import BeautifulSoup

from datetime import datetime

from scraper.mongo_client import get_db

USER_AGENT = "Devender Kataria devender20025090@gmail.com"

VALID_COUNTS = {10, 20, 40, 80, 100}

def fetch_filings(cik: str, filing_type: str = "10-K", count: int = 10):
    if count not in VALID_COUNTS:
        raise ValueError(f"count must be one of {sorted(VALID_COUNTS)} (SEC EDGAR silently ignores other values), got {count}")

    url = (
        "https://www.sec.gov/cgi-bin/browse-edgar"
        f"?action=getcompany&CIK={cik}&type={filing_type}&dateb=&owner=include&count={count}"
    )

    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    table = soup.find("table", summary="Results")
    if table is None:
        return []

    filings = []
    rows = table.find_all("tr")[1:]  # skip header row

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 4:
            continue

        filing_type_cell = cells[0].get_text(strip=True)
        doc_link_tag = cells[1].find("a", id="documentsbutton")
        doc_url = "https://www.sec.gov" + doc_link_tag["href"] if doc_link_tag else None
        description = cells[2].get_text(strip=True)
        filing_date = cells[3].get_text(strip=True)

        accession_match = re.search(r"Acc-no:\s*(\S+)", description)
        accession_number = accession_match.group(1) if accession_match else None

        filings.append({
            "filing_type": filing_type_cell,
            "accession_number": accession_number,
            "filing_date": filing_date,
            "document_url": doc_url,
            "description": description,
        })

    return filings

def save_filings_to_mongo(filings, cik: str):
    db = get_db()
    collection = db.raw_sec_filings

    upserted_count = 0
    for filing in filings:
        filing["cik"] = cik
        filing["scraped_at"] = datetime.now()
        result = collection.update_one(
            {"accession_number": filing["accession_number"]},
            {"$set": filing},
            upsert=True,
        )
        if result.upserted_id or result.modified_count:
            upserted_count += 1
    return upserted_count