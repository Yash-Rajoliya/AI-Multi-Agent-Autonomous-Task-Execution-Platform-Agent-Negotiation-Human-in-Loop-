import openai
from infrastructure.config import get_settings


class OpenAIClient:
    def __init__(self):
        settings = get_settings()
        openai.api_key = settings.OPENAI_API_KEY

    async def generate(self, prompt: str):
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message["content"]