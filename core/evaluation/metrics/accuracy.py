from typing import List


class AccuracyMetric:
    """
    Measures exact match / correctness
    """

    def compute(self, predictions: List[str], ground_truths: List[str]) -> float:
        if len(predictions) != len(ground_truths):
            raise ValueError("Mismatched lengths")

        correct = sum(
            1 for p, g in zip(predictions, ground_truths)
            if p.strip().lower() == g.strip().lower()
        )

        return correct / len(predictions) if predictions else 0.0