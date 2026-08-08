import asyncio

class DAGException(Exception):
    """Raised when graph consistency validation fails."""
    pass


class GraphExecutor:
    def __init__(self, dag):
        self.dag = dag

    def _validate_graph(self):
        """Ensures the DAG contains no cycles before execution."""
        in_degrees = {node_id: len(self.dag.get_parents(node_id)) for node_id in self.dag.nodes}
        queue = [node_id for node_id, degree in in_degrees.items() if degree == 0]
        visited_count = 0

        while queue:
            node_id = queue.pop(0)
            visited_count += 1
            for child in self.dag.get_children(node_id):
                in_degrees[child] -= 1
                if in_degrees[child] == 0:
                    queue.append(child)

        if visited_count != len(self.dag.nodes):
            raise DAGException("Graph consistency error: Cycle detected in DAG.")

    async def execute(self, context: dict):
        # 1. Enforce Graph Consistency
        self._validate_graph()

        # Track unresolved parent dependencies per node
        in_degree = {
            node_id: len(self.dag.get_parents(node_id))
            for node_id in self.dag.nodes
        }
        
        # State locks and completion tracking
        lock = asyncio.Lock()
        completed_nodes = set()
        failed_nodes = set()
        ready_queue = asyncio.Queue()

        # Initialize queue with root nodes (in-degree == 0)
        roots = self.dag.get_roots()
        for root_id in roots:
            await ready_queue.put(root_id)

        async def worker():
            while True:
                node_id = await ready_queue.get()
                try:
                    # Skip execution if any parent failed
                    parents = self.dag.get_parents(node_id)
                    if any(parent in failed_nodes for parent in parents):
                        async with lock:
                            failed_nodes.add(node_id)
                        continue

                    # Execute node safely
                    node = self.dag.nodes[node_id]
                    await node.execute(context)

                    async with lock:
                        completed_nodes.add(node_id)
                        # Notify children and enqueue those whose dependencies are satisfied
                        for child_id in self.dag.get_children(node_id):
                            in_degree[child_id] -= 1
                            if in_degree[child_id] == 0:
                                await ready_queue.put(child_id)

                except Exception as exc:
                    async with lock:
                        failed_nodes.add(node_id)
                    raise exc
                finally:
                    ready_queue.task_done()

        # Launch dynamic worker pool matching DAG size
        workers = [
            asyncio.create_task(worker()) 
            for _ in range(max(1, len(self.dag.nodes)))
        ]

        # Wait until all queued tasks are processed
        await ready_queue.join()

        # Cancel remaining idle worker loops
        for w in workers:
            w.cancel()
        await asyncio.gather(*workers, return_exceptions=True)

        if failed_nodes:
            raise DAGException(f"Workflow execution failed on nodes: {failed_nodes}")