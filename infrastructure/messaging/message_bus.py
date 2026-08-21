import json
import logging
import time
import uuid
from typing import Any, Dict, Optional

from confluent_kafka import Producer

logger = logging.getLogger(__name__)

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
        logger.error(f"Delivery failed: {err}")
    else:
        logger.info(f"Delivered to {msg.topic()} [{msg.partition()}]")


class MessageBus:

    @staticmethod
    def _encode_headers(headers: Dict[str, Any]) -> list:
        encoded = []
        for k, v in headers.items():
            encoded_val = v.encode("utf-8") if isinstance(v, str) else str(v).encode("utf-8") if v is not None else b""
            encoded.append((k, encoded_val))
        return encoded

    @classmethod
    def publish(
        cls,
        topic: str,
        key: str,
        value: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None
    ):
        headers = headers or {}
        headers.update({
            "event_id": headers.get("event_id") or str(uuid.uuid4()),
            "retry_count": headers.get("retry_count", "0"),
        })

        encoded_key = key.encode("utf-8") if isinstance(key, str) else key

        producer.produce(
            topic=topic,
            key=encoded_key,
            value=json.dumps(value),
            headers=cls._encode_headers(headers),
            on_delivery=delivery_report
        )
        producer.poll(0)

    @classmethod
    def publish_retry(
        cls,
        topic: str,
        value: Dict[str, Any],
        headers: Dict[str, str],
        retry_count: int
    ):
        delay_topic = f"{topic}.retry.{retry_count}"
        headers["retry_count"] = str(retry_count)

        key = headers.get("event_id")
        encoded_key = key.encode("utf-8") if isinstance(key, str) else key

        producer.produce(
            topic=delay_topic,
            key=encoded_key,
            value=json.dumps(value),
            headers=cls._encode_headers(headers),
            on_delivery=delivery_report
        )
        producer.flush()

    @classmethod
    def publish_dlq(
        cls,
        topic: str,
        value: Dict[str, Any],
        headers: Dict[str, str],
        error: str
    ):
        dlq_topic = f"{topic}.dlq"
        headers["error"] = error

        key = headers.get("event_id")
        encoded_key = key.encode("utf-8") if isinstance(key, str) else key

        producer.produce(
            topic=dlq_topic,
            key=encoded_key,
            value=json.dumps(value),
            headers=cls._encode_headers(headers),
            on_delivery=delivery_report
        )
        producer.flush()