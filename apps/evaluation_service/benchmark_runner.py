import asyncio
from typing import List, Dict, Any

from infrastructure.observability.logging import get_logger
from .evaluator import Evaluator

logger = get_logger(__name__)


class BenchmarkRunner:
    def __init__(self):
        self.evaluator = Evaluator()

    async def run(self, dataset: List[Dict[str, Any]]) -> List[Dict]:
        logger.info("Running benchmark", size=len(dataset))

        tasks = [self.evaluator.evaluate(item) for item in dataset]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        return self._handle_results(results)

    def _handle_results(self, results):
        processed = []

        for r in results:
            if isinstance(r, Exception):
                processed.append({"error": str(r)})
            else:
                processed.append(r)

        return processed