import os

import pandas as pd
from sqlalchemy import create_engine

DB_URL = "postgresql+psycopg2://news_user:news_pass@postgres:5432/news_dw"
GOLD_DIR = "data/gold"
SILVER_FILE = "data/silver/articles_clean.csv"


def load_csv_if_exists(engine, path, table_name):
    if not os.path.exists(path):
        print(f"Skipped {table_name}: file not found")
        return
    df = pd.read_csv(path)
    with engine.begin() as connection:
        df.to_sql(table_name, connection, if_exists="replace", index=False)
    print(f"Loaded {table_name}: {len(df)} rows")


if __name__ == "__main__":
    engine = create_engine(DB_URL)
    load_csv_if_exists(engine, SILVER_FILE, "silver_articles")
    load_csv_if_exists(engine, os.path.join(GOLD_DIR, "articles_par_jour.csv"), "gold_articles_par_jour")
    load_csv_if_exists(engine, os.path.join(GOLD_DIR, "articles_par_source.csv"), "gold_articles_par_source")
    load_csv_if_exists(engine, os.path.join(GOLD_DIR, "articles_par_categorie.csv"), "gold_articles_par_categorie")
    load_csv_if_exists(engine, os.path.join(GOLD_DIR, "top_mots_cles.csv"), "gold_top_mots_cles")
