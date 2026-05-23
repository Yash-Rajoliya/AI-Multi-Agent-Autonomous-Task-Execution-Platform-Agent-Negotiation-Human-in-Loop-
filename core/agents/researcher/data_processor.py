from typing import List


class DataProcessor:
    def process(self, data: List[str]) -> List[str]:
        return [d.lower() for d in data]