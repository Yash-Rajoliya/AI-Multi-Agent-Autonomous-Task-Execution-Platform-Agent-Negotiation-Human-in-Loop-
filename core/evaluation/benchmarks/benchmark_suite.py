from typing import Callable, List, Dict
from core.evaluation.metrics.accuracy import AccuracyMetric


class BenchmarkSuite:
    """
    Runs test datasets against a model/system
    """

    def __init__(self):
        self.tests: List[Dict] = []

    def add_test(self, input_data, expected_output):
        self.tests.append({
            "input": input_data,
            "expected": expected_output
        })

    async def run(self, model_fn: Callable):
        predictions = []
        ground_truths = []

        for test in self.tests:
            result = await model_fn(test["input"])
            predictions.append(result)
            ground_truths.append(test["expected"])

        accuracy = AccuracyMetric().compute(predictions, ground_truths)

        return {
            "accuracy": accuracy,
            "total_tests": len(self.tests)
        }