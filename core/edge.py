class Edge:
    def __init__(self, node_a: int, node_b: int, weight: float):
        self.a = node_a
        self.b = node_b
        self.weight = weight


    def __repr__(self) -> str:
        return f"Edge({self.source_id} -> {self.target_id}, weight={self.weight:.3f})"
