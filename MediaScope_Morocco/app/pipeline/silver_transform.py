import glob
import json
import os
import re

import pandas as pd

BRONZE_DIR = "data/bronze"
SILVER_DIR = "data/silver"


def normalize_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", str(text))
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_bronze_records():
    records = []
    for path in glob.glob(os.path.join(BRONZE_DIR, "*.json")):
        with open(path, "r", encoding="utf-8") as f:
            content = json.load(f)
            if isinstance(content, list):
                records.extend(content)
            elif isinstance(content, dict):
                records.append(content)
    return records


def build_silver():
    os.makedirs(SILVER_DIR, exist_ok=True)
    records = load_bronze_records()
    if not records:
        print("No bronze data found.")
        return

    df = pd.DataFrame(records)
    for col in ["title", "author", "category", "content", "source", "url", "language"]:
        if col not in df.columns:
            df[col] = ""
        df[col] = df[col].fillna("").astype(str).apply(normalize_text)

    if "publication_date" not in df.columns:
        df["publication_date"] = ""
    df["publication_date"] = pd.to_datetime(df["publication_date"], errors="coerce")
    if "scraping_date" not in df.columns:
        df["scraping_date"] = ""
    df["scraping_date"] = pd.to_datetime(df["scraping_date"], errors="coerce")

    df = df.drop_duplicates(subset=["url"], keep="first")
    df["word_count"] = df["content"].apply(lambda x: len(str(x).split()))
    df["is_valid_content"] = df["word_count"] >= 30
    df["date_only"] = df["publication_date"].dt.date

    out_path = os.path.join(SILVER_DIR, "articles_clean.csv")
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"Saved silver dataset to {out_path} with {len(df)} rows")


if __name__ == "__main__":
    build_silver()
