from typing import List


class FeaturePipeline:
    def __init__(self, steps: List):
        self.steps = steps

    async def run(self, data):
        for step in self.steps:
            data = await step(data)
        return data