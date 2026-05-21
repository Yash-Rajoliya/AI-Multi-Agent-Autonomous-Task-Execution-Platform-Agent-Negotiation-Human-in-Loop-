from uuid import uuid4
from datetime import datetime


class AgentService:

    async def create(self, payload, user):
        return {
            "agent_id": str(uuid4()),
            "name": payload.name,
            "created_by": user["sub"],
            "created_at": datetime.utcnow()
        }

    async def get(self, agent_id: str):
        return {
            "agent_id": agent_id,
            "status": "active"
        }


class AgentController:

    def __init__(self):
        self.service = AgentService()

    async def create_agent(self, payload, user):
        return await self.service.create(payload, user)

    async def get_agent(self, agent_id):
        return await self.service.get(agent_id)