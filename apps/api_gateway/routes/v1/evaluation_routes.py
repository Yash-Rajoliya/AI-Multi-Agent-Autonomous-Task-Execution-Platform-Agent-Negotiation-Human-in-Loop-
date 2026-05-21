from fastapi import APIRouter
from ...controllers.evaluation_controller import EvaluationController

router = APIRouter()
controller = EvaluationController()


@router.post("/run")
async def run_evaluation(payload: dict):
    return await controller.run(payload)