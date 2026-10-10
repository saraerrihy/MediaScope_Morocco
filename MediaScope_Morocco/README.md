# MediaScope Morocco

## Plateforme Big Data d’analyse des tendances médiatiques marocaines et internationales

**MediaScope Morocco** est un projet d’architecture de données dédié à la collecte, au nettoyage, à l’analyse et à la visualisation d’articles d’actualité.  
Le pipeline implémente une architecture **Médaillon** avec trois zones :
- **Bronze** : données brutes JSON issues du scraping
- **Silver** : données nettoyées et standardisées
- **Gold** : tables analytiques prêtes pour la visualisation

## Fonctionnalités

- Web scraping multi-sources via RSS + parsing HTML
- Ingestion batch
- Producteur / consommateur Kafka pour le pseudo-streaming
- Data Lake local (`data/bronze`, `data/silver`, `data/gold`)
- Contrôles de qualité des données
- Chargement PostgreSQL
- Orchestration Airflow
- Dashboard Streamlit
- Déploiement Docker Compose

## Structure

```text
MediaScope_Morocco/
├── airflow/
│   └── dags/news_pipeline_dag.py
├── app/
│   ├── dashboard/streamlit_app.py
│   ├── pipeline/gold_transform.py
│   ├── pipeline/silver_transform.py
│   ├── quality/data_quality.py
│   ├── scrapers/batch_ingest.py
│   ├── scrapers/config.py
│   ├── scrapers/generic_scraper.py
│   ├── scrapers/kafka_consumer.py
│   ├── scrapers/kafka_producer.py
│   └── warehouse/load_to_postgres.py
├── config/sources.yaml
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── docker-compose.yml
├── Dockerfile.app
├── requirements.txt
├── run_pipeline.sh
└── sql/init.sql
```

## Lancement

### 1. Démarrer les conteneurs
```bash
docker compose up --build -d
```

### 2. Exécuter le pipeline manuellement
```bash
docker compose exec app python app/scrapers/batch_ingest.py
docker compose exec app python app/pipeline/silver_transform.py
docker compose exec app python app/quality/data_quality.py
docker compose exec app python app/pipeline/gold_transform.py
docker compose exec app python app/warehouse/load_to_postgres.py
```

### 3. Ouvrir les interfaces
- Streamlit : http://localhost:8501
- Airflow : http://localhost:8080

## Comptes par défaut

### Airflow
- utilisateur : `admin`
- mot de passe : `admin`

### PostgreSQL
- base : `news_dw`
- utilisateur : `news_user`
- mot de passe : `news_pass`

## Indicateurs produits

- nombre d’articles par jour
- nombre d’articles par source
- nombre d’articles par catégorie
- top mots-clés
- taux de complétude du titre
- validité de la date de publication

## Résultat attendu

Le projet permet de montrer une chaîne complète de données, depuis la collecte d’articles jusqu’à leur visualisation dans un dashboard analytique.

## Auteur
Projet personnalisé pour **Maryam Farhoune**.
