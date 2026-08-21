import inspect
from typing import List, Callable, Any


class FeaturePipeline:
    def __init__(self, steps: List[Callable]):
        self.steps = steps

    async def run(self, data: Any) -> Any:
        for step in self.steps:
            if inspect.iscoroutinefunction(step):
                data = await step(data)
            else:
                data = step(data)
        return data