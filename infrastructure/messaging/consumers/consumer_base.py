import json
import logging
from typing import Callable, Dict, Optional

from confluent_kafka import Consumer, KafkaException

from infrastructure.messaging.message_bus import MessageBus

logger = logging.getLogger(__name__)


class BaseConsumer:

    def __init__(self, topic: str, group_id: str):
        self.topic = topic

        self.consumer = Consumer({
            "bootstrap.servers": "localhost:9092",
            "group.id": group_id,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False
        })

        self.consumer.subscribe([topic])

    def start(self, handler: Callable):
        try:
            while True:
                msg = self.consumer.poll(1.0)

                if msg is None:
                    continue

                if msg.error():
                    logger.error(f"Kafka consumer error: {msg.error()}")
                    raise KafkaException(msg.error())

                try:
                    value = json.loads(msg.value().decode("utf-8"))
                    headers = self._parse_headers(msg.headers())

                    # Idempotency check
                    if self._is_duplicate(headers.get("event_id")):
                        self.consumer.commit(msg, asynchronous=False)
                        continue

                    handler(value, headers)
                    self.consumer.commit(msg, asynchronous=False)

                except Exception as e:
                    logger.exception(f"Error processing message from topic {self.topic}: {e}")
                    self._handle_failure(msg, str(e))
        finally:
            self.consumer.close()

    def _parse_headers(self, headers) -> Dict[str, str]:
        if not headers:
            return {}
        
        parsed = {}
        for k, v in headers:
            if v is not None:
                parsed[k] = v.decode("utf-8") if isinstance(v, bytes) else str(v)
            else:
                parsed[k] = ""
        return parsed

    def _is_duplicate(self, event_id: Optional[str]) -> bool:
        # TODO: Replace with Redis/DB
        return False

    def _handle_failure(self, msg, error: str):
        try:
            headers = self._parse_headers(msg.headers())
            retry_count = int(headers.get("retry_count", 0))
            value = json.loads(msg.value().decode("utf-8"))

            if retry_count < 3:
                MessageBus.publish_retry(
                    topic=self.topic,
                    value=value,
                    headers=headers,
                    retry_count=retry_count + 1
                )
            else:
                MessageBus.publish_dlq(
                    topic=self.topic,
                    value=value,
                    headers=headers,
                    error=error
                )

            self.consumer.commit(msg, asynchronous=False)
        except Exception as retry_err:
            logger.critical(f"Failed to process retry/DLQ fallback: {retry_err}")