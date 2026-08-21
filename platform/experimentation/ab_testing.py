import random


class ABTesting:
    def __init__(self):
        self.experiments = {}

    def create_experiment(self, name: str, variants: list):
        self.experiments[name] = variants

    def assign(self, name: str):
        variants = self.experiments.get(name, [])
        return random.choice(variants) if variants else None