from typing import List, Dict


class MemoryInterface:
    async def retrieve(self, query: str) -> List[Dict]:
        raise NotImplementedError

    async def store(self, data: Dict):
        raise NotImplementedError