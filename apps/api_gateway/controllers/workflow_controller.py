from uuid import uuid4
from datetime import datetime


class WorkflowService:

    async def create(self, payload, user):
        return {
            "workflow_id": str(uuid4()),
            "name": payload.name,
            "steps": payload.steps,
            "created_by": user["sub"],
            "created_at": datetime.utcnow()
        }

    async def get(self, workflow_id: str):
        return {
            "workflow_id": workflow_id,
            "status": "running"
        }


class WorkflowController:

    def __init__(self):
        self.service = WorkflowService()

    async def create_workflow(self, payload, user):
        return await self.service.create(payload, user)

    async def get_workflow(self, workflow_id):
        return await self.service.get(workflow_id)