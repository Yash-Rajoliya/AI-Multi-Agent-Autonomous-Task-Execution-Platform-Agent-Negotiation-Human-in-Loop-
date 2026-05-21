from typing import Any

from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

from infrastructure.config.settings import get_settings

settings = get_settings()

schema_registry_client = SchemaRegistryClient(
    {"url": settings.SCHEMA_REGISTRY_URL},
)


class EventSchemaManager:
    """Manages Kafka Avro schemas."""

    def __init__(self) -> None:
        self._schemas: dict[str, AvroSerializer] = {}

    def register_schema(
        self,
        subject: str,
        schema_str: str,
    ) -> None:
        """Register Avro schema."""
        self._schemas[subject] = AvroSerializer(
            schema_registry_client,
            schema_str,
        )

    def serialize(
        self,
        subject: str,
        data: dict[str, Any],
    ) -> bytes:
        """Serialize payload using Avro schema."""
        if subject not in self._schemas:
            raise ValueError(
                f"Schema not registered for subject={subject}",
            )

        return self._schemas[subject](data, None)


event_schema_manager = EventSchemaManager()

TASK_EVENT_V1 = """
{
  "type": "record",
  "name": "TaskEvent",
  "namespace": "ai.platform",
  "fields": [
    {"name": "event_id", "type": "string"},
    {"name": "event_type", "type": "string"},
    {"name": "version", "type": "int"},
    {"name": "timestamp", "type": "long"},
    {"name": "tenant_id", "type": "string"},
    {
      "name": "payload",
      "type": {
        "type": "map",
        "values": "string"
      }
    }
  ]
}
"""

event_schema_manager.register_schema(
    "task-events-value",
    TASK_EVENT_V1,
)