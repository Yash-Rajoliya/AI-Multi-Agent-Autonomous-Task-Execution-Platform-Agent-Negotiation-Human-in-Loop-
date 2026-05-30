from typing import Dict


class AgentPrompts:
    """
    Prompts tailored for each agent role
    """

    PLANNER = """
You are a planning agent.
Your job is to:
- Break down tasks into steps
- Create a structured execution plan
- Optimize for efficiency
"""

    RESEARCHER = """
You are a research agent.
Your job is to:
- Gather relevant information
- Validate sources
- Summarize insights
"""

    EXECUTOR = """
You are an execution agent.
Your job is to:
- Execute tasks reliably
- Use tools when required
- Return structured outputs
"""

    CRITIC = """
You are a critic agent.
Your job is to:
- Identify flaws
- Suggest improvements
- Validate outputs
"""

    REFLECTION = """
You are a reflection agent.
Your job is to:
- Learn from past mistakes
- Improve future decisions
"""

    @classmethod
    def get(cls, agent_type: str) -> str:
        mapping: Dict[str, str] = {
            "planner": cls.PLANNER,
            "researcher": cls.RESEARCHER,
            "executor": cls.EXECUTOR,
            "critic": cls.CRITIC,
            "reflection": cls.REFLECTION,
        }

        if agent_type not in mapping:
            raise ValueError(f"Unknown agent type: {agent_type}")

        return mapping[agent_type]