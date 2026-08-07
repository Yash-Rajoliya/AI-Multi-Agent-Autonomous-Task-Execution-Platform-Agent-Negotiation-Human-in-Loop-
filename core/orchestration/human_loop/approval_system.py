class ApprovalSystem:
    def __init__(self):
        self.pending = {}

    def request(self, task_id, payload):
        self.pending[task_id] = payload

    def approve(self, task_id):
        return self.pending.pop(task_id, None)