from fastapi import APIRouter, HTTPException
from typing import List, Dict, Optional

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
    if len(ids) != len(texts) or len(ids) != len(metadata):
        raise HTTPException(
            status_code=400,
            detail="Payload lengths for ids, texts, and metadata must match",
        )

    try:
        vectors = await embedder.embed(texts)
        if not vectors:
            raise HTTPException(status_code=400, detail="Failed to compute embeddings for texts")

        await index.upsert(ids, vectors, metadata)
        return {"status": "success", "count": len(ids)}

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Upsert failed", error=str(e))
        raise HTTPException(status_code=500, detail="Upsert failed")


@router.post("/memory/query")
async def query_memory(query: str, filters: Optional[Dict] = None):
    if not query or not query.strip():
        raise HTTPException(status_code=400, detail="Query text cannot be empty")

    try:
        results = await retriever.retrieve(query, filters)
        return {"results": results, "count": len(results)}

    except Exception as e:
        logger.exception("Query failed", error=str(e))
        raise HTTPException(status_code=500, detail="Query failed")