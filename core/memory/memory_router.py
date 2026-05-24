from typing import Dict, Any


class MemoryRouter:
    """
    Routes queries to appropriate memory type
    """

    def __init__(self, working, episodic, semantic):
        self.working = working
        self.episodic = episodic
        self.semantic = semantic

    def route(self, query: str, embedding=None):
        results = {}

        # Working memory (exact match)
        if query in self.working.dump():
            results["working"] = self.working.get(query)

        # Episodic search
        results["episodic"] = self.episodic.search(query)

        # Semantic search
        if embedding:
            results["semantic"] = self.semantic.similarity_search(embedding)

        return results