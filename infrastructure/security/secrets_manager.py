import os


class SecretsManager:
    def get_secret(self, key: str):
        return os.getenv(key)