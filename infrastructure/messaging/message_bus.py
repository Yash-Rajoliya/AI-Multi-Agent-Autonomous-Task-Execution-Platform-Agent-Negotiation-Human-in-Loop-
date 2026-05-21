import json
import logging
import uuid
from typing import Any

from confluent_kafka import Producer

from infrastructure.config.settings import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

producer = Producer(
    {
        "bootstrap.servers": settings.KAFKA_BROKER,
        "enable.idempotence": True,
        "acks": "all",
        "retries": 5,
        "linger.ms": 5,
        "batch.size": 32768,
    },
)


def delivery_report(err: Exception | None, msg: Any) -> None:
    """Kafka delivery callback."""
    if err:
        logger.error("Delivery failed: %s", err)
    else:
        logger.info(
            "Delivered message topic=%s partition=%s",
            msg.topic(),
            msg.partition(),
        )


class MessageBus:
    """Kafka message bus abstraction."""

    @staticmethod
    def publish(
        topic: str,
        key: str,
        value: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> None:
        """Publish message to Kafka topic."""
        message_headers = headers or {}

        message_headers.update(
            {
                "event_id": str(uuid.uuid4()),
                "retry_count": "0",
            },
        )

        producer.produce(
            topic=topic,
            key=key,
            value=json.dumps(value),
            headers=[
                (k, v.encode("utf-8"))
                for k, v in message_headers.items()
            ],
            on_delivery=delivery_report,
        )

        producer.poll(0)

    @staticmethod
    def publish_retry(
        topic: str,
        value: dict[str, Any],
        headers: dict[str, str],
        retry_count: int,
    ) -> None:
        """Publish retry event."""
        delay_topic = f"{topic}.retry.{retry_count}"

        retry_headers = headers.copy()
        retry_headers["retry_count"] = str(retry_count)

        producer.produce(
            topic=delay_topic,
            key=retry_headers.get("event_id"),
            value=json.dumps(value),
            headers=[
                (k, v.encode("utf-8"))
                for k, v in retry_headers.items()
            ],
        )

        producer.poll(0)

        logger.warning(
            "Published retry event topic=%s retry_count=%s",
            delay_topic,
            retry_count,
        )

    @staticmethod
    def publish_dlq(
        topic: str,
        value: dict[str, Any],
        headers: dict[str, str],
        error: str,
    ) -> None:
        """Publish failed event to DLQ."""
        dlq_topic = f"{topic}.dlq"

        dlq_headers = headers.copy()
        dlq_headers["error"] = error

        producer.produce(
            topic=dlq_topic,
            key=dlq_headers.get("event_id"),
            value=json.dumps(value),
            headers=[
                (k, v.encode("utf-8"))
                for k, v in dlq_headers.items()
            ],
        )

        producer.poll(0)

        logger.error(
            "Published message to DLQ topic=%s error=%s",
            dlq_topic,
            error,
        )