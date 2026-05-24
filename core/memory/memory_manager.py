from .working_memory import WorkingMemory
from .episodic_memory import EpisodicMemory
from .semantic_memory import SemanticMemory
from .memory_router import MemoryRouter


class MemoryManager:
    """
    Unified interface for all memory types
    """

    def __init__(self):
        self.working = WorkingMemory()
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()

        self.router = MemoryRouter(
            self.working,
            self.episodic,
            self.semantic
        )

    # ------------------------
    # Working Memory
    # ------------------------

    def set(self, key, value):
        self.working.set(key, value)

    def get(self, key):
        return self.working.get(key)

    # ------------------------
    # Episodic Memory
    # ------------------------

    def remember_event(self, content, metadata=None):
        return self.episodic.add_event(content, metadata)

    def recall_events(self, query):
        return self.episodic.search(query)

    # ------------------------
    # Semantic Memory
    # ------------------------

    def store_knowledge(self, embedding, document):
        self.semantic.add(embedding, document)

    def search_knowledge(self, embedding):
        return self.semantic.similarity_search(embedding)

    # ------------------------
    # Unified Retrieval
    # ------------------------

    def retrieve(self, query: str, embedding=None):
        return self.router.route(query, embedding)