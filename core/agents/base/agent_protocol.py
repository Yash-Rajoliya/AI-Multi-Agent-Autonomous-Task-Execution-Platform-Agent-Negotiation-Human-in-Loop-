from abc import ABC, abstractmethod
from typing import Dict, Any


class AgentProtocol(ABC):
    @abstractmethod
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pass