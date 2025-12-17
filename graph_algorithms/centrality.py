class DegreeCentrality:
    def __init__(self,graph):
        self.graph=graph

    def top_k(self, k=5):
        scores = {}
        n = len(self.graph.nodes)
        for node_id, node in self.graph.nodes.items():
            scores[node_id] = len(node.neighbors) / (n-1 if n > 1 else 1)
        return sorted(scores.items(), key = lambda x: x[1], reverse=True)[:k]