from typing import Dict, Any

from infrastructure.observability.logging import get_logger

logger = get_logger(__name__)


class ScoringEngine:
    def __init__(self):
        self.metrics = [
            self._accuracy,
            self._latency,
            self._cost,
        ]

    async def score(self, data: Dict[str, Any]) -> Dict[str, float]:
        scores = {}

        for metric in self.metrics:
            try:
                result = await metric(data)
                scores.update(result)
            except Exception as e:
                logger.error("Metric failed", metric=metric.__name__, error=str(e))

        return scores

    async def _accuracy(self, data):
        expected = data.get("expected")
        output = data.get("output")

        score = 1.0 if expected == output else 0.0
        return {"accuracy": score}

    async def _latency(self, data):
        latency = data.get("latency", 0)
        return {"latency": latency}

    async def _cost(self, data):
        tokens = data.get("tokens", 0)
        cost = tokens * 0.00001
        return {"cost": cost}