import json
import logging
from collections.abc import Callable
from typing import Any

from confluent_kafka import Consumer, KafkaException, Message

from infrastructure.config.settings import get_settings
from infrastructure.messaging.message_bus import MessageBus

logger = logging.getLogger(__name__)

settings = get_settings()


class BaseConsumer:
    """Reusable Kafka consumer base class."""

    def __init__(
        self,
        topic: str,
        group_id: str,
    ) -> None:
        self.topic = topic

        self.consumer = Consumer(
            {
                "bootstrap.servers": settings.KAFKA_BROKER,
                "group.id": group_id,
                "auto.offset.reset": "earliest",
                "enable.auto.commit": False,
            },
        )

        self.consumer.subscribe([topic])

    def start(
        self,
        handler: Callable[
            [dict[str, Any], dict[str, str]],
            None,
        ],
    ) -> None:
        """Start Kafka consumer polling loop."""
        logger.info(
            "Consumer started topic=%s",
            self.topic,
        )

        while True:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                raise KafkaException(msg.error())

            try:
                value = json.loads(msg.value().decode("utf-8"))

                headers = self._parse_headers(
                    msg.headers(),
                )

                if self._is_duplicate(
                    headers.get("event_id"),
                ):
                    self.consumer.commit(msg)
                    continue

                handler(value, headers)

                self.consumer.commit(msg)

            except Exception as exc:
                logger.exception(
                    "Failed processing Kafka message",
                )

                self._handle_failure(
                    msg=msg,
                    error=str(exc),
                )

    @staticmethod
    def _parse_headers(
        headers: list[tuple[str, bytes]] | None,
    ) -> dict[str, str]:
        """Parse Kafka headers."""
        if not headers:
            return {}

        return {
            key: value.decode("utf-8")
            for key, value in headers
        }

    @staticmethod
    def _is_duplicate(event_id: str | None) -> bool:
        """Placeholder idempotency check."""
        if not event_id:
            return False

        # TODO: Replace with Redis or database check
        return False

    def _handle_failure(
        self,
        msg: Message,
        error: str,
    ) -> None:
        """Handle retry and DLQ flow."""
        headers = self._parse_headers(
            msg.headers(),
        )

        retry_count = int(
            headers.get("retry_count", "0"),
        )

        value = json.loads(
            msg.value().decode("utf-8"),
        )

        if retry_count < 3:
            MessageBus.publish_retry(
                topic=self.topic,
                value=value,
                headers=headers,
                retry_count=retry_count + 1,
            )

        else:
            MessageBus.publish_dlq(
                topic=self.topic,
                value=value,
                headers=headers,
                error=error,
            )

        self.consumer.commit(msg)