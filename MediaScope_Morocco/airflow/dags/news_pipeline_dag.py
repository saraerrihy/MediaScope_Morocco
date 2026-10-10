from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

DEFAULT_ARGS = {
    "owner": "maryam",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="news_bigdata_pipeline",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2026, 5, 1),
    schedule_interval="@hourly",
    catchup=False,
    description="Pipeline Big Data de scraping et analyse d'articles",
) as dag:
    batch_scraping = BashOperator(
        task_id="batch_scraping",
        bash_command="cd /project && python app/scrapers/batch_ingest.py",
    )

    silver_transform = BashOperator(
        task_id="silver_transform",
        bash_command="cd /project && python app/pipeline/silver_transform.py",
    )

    data_quality = BashOperator(
        task_id="data_quality",
        bash_command="cd /project && python app/quality/data_quality.py",
    )

    gold_transform = BashOperator(
        task_id="gold_transform",
        bash_command="cd /project && python app/pipeline/gold_transform.py",
    )

    load_warehouse = BashOperator(
        task_id="load_warehouse",
        bash_command="cd /project && python app/warehouse/load_to_postgres.py",
    )

    batch_scraping >> silver_transform >> data_quality >> gold_transform >> load_warehouse
