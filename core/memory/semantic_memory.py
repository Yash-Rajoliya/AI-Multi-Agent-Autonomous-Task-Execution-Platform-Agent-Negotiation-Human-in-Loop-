from typing import List, Dict
import numpy as np


class SemanticMemory:
    """
    Vector-based memory
    """

    def __init__(self):
        self.vectors: List[np.ndarray] = []
        self.documents: List[Dict] = []

    def add(self, embedding: List[float], document: Dict):
        self.vectors.append(np.array(embedding))
        self.documents.append(document)

    def similarity_search(self, query_embedding: List[float], top_k=3):
        if not self.vectors:
            return []

        query_vec = np.array(query_embedding)

        scores = [
            np.dot(vec, query_vec) / (np.linalg.norm(vec) * np.linalg.norm(query_vec))
            for vec in self.vectors
        ]

        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        return [self.documents[i] for i in top_indices]