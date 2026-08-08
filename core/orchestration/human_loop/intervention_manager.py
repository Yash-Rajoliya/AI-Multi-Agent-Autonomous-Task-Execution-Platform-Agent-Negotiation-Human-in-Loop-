import enum
import time
from typing import Dict, Any, Optional


class WorkflowExecutionState(str, enum.Enum):
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    RESUMED = "RESUMED"
    ABORTED = "ABORTED"


class InterventionError(Exception):
    """Raised when an intervention is performed on an invalid state."""
    pass


class InterventionManager:
    def intervene(
        self,
        workflow: Dict[str, Any],
        operator_id: Optional[str] = None,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Pauses a workflow for human intervention with metadata and safety checks.
        """
        current_state = workflow.get("state", WorkflowExecutionState.RUNNING)
        if current_state == WorkflowExecutionState.PAUSED:
            raise InterventionError(f"Workflow '{workflow.get('id', 'unknown')}' is already paused.")
        
        if current_state == WorkflowExecutionState.ABORTED:
            raise InterventionError(f"Cannot intervene on aborted workflow '{workflow.get('id', 'unknown')}'.")

        workflow["state"] = WorkflowExecutionState.PAUSED
        workflow["paused"] = True
        workflow["intervention"] = {
            "intervened_at": time.time(),
            "operator_id": operator_id,
            "reason": reason or "Manual intervention triggered",
            "previous_state": current_state
        }
        return workflow

    def resume(
        self,
        workflow: Dict[str, Any],
        operator_id: Optional[str] = None,
        modifications: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Resumes a paused workflow, optionally applying human override payload updates.
        """
        if workflow.get("state") != WorkflowExecutionState.PAUSED and not workflow.get("paused", False):
            raise InterventionError(f"Cannot resume workflow '{workflow.get('id', 'unknown')}' - it is not in a PAUSED state.")

        workflow["state"] = WorkflowExecutionState.RUNNING
        workflow["paused"] = False

        if modifications:
            context = workflow.setdefault("context", {})
            context.update(modifications)

        if "intervention" in workflow:
            workflow["intervention"]["resumed_at"] = time.time()
            workflow["intervention"]["resumed_by"] = operator_id

        return workflow

    def abort(
        self,
        workflow: Dict[str, Any],
        operator_id: Optional[str] = None,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """Safely terminates an intervened workflow without resuming it."""
        workflow["state"] = WorkflowExecutionState.ABORTED
        workflow["paused"] = False
        workflow["intervention_abort"] = {
            "aborted_at": time.time(),
            "operator_id": operator_id,
            "reason": reason
        }
        return workflow