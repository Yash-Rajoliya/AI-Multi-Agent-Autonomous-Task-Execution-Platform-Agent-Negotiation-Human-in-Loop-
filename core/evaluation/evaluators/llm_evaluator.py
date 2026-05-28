from typing import Dict
from infrastructure.llm.openai_client import OpenAIClient


class LLMEvaluator:
    """
    Uses LLM to judge outputs (subjective evaluation)
    """

    def __init__(self):
        self.client = OpenAIClient()

    async def evaluate(self, input_text: str, output: str, criteria: str) -> Dict:
        prompt = f"""
You are an expert evaluator.

Input:
{input_text}

Output:
{output}

Criteria:
{criteria}

Return JSON with:
- score (0-10)
- reasoning
"""

        response = await self.client.complete(prompt)

        return {
            "raw": response
        }