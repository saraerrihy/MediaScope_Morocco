import json
import os
from datetime import datetime

from app.scrapers.generic_scraper import scrape_from_rss

BRONZE_DIR = "data/bronze"


def save_bronze(records):
    os.makedirs(BRONZE_DIR, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(BRONZE_DIR, f"articles_{ts}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(records)} records to {path}")


if __name__ == "__main__":
    records = scrape_from_rss(limit_per_source=10)
    save_bronze(records)
