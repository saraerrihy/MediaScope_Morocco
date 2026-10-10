import json
import os
from datetime import datetime

from kafka import KafkaConsumer

TOPIC = "news_articles"
BRONZE_DIR = "data/bronze"


def get_consumer():
    return KafkaConsumer(
        TOPIC,
        bootstrap_servers="kafka:9092",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="news-consumer-group",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )


if __name__ == "__main__":
    os.makedirs(BRONZE_DIR, exist_ok=True)
    consumer = get_consumer()
    for message in consumer:
        record = message.value
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
        path = os.path.join(BRONZE_DIR, f"stream_article_{ts}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        print(f"Saved streaming record to {path}")
