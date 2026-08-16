import asyncio
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class StateManager:
    def __init__(self):
        self._store = {}

    async def fetch_pending_workflows(self) -> List[Dict[str, Any]]:
        # In real: DB query
        return [
            {
                "id": "wf-1",
                "steps": [
                    {"id": "node-1", "type": "agent"},
                    {"id": "node-2", "type": "tool"},
                ],
            }
        ]

    async def save_node_result(self, workflow_id: str, node_id: str, result: Any):
        logger.info(f"Saving result {workflow_id}:{node_id}")
        self._store.setdefault(workflow_id, {})[node_id] = result

    async def mark_completed(self, workflow_id: str):
        logger.info(f"Workflow completed: {workflow_id}")

    async def mark_failed(self, workflow_id: str, error: str):
        logger.error(f"Workflow failed: {workflow_id} | {error}")