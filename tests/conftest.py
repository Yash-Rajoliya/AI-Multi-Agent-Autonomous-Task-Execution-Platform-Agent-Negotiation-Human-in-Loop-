import asyncio
import pytest
from httpx import AsyncClient

from apps.api_gateway.app import create_app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop


@pytest.fixture
async def app():
    return create_app()


@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac