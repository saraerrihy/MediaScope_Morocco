CREATE TABLE IF NOT EXISTS silver_articles (
    title TEXT,
    author TEXT,
    publication_date TEXT,
    category TEXT,
    content TEXT,
    source TEXT,
    url TEXT,
    scraping_date TEXT,
    language TEXT,
    word_count INTEGER,
    is_valid_content BOOLEAN,
    date_only TEXT
);

CREATE TABLE IF NOT EXISTS gold_articles_par_jour (
    date_only TEXT,
    nombre_articles INTEGER
);

CREATE TABLE IF NOT EXISTS gold_articles_par_source (
    source TEXT,
    nombre_articles INTEGER
);

CREATE TABLE IF NOT EXISTS gold_articles_par_categorie (
    category TEXT,
    nombre_articles INTEGER
);

CREATE TABLE IF NOT EXISTS gold_top_mots_cles (
    mot_cle TEXT,
    frequence INTEGER
);
