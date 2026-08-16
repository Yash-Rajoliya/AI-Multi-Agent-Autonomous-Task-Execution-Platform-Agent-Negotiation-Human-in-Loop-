import faiss
import numpy as np


class FaissAdapter:
    def __init__(self, dim: int = 768):
        self.index = faiss.IndexFlatL2(dim)

    def add(self, vectors):
        self.index.add(np.array(vectors).astype("float32"))

    def search(self, query, k=5):
        distances, indices = self.index.search(
            np.array([query]).astype("float32"), k
        )
        return indices