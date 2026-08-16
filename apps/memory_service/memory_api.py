from fastapi import APIRouter, HTTPException
from typing import List, Dict

from infrastructure.observability.logging import get_logger

from .embedding_pipeline import EmbeddingPipeline
from .vector_index_manager import VectorIndexManager
from .retrieval_engine import RetrievalEngine

router = APIRouter()
logger = get_logger(__name__)

embedder = EmbeddingPipeline()
index = VectorIndexManager()
retriever = RetrievalEngine()


@router.post("/memory/upsert")
async def upsert_memory(
    ids: List[str],
    texts: List[str],
    metadata: List[Dict],
):
    try:
        vectors = await embedder.embed(texts)

        await index.upsert(ids, vectors, metadata)

        return {"status": "success"}

    except Exception as e:
        logger.exception("Upsert failed", error=str(e))
        raise HTTPException(status_code=500, detail="Upsert failed")


@router.post("/memory/query")
async def query_memory(query: str, filters: Dict = None):
    try:
        results = await retriever.retrieve(query, filters)

        return {
            "results": results
        }

    except Exception as e:
        logger.exception("Query failed", error=str(e))
        raise HTTPException(status_code=500, detail="Query failed")