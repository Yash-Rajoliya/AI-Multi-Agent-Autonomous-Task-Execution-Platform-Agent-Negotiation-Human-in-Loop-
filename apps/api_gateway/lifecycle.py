from fastapi import FastAPI
import logging

logger = logging.getLogger(__name__)


def register_lifecycle(app: FastAPI):

    @app.on_event("startup")
    async def startup():
        logger.info("API Gateway starting...")
        # Initialize connections (DB, Redis, etc.)

    @app.on_event("shutdown")
    async def shutdown():
        logger.info("API Gateway shutting down...")