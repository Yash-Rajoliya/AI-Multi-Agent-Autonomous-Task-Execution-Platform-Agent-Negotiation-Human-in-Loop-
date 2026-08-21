import asyncio
from .interactive_session import InteractiveSession


def run_cli():
    session = InteractiveSession()
    asyncio.run(session.start())