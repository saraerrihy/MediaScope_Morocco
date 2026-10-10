import json
from kafka import KafkaProducer

from app.scrapers.generic_scraper import scrape_from_rss

TOPIC = "news_articles"


def get_producer():
    return KafkaProducer(
        bootstrap_servers="kafka:9092",
        value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode("utf-8"),
    )


if __name__ == "__main__":
    producer = get_producer()
    for record in scrape_from_rss(limit_per_source=5):
        producer.send(TOPIC, record)
        print(f"Sent article: {record.get('title', '')[:60]}")
    producer.flush()
