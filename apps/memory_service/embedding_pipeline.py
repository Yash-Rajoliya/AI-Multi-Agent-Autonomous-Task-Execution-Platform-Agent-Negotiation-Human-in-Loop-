from typing import List

from infrastructure.llm.openai_client import OpenAIClient
from infrastructure.observability.logging import get_logger

logger = get_logger(__name__)


class EmbeddingPipeline:
    def __init__(self):
        self.client = OpenAIClient()

    async def embed(self, texts: List[str]) -> List[List[float]]:
        logger.info("Generating embeddings", count=len(texts))

        embeddings = await self.client.get_embeddings(texts)

        return embeddings