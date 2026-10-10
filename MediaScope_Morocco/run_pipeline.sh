#!/usr/bin/env bash
set -e
python app/scrapers/batch_ingest.py
python app/pipeline/silver_transform.py
python app/quality/data_quality.py
python app/pipeline/gold_transform.py
python app/warehouse/load_to_postgres.py
