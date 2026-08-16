from typing import Dict, List
from datetime import datetime

from infrastructure.observability.logging import get_logger

logger = get_logger(__name__)


class ReportGenerator:
    def generate(self, summary: Dict, raw_results: List[Dict]) -> Dict:
        logger.info("Generating report")

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "summary": summary,
            "details": raw_results,
        }