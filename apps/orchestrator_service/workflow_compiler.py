from typing import Dict, Any, List


class Node:
    def __init__(self, id: str, type: str):
        self.id = id
        self.type = type


class ExecutionGraph:
    def __init__(self, nodes: List[Node]):
        self.nodes = nodes

    def topological_sort(self) -> List[Node]:
        # Simplified for demo (real: DAG sort)
        return self.nodes


class WorkflowCompiler:
    def compile(self, workflow: Dict[str, Any]) -> ExecutionGraph:
        nodes = [
            Node(step["id"], step["type"])
            for step in workflow.get("steps", [])
        ]
        return ExecutionGraph(nodes)