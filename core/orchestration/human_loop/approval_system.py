import enum
import time
from typing import Dict, Any, Optional


class ApprovalStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class ApprovalRequestError(Exception):
    """Raised on invalid state transitions or duplicate requests."""
    pass


class ApprovalSystem:
    def __init__(self, default_ttl_seconds: Optional[float] = 3600):
        self._pending: Dict[str, Dict[str, Any]] = {}
        self.default_ttl_seconds = default_ttl_seconds

    def request(self, task_id: str, payload: Dict[str, Any], ttl_seconds: Optional[float] = None) -> Dict[str, Any]:
        """Submits a task for human approval with duplicate prevention and TTL."""
        if task_id in self._pending:
            existing = self._pending[task_id]
            if existing["status"] == ApprovalStatus.PENDING and not self._is_expired(existing):
                raise ApprovalRequestError(f"Task '{task_id}' already has an active pending approval request.")

        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl_seconds
        created_at = time.time()
        
        request_record = {
            "task_id": task_id,
            "payload": payload,
            "status": ApprovalStatus.PENDING,
            "created_at": created_at,
            "expires_at": created_at + ttl if ttl else None,
            "decision_metadata": None,
        }
        self._pending[task_id] = request_record
        return request_record

    def _is_expired(self, record: Dict[str, Any]) -> bool:
        if record["expires_at"] and time.time() > record["expires_at"]:
            record["status"] = ApprovalStatus.EXPIRED
            return True
        return False

    def approve(self, task_id: str, approver: Optional[str] = None) -> Dict[str, Any]:
        """Approves a pending task. Idempotent against double-approval."""
        return self._resolve(task_id, ApprovalStatus.APPROVED, reviewer=approver)

    def reject(self, task_id: str, reviewer: Optional[str] = None, reason: Optional[str] = None) -> Dict[str, Any]:
        """Explicitly rejects a pending task."""
        return self._resolve(task_id, ApprovalStatus.REJECTED, reviewer=reviewer, reason=reason)

    def _resolve(self, task_id: str, status: ApprovalStatus, reviewer: Optional[str] = None, reason: Optional[str] = None) -> Dict[str, Any]:
        if task_id not in self._pending:
            raise ApprovalRequestError(f"No approval request found for task '{task_id}'.")

        record = self._pending[task_id]

        if self._is_expired(record):
            raise ApprovalRequestError(f"Approval request for task '{task_id}' has expired.")

        if record["status"] != ApprovalStatus.PENDING:
            raise ApprovalRequestError(f"Task '{task_id}' is already resolved with status: {record['status']}.")

        record["status"] = status
        record["decision_metadata"] = {
            "resolved_at": time.time(),
            "reviewer": reviewer,
            "reason": reason,
        }
        return self._pending.pop(task_id)

    def get_status(self, task_id: str) -> Optional[ApprovalStatus]:
        """Safe non-destructive lookup of request status handling auto-expiration."""
        record = self._pending.get(task_id)
        if not record:
            return None
        if record["status"] == ApprovalStatus.PENDING and self._is_expired(record):
            return ApprovalStatus.EXPIRED
        return record["status"]