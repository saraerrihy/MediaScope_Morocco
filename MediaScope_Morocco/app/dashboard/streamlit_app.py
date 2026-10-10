import json
import os

import pandas as pd
import streamlit as st

st.set_page_config(page_title="MediaScope Morocco", layout="wide")
st.title("MediaScope Morocco")
st.caption("Plateforme Big Data d’analyse des tendances médiatiques marocaines et internationales")

GOLD_DIR = "data/gold"
SILVER_FILE = "data/silver/articles_clean.csv"
QUALITY_FILE = os.path.join(GOLD_DIR, "data_quality_report.json")

col1, col2, col3, col4 = st.columns(4)

if os.path.exists(SILVER_FILE):
    df = pd.read_csv(SILVER_FILE)
    col1.metric("Articles collectés", len(df))
    col2.metric("Sources", df["source"].nunique() if "source" in df.columns else 0)
    col3.metric("Catégories", df["category"].nunique() if "category" in df.columns else 0)
    valid_content = int(df["is_valid_content"].fillna(False).astype(bool).sum()) if "is_valid_content" in df.columns else 0
    col4.metric("Contenu valide", valid_content)

    st.subheader("Aperçu Silver")
    st.dataframe(df.head(20), use_container_width=True)
else:
    st.warning("Aucune donnée Silver disponible pour le moment.")

if os.path.exists(QUALITY_FILE):
    with open(QUALITY_FILE, "r", encoding="utf-8") as f:
        quality = json.load(f)
    st.subheader("Contrôles qualité")
    q1, q2, q3 = st.columns(3)
    q1.metric("Complétude titre", f"{quality.get('completude_titre', 0)}%")
    q2.metric("Validité date", f"{quality.get('validite_date', 0)}%")
    q3.metric("URLs dupliquées", quality.get("duplicate_urls", 0))

source_file = os.path.join(GOLD_DIR, "articles_par_source.csv")
if os.path.exists(source_file):
    st.subheader("Nombre d'articles par source")
    source_df = pd.read_csv(source_file)
    if not source_df.empty:
        st.bar_chart(source_df.set_index("source"))

category_file = os.path.join(GOLD_DIR, "articles_par_categorie.csv")
if os.path.exists(category_file):
    st.subheader("Nombre d'articles par catégorie")
    cat_df = pd.read_csv(category_file)
    if not cat_df.empty:
        st.bar_chart(cat_df.set_index("category"))

day_file = os.path.join(GOLD_DIR, "articles_par_jour.csv")
if os.path.exists(day_file):
    st.subheader("Évolution journalière")
    day_df = pd.read_csv(day_file)
    if not day_df.empty:
        st.line_chart(day_df.set_index("date_only"))

keywords_file = os.path.join(GOLD_DIR, "top_mots_cles.csv")
if os.path.exists(keywords_file):
    st.subheader("Top mots-clés")
    kw_df = pd.read_csv(keywords_file)
    st.dataframe(kw_df, use_container_width=True)
