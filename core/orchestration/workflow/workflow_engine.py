from core.orchestration.execution_graph.graph_executor import GraphExecutor
from core.orchestration.execution_graph.graph_validator import GraphValidator


class WorkflowEngine:
    def __init__(self, dag):
        self.dag = dag

    async def run(self, context: dict | None = None) -> dict:
        """
        Validates and executes the DAG workflow with the given context.
        """
        # 1. Standardize context object
        ctx = context if context is not None else {}

        # 2. Externalize validation (removes redundant internal validation if handled here)
        GraphValidator.validate(self.dag)

        # 3. Instantiate and execute
        executor = GraphExecutor(self.dag)
        await executor.execute(ctx)

        # 4. Return context so caller receives any mutations/results
        return ctx