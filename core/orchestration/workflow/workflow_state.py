from typing import Dict


class WorkflowState:
    def __init__(self):
        self.state: Dict = {}

    def update(self, key, value):
        self.state[key] = value

    def get(self, key):
        return self.state.get(key)

    def dump(self):
        return self.state