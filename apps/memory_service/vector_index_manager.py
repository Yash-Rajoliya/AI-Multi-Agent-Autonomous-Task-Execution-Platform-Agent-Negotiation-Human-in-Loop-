from typing import List, Dict, Any

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
        metadata: List[Dict[str, Any]],
    ):
        if not ids or not vectors:
            raise ValueError("IDs and vectors cannot be empty for indexing")

        if len(ids) != len(vectors) or (metadata and len(ids) != len(metadata)):
            raise ValueError("Mismatched list lengths between IDs, vectors, and metadata")

        logger.info("Upserting vectors", count=len(ids))
        await self.backend.upsert(ids, vectors, metadata)

    async def query(
        self,
        vector: List[float],
        top_k: int,
        filters: Dict[str, Any] = None,
    ) -> List[Dict[str, Any]]:
        if not vector:
            logger.warning("Query vector is empty")
            return []

        logger.info("Querying vector DB", top_k=top_k)
        results = await self.backend.query(vector, top_k=top_k, filters=filters)
        return results or []