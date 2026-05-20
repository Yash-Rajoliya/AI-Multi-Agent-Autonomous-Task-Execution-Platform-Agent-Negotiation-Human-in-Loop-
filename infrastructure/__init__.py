# infrastructure/__init__.py

"""
Infrastructure layer for the AI Multi-Agent Autonomous Task Execution Platform.

Provides foundational platform services including:

- Messaging and event streaming
- Database integrations
- Vector database adapters
- LLM provider abstractions
- Redis caching and state management
- Security and policy enforcement
- Observability and monitoring
- Centralized configuration management
"""

__version__ = "1.0.0"

__all__ = [
    "config",
    "database",
    "llm",
    "messaging",
    "observability",
    "redis",
    "security",
    "vector_db",
]
