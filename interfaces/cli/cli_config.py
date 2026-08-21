import os


class CLIConfig:
    API_URL = os.getenv("API_URL", "http://localhost:8000")
    TIMEOUT = int(os.getenv("CLI_TIMEOUT", "10"))