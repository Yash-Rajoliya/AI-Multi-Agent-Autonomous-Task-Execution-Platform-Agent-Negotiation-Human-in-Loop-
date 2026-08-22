class MockLLM:
    async def generate(self, prompt: str):
        return f"[MOCK RESPONSE] {prompt}"