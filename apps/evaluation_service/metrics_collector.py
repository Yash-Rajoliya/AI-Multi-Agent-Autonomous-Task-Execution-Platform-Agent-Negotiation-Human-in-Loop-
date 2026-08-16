from typing import List, Dict

from infrastructure.observability.logging import get_logger

logger = get_logger(__name__)


class MetricsCollector:
    def aggregate(self, results: List[Dict]) -> Dict:
        logger.info("Aggregating metrics")

        summary = {
            "accuracy": 0,
            "latency": 0,
            "cost": 0,
            "count": len(results),
        }

        for r in results:
            scores = r.get("scores", {})
            summary["accuracy"] += scores.get("accuracy", 0)
            summary["latency"] += scores.get("latency", 0)
            summary["cost"] += scores.get("cost", 0)

        if summary["count"] > 0:
            summary["accuracy"] /= summary["count"]
            summary["latency"] /= summary["count"]
            summary["cost"] /= summary["count"]

        return summary