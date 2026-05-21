from fastapi import APIRouter
import time

router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time()
    }


@router.get("/metrics")
async def metrics():
    return {
        "requests": "N/A",
        "latency": "N/A"
    }