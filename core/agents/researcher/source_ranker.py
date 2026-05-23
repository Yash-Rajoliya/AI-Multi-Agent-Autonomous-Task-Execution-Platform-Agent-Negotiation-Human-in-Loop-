from typing import List


class SourceRanker:
    def rank(self, sources: List[str]) -> List[str]:
        return sorted(sources)