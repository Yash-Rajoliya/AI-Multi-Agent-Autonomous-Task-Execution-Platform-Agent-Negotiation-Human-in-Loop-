from typing import List, Dict

from infrastructure.vector_db.faiss_adapter import FAISSAdapter
from infrastructure.observability.logging import get_logger

logger = get_logger(__name__)


class VectorIndexManager:
    def __init__(self):
        self.backend = FAISSAdapter()

    async def upsert(
        self,
        ids: List[str],
        vectors: List[List[float]],
        metadata: List[Dict],
    ):
        logger.info("Upserting vectors", count=len(ids))
        await self.backend.upsert(ids, vectors, metadata)

    async def query(
        self,
        vector: List[float],
        top_k: int,
        filters: Dict = None,
    ):
        logger.info("Querying vector DB", top_k=top_k)
        return await self.backend.query(vector, top_k, filters)