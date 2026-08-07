class CostPolicy:
    def __init__(self, limit=100):
        self.limit = limit

    def check(self, cost):
        if cost > self.limit:
            raise Exception("Cost exceeded")