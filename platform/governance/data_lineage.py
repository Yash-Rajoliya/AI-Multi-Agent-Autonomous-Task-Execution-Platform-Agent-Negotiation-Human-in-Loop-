class DataLineageTracker:
    def __init__(self):
        self.lineage = {}

    def track(self, source: str, target: str):
        self.lineage.setdefault(source, []).append(target)

    def get_lineage(self, source: str):
        return self.lineage.get(source, [])