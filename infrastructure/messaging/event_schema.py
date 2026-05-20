import json
from typing import Dict, Any
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

SCHEMA_REGISTRY_URL = "http://localhost:8081"

schema_registry_client = SchemaRegistryClient({"url": SCHEMA_REGISTRY_URL})


class EventSchemaManager:
    def __init__(self):
        self._schemas = {}

    def register_schema(self, subject: str, schema_str: str):
        self._schemas[subject] = AvroSerializer(
            schema_registry_client,
            schema_str
        )

    def serialize(self, subject: str, data: Dict[str, Any]):
        if subject not in self._schemas:
            raise ValueError(f"Schema not registered for subject={subject}")
        return self._schemas[subject](data, None)


event_schema_manager = EventSchemaManager()


# Example schema
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
    {"name": "payload", "type": {"type": "map", "values": "string"}}
  ]
}
"""

event_schema_manager.register_schema("task-events-value", TASK_EVENT_V1)