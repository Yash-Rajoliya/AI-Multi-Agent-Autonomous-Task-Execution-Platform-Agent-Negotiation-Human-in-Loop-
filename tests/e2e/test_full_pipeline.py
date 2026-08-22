import pytest


@pytest.mark.asyncio
async def test_full_pipeline(client):
    payload = {
        "task": "analyze data",
        "agent_type": "researcher"
    }

    response = await client.post("/v1/tasks", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "task_id" in data
    assert data["status"] == "submitted"