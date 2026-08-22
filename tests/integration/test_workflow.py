import pytest
from apps.orchestrator_service.orchestration_engine import OrchestrationEngine


@pytest.mark.asyncio
async def test_workflow_execution():
    engine = OrchestrationEngine()

    workflow = {
        "steps": [
            {"id": "step1", "action": "process"},
            {"id": "step2", "action": "finalize"},
        ]
    }

    result = await engine.execute(workflow)

    assert result is not None
    assert "status" in result