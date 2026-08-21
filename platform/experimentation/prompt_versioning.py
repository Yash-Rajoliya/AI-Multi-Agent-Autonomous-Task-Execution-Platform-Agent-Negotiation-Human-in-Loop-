class PromptVersioning:
    def __init__(self):
        self.versions = {}

    def add_version(self, name: str, prompt: str):
        self.versions.setdefault(name, []).append(prompt)

    def get_latest(self, name: str):
        return self.versions.get(name, [])[-1]