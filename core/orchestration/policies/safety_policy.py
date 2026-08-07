class SafetyPolicy:
    def validate(self, task):
        if "delete_all" in str(task):
            raise ValueError("Unsafe task detected")