import json
import time
import uuid
from typing import Dict, Any

from confluent_kafka import Producer

KAFKA_BROKER = "localhost:9092"

producer = Producer({
    "bootstrap.servers": KAFKA_BROKER,
    "enable.idempotence": True,
    "acks": "all",
    "retries": 5,
    "linger.ms": 5,
    "batch.size": 32768,
})


def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered to {msg.topic()} [{msg.partition()}]")


class MessageBus:

    @staticmethod
    def publish(
        topic: str,
        key: str,
        value: Dict[str, Any],
        headers: Dict[str, str] = None
    ):
        headers = headers or {}

        headers.update({
            "event_id": str(uuid.uuid4()),
            "retry_count": "0",
        })

        producer.produce(
            topic=topic,
            key=key,
            value=json.dumps(value),
            headers=[(k, v.encode()) for k, v in headers.items()],
            on_delivery=delivery_report
        )

        producer.poll(0)

    @staticmethod
    def publish_retry(
        topic: str,
        value: Dict[str, Any],
        headers: Dict[str, str],
        retry_count: int
    ):
        delay_topic = f"{topic}.retry.{retry_count}"

        headers["retry_count"] = str(retry_count)

        producer.produce(
            topic=delay_topic,
            key=headers.get("event_id"),
            value=json.dumps(value),
            headers=[(k, v.encode()) for k, v in headers.items()],
        )

    @staticmethod
    def publish_dlq(
        topic: str,
        value: Dict[str, Any],
        headers: Dict[str, str],
        error: str
    ):
        dlq_topic = f"{topic}.dlq"

        headers["error"] = error

        producer.produce(
            topic=dlq_topic,
            key=headers.get("event_id"),
            value=json.dumps(value),
            headers=[(k, v.encode()) for k, v in headers.items()],
        )