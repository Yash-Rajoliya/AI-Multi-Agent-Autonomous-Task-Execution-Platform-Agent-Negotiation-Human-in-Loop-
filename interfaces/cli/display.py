import json


class Display:
    @staticmethod
    def print_json(data):
        print(json.dumps(data, indent=2))

    @staticmethod
    def success(message: str):
        print(f"[✔] {message}")

    @staticmethod
    def error(message: str):
        print(f"[✖] {message}")