# infrastructure/messaging/consumers/__init__.py

"""
Message consumer infrastructure.

Responsible for:
- Consuming distributed events
- Processing task queues
- Handling async workflow messages
- Event-driven execution triggers
- Queue subscription management
"""

__all__ = [
    "task_consumer",
]