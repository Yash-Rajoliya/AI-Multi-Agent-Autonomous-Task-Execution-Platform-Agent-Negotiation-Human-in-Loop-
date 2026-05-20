import json
from typing import Callable

from confluent_kafka import Consumer, KafkaException

from infrastructure.messaging.message_bus import MessageBus


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
        while True:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                raise KafkaException(msg.error())

            try:
                value = json.loads(msg.value())
                headers = self._parse_headers(msg.headers())

                # Idempotency check
                if self._is_duplicate(headers.get("event_id")):
                    self.consumer.commit(msg)
                    continue

                handler(value, headers)

                self.consumer.commit(msg)

            except Exception as e:
                self._handle_failure(msg, str(e))

    def _parse_headers(self, headers):
        return {k: v.decode() for k, v in headers} if headers else {}

    def _is_duplicate(self, event_id: str) -> bool:
        # TODO: Replace with Redis/DB
        return False

    def _handle_failure(self, msg, error: str):
        headers = self._parse_headers(msg.headers())
        retry_count = int(headers.get("retry_count", 0))

        if retry_count < 3:
            MessageBus.publish_retry(
                topic=self.topic,
                value=json.loads(msg.value()),
                headers=headers,
                retry_count=retry_count + 1
            )
        else:
            MessageBus.publish_dlq(
                topic=self.topic,
                value=json.loads(msg.value()),
                headers=headers,
                error=error
            )

        self.consumer.commit(msg)