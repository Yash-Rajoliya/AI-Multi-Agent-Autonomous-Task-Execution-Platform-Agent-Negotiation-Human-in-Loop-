import pytest
from core.agents.base.base_agent import BaseAgent


class DummyAgent(BaseAgent):
    async def act(self, input_data):
        return {"result": "processed", "input": input_data}


@pytest.mark.asyncio
async def test_agent_execution():
    agent = DummyAgent(name="test-agent")

    result = await agent.run({"task": "demo"})

    assert result["result"] == "processed"
    assert result["input"]["task"] == "demo"