import json


class CheckpointManager:
    def __init__(self, filepath: str = "checkpoint.json"):
        self.filepath = filepath

    def save(self, state: dict):
        with open(self.filepath, "w") as f:
            json.dump(state, f)

    def load(self):
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}