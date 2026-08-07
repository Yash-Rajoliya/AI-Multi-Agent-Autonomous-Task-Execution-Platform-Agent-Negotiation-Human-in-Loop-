from core.orchestration.execution_graph.graph_executor import GraphExecutor
from core.orchestration.execution_graph.graph_validator import GraphValidator


class WorkflowEngine:
    def __init__(self, dag):
        self.dag = dag

    async def run(self, context: dict):
        GraphValidator.validate(self.dag)
        executor = GraphExecutor(self.dag)
        await executor.execute(context)