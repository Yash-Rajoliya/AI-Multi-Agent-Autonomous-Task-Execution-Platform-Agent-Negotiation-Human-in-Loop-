from typing import List, Dict, Any

from infrastructure.observability.logging import get_logger

from .embedding_pipeline import EmbeddingPipeline
from .vector_index_manager import VectorIndexManager
from .memory_config import config

logger = get_logger(__name__)


class RetrievalEngine:
    def __init__(self):
        self.embedder = EmbeddingPipeline()
        self.index = VectorIndexManager()

    async def retrieve(
        self,
        query: str,
        filters: Dict[str, Any] = None,
    ) -> List[Dict[str, Any]]:
        if not query or not query.strip():
            logger.warning("Empty query received for retrieval")
            return []

        logger.info("Retrieval started", query=query)

        embeddings = await self.embedder.embed([query])
        if not embeddings:
            logger.error("Failed to generate embedding for query")
            return []

        results = await self.index.query(
            embeddings[0],
            top_k=config.top_k,
            filters=filters,
        )

        return self._post_process(results)

    def _post_process(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not results:
            return []

        # Deduplicate results by ID and sort by similarity score descending
        seen_ids = set()
        deduped = []
        for item in sorted(results, key=lambda x: x.get("score", 0), reverse=True):
            item_id = item.get("id")
            if item_id and item_id not in seen_ids:
                seen_ids.add(item_id)
                deduped.append(item)

        return deduped