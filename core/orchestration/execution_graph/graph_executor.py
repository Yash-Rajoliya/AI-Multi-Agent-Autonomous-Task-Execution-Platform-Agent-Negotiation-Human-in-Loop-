import asyncio
from .dag import DAG


class GraphExecutor:
    def __init__(self, dag: DAG):
        self.dag = dag

    async def execute(self, context: dict):
        tasks = []

        async def run_node(node_id):
            node = self.dag.nodes[node_id]
            await node.execute(context)

            for child in self.dag.get_children(node_id):
                await run_node(child)

        for root in self.dag.get_roots():
            tasks.append(run_node(root))

        await asyncio.gather(*tasks)