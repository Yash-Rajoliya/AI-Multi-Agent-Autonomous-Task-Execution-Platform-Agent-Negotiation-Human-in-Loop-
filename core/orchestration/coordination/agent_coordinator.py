import asyncio


class AgentCoordinator:
    def __init__(self):
        self.agents = {}

    def register(self, name, agent):
        self.agents[name] = agent

    async def broadcast(self, message):
        tasks = [agent.handle(message) for agent in self.agents.values()]
        return await asyncio.gather(*tasks)