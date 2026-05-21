class ApprovalService:

    async def approve(self, approval_id, user):
        return {
            "approval_id": approval_id,
            "status": "approved",
            "reviewed_by": user["sub"]
        }

    async def reject(self, approval_id, user):
        return {
            "approval_id": approval_id,
            "status": "rejected",
            "reviewed_by": user["sub"]
        }


class ApprovalController:

    def __init__(self):
        self.service = ApprovalService()

    async def approve(self, approval_id, user):
        return await self.service.approve(approval_id, user)

    async def reject(self, approval_id, user):
        return await self.service.reject(approval_id, user)