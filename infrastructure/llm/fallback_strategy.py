class FallbackStrategy:
    async def execute(self, primary, fallback, *args, **kwargs):
        try:
            return await primary(*args, **kwargs)
        except Exception:
            return await fallback(*args, **kwargs)