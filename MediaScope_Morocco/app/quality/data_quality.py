import json
import os

import pandas as pd

SILVER_FILE = "data/silver/articles_clean.csv"
REPORT_FILE = "data/gold/data_quality_report.json"


def run_quality_checks():
    if not os.path.exists(SILVER_FILE):
        print("Silver file not found.")
        return

    df = pd.read_csv(SILVER_FILE)
    total = len(df)
    report = {
        "total_articles": int(total),
        "articles_without_title": int(df["title"].fillna("").eq("").sum()) if "title" in df.columns else total,
        "articles_without_date": int(df["publication_date"].isna().sum()) if "publication_date" in df.columns else total,
        "articles_content_too_short": int((df["word_count"].fillna(0) < 30).sum()) if "word_count" in df.columns else total,
        "duplicate_urls": int(df["url"].duplicated().sum()) if "url" in df.columns else 0,
        "completude_titre": round((1 - (df["title"].fillna("").eq("").sum() / total)) * 100, 2) if total and "title" in df.columns else 0,
        "validite_date": round((1 - (df["publication_date"].isna().sum() / total)) * 100, 2) if total and "publication_date" in df.columns else 0,
    }

    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run_quality_checks()
