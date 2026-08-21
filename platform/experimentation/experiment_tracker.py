import datetime


class ExperimentTracker:
    def __init__(self):
        self.records = []

    def track(self, experiment_name: str, variant: str, result: dict):
        self.records.append({
            "experiment": experiment_name,
            "variant": variant,
            "result": result,
            "timestamp": datetime.datetime.utcnow().isoformat()
        })

    def get_results(self):
        return self.records