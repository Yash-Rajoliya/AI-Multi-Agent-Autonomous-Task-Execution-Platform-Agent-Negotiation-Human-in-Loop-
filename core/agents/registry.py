from typing import Dict, Type

from core.agents.base.base_agent import BaseAgent

from core.agents.planner.planner_agent import PlannerAgent
from core.agents.researcher.researcher_agent import ResearcherAgent
from core.agents.executor.executor_agent import ExecutorAgent
from core.agents.critic.critic_agent import CriticAgent
from core.agents.reflection.reflection_agent import ReflectionAgent


class AgentRegistry:
    def __init__(self):
        self._registry: Dict[str, Type[BaseAgent]] = {}

        self.register("planner", PlannerAgent)
        self.register("researcher", ResearcherAgent)
        self.register("executor", ExecutorAgent)
        self.register("critic", CriticAgent)
        self.register("reflection", ReflectionAgent)

    def register(self, name: str, agent_cls: Type[BaseAgent]):
        self._registry[name] = agent_cls

    def get(self, name: str) -> BaseAgent:
        if name not in self._registry:
            raise ValueError(f"Agent {name} not registered")

        return self._registry[name]()