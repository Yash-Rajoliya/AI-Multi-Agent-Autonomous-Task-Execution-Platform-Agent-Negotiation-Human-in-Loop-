from typing import Dict, Any

from infrastructure.observability.logging import get_logger
from .scoring_engine import ScoringEngine

logger = get_logger(__name__)


class Evaluator:
    def __init__(self):
        self.scoring_engine = ScoringEngine()

    async def evaluate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Starting evaluation")

        scores = await self.scoring_engine.score(input_data)

        return {
            "scores": scores,
            "status": "completed"
        }