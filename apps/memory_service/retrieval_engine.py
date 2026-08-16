from typing import List, Dict

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
        filters: Dict = None,
    ) -> List[Dict]:
        logger.info("Retrieval started", query=query)

        embedding = (await self.embedder.embed([query]))[0]

        results = await self.index.query(
            embedding,
            top_k=config.top_k,
            filters=filters,
        )

        return self._post_process(results)

    def _post_process(self, results: List[Dict]) -> List[Dict]:
        # Placeholder for reranking / filtering
        return results