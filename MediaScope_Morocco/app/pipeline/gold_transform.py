import os
import re
from collections import Counter

import pandas as pd

SILVER_FILE = "data/silver/articles_clean.csv"
GOLD_DIR = "data/gold"
STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "have", "been", "will",
    "les", "des", "pour", "dans", "une", "est", "sur", "par", "avec", "plus",
    "من", "على", "في", "عن", "إلى", "هذا", "هذه"
}


def extract_keywords(series, top_n=20):
    text = " ".join(series.dropna().astype(str).tolist()).lower()
    tokens = re.findall(r"\b[\w\-]{4,}\b", text)
    tokens = [t for t in tokens if t not in STOPWORDS]
    return Counter(tokens).most_common(top_n)


def build_gold():
    os.makedirs(GOLD_DIR, exist_ok=True)
    if not os.path.exists(SILVER_FILE):
        print("Silver file not found.")
        return

    df = pd.read_csv(SILVER_FILE)
    if df.empty:
        print("Silver file is empty.")
        return

    if "date_only" in df.columns:
        articles_per_day = df.groupby("date_only").size().reset_index(name="nombre_articles")
        articles_per_day.to_csv(os.path.join(GOLD_DIR, "articles_par_jour.csv"), index=False, encoding="utf-8-sig")

    articles_per_source = df.groupby("source").size().reset_index(name="nombre_articles")
    articles_per_source.to_csv(os.path.join(GOLD_DIR, "articles_par_source.csv"), index=False, encoding="utf-8-sig")

    articles_per_category = df.groupby("category").size().reset_index(name="nombre_articles")
    articles_per_category.to_csv(os.path.join(GOLD_DIR, "articles_par_categorie.csv"), index=False, encoding="utf-8-sig")

    keywords = extract_keywords(df["title"].fillna("") + " " + df["content"].fillna(""))
    pd.DataFrame(keywords, columns=["mot_cle", "frequence"]).to_csv(
        os.path.join(GOLD_DIR, "top_mots_cles.csv"), index=False, encoding="utf-8-sig"
    )
    print("Gold tables generated.")


if __name__ == "__main__":
    build_gold()
