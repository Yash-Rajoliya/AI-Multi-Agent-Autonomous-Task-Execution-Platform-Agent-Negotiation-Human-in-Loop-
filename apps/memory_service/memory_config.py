from pydantic import BaseSettings


class MemoryConfig(BaseSettings):
    service_name: str = "memory-service"

    vector_backend: str = "faiss"  # faiss | pinecone | weaviate
    embedding_model: str = "text-embedding-3-small"

    top_k: int = 5

    enable_cache: bool = True
    cache_ttl: int = 300

    redis_url: str = "redis://localhost:6379/1"

    class Config:
        env_file = ".env"


config = MemoryConfig()