import logging
from typing import Optional

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "gpt-4"
ROUTING_MAP = {
    "cheap": "gpt-3.5",
    "fast": "gpt-3.5",
    "reasoning": "gpt-4",
    "complex": "gpt-4",
}


class ModelRouter:

    def __init__(
        self,
        custom_routes: Optional[dict[str, str]] = None,
        default_model: str = DEFAULT_MODEL,
    ):
        self.routes = {**ROUTING_MAP, **(custom_routes or {})}
        self.default_model = default_model

    def route(self, task_type: Optional[str] = None) -> str:
        if not task_type:
            logger.debug(
                "No task_type provided. Routing to default model: %s",
                self.default_model,
            )
            return self.default_model

        normalized_task = task_type.strip().lower()
        selected_model = self.routes.get(normalized_task, self.default_model)

        logger.debug(
            "Routed task_type '%s' (normalized: '%s') to model: %s",
            task_type,
            normalized_task,
            selected_model,
        )
        return selected_model