class ConsensusEngine:
    def reach(self, results):
        return max(set(results), key=results.count)