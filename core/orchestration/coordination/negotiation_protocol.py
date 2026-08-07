class NegotiationProtocol:
    def negotiate(self, proposals):
        # simple majority selection
        votes = {}
        for p in proposals:
            votes[p] = votes.get(p, 0) + 1
        return max(votes, key=votes.get)