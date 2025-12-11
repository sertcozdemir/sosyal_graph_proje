class Edge:
    def __init__(self, source_id: int, target_id: int, weight: float):
        self.source_id = source_id
        self.target_id = target_id
        self.weight = weight

    def __repr__(self) -> str:
        return f"Edge({self.source_id} -> {self.target_id}, weight={self.weight:.3f})"
