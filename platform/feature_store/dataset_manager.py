from typing import Dict


class DatasetManager:
    def __init__(self):
        self.datasets: Dict[str, list] = {}

    def create_dataset(self, name: str):
        self.datasets[name] = []

    def add_data(self, name: str, record):
        if name not in self.datasets:
            raise ValueError("Dataset not found")
        self.datasets[name].append(record)

    def get_dataset(self, name: str):
        return self.datasets.get(name, [])