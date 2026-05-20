# infrastructure/messaging/publishers/__init__.py

"""
Message publisher infrastructure.

Responsible for:
- Publishing workflow events
- Dispatching task messages
- Emitting orchestration signals
- Event stream production
- Queue message delivery
"""

__all__ = [
    "task_publisher",
]