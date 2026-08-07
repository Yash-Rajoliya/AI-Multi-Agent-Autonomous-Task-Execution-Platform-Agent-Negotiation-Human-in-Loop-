from .dag import DAG


class GraphValidator:
    @staticmethod
    def validate(dag: DAG):
        visited = set()
        stack = set()

        def dfs(node):
            if node in stack:
                raise ValueError("Cycle detected")
            if node in visited:
                return

            stack.add(node)
            for child in dag.get_children(node):
                dfs(child)
            stack.remove(node)
            visited.add(node)

        for root in dag.get_roots():
            dfs(root)