class CostMetric:
    """
    Tracks token / API cost usage
    """

    def __init__(self):
        self.total_cost = 0.0

    def add(self, cost: float):
        self.total_cost += cost

    def value(self):
        return self.total_cost