from typing import Dict, List
from .node import Node
from .edge import Edge


class DAG:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []

    def add_node(self, node: Node):
        if node.id in self.nodes:
            raise ValueError(f"Node {node.id} already exists")
        self.nodes[node.id] = node

    def add_edge(self, edge: Edge):
        if edge.source not in self.nodes or edge.target not in self.nodes:
            raise ValueError("Invalid edge reference")
        self.edges.append(edge)

    def get_children(self, node_id: str) -> List[str]:
        return [e.target for e in self.edges if e.source == node_id]

    def get_roots(self):
        targets = {e.target for e in self.edges}
        return [n for n in self.nodes if n not in targets]