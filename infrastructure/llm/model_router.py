class ModelRouter:
    def route(self, task_type: str):
        if task_type == "cheap":
            return "gpt-3.5"
        return "gpt-4"