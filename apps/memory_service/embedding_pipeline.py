from typing import List

from infrastructure.llm.openai_client import OpenAIClient
from infrastructure.observability.logging import get_logger

logger = get_logger(__name__)


class EmbeddingPipeline:
    def __init__(self):
        self.client = OpenAIClient()

    async def embed(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            logger.warning("Embed called with empty text list")
            return []

        # Sanitize inputs to ensure consistency
        cleaned_texts = [text.strip() for text in texts if text and text.strip()]
        if not cleaned_texts:
            logger.warning("No valid non-empty texts to embed after sanitization")
            return []

        logger.info("Generating embeddings", count=len(cleaned_texts))
        embeddings = await self.client.get_embeddings(cleaned_texts)

        return embeddings