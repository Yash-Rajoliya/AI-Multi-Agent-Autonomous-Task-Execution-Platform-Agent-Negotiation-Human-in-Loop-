class CostTracker:
    def __init__(self):
        self.total_cost = 0

    def add_cost(self, amount: float):
        self.total_cost += amount

    def get_cost(self):
        return self.total_cost