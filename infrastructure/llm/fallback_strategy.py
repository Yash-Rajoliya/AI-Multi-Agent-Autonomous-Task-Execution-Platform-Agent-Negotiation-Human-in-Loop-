import logging

logger = logging.getLogger(__name__)


class FallbackStrategy:

    async def execute(self, primary, fallback, *args, **kwargs):
        try:
            return await primary(*args, **kwargs)
        except Exception as exc:
            logger.warning(
                "Primary model execution failed (%s). Triggering fallback execution.",
                exc,
                exc_info=True,
            )
            try:
                return await fallback(*args, **kwargs)
            except Exception as fallback_exc:
                logger.error(
                    "Fallback execution also failed (%s).",
                    fallback_exc,
                    exc_info=True,
                )
                raise fallback_exc from exc