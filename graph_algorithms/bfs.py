# graph_algorithms/bfs.py
from collections import deque
from typing import Dict, List, Optional
from core.graph import Graph
from .base import Algorithm


class BFSAlgorithm(Algorithm):
    @property
    def name(self) -> str:
        return "BFS"

    def run(self, start_id: int) -> Dict[str, object]:
        """
        BFS Algoritması:
        - visited_order: düğümlerin gezilme sırası
        - parents: BFS ağacında her düğümün parent'ı
        """

        graph = self.graph

        if start_id not in graph.nodes:
            raise ValueError(f"Başlangıç düğümü bulunamadı: {start_id}")

        visited = set()
        queue = deque()
        parents: Dict[int, Optional[int]] = {}

        visited_order: List[int] = []

        queue.append(start_id)
        visited.add(start_id)
        parents[start_id] = None

        while queue:
            current = queue.popleft()
            visited_order.append(current)

            for neighbor_id in graph.get_neighbors(current):
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    parents[neighbor_id] = current
                    queue.append(neighbor_id)

        return {
            "visited_order": visited_order,
            "parents": parents
        }


# Eski fonksiyonlu kullanım bozulmasın diye:
def bfs(graph: Graph, start_id: int) -> Dict[str, object]:
    return BFSAlgorithm(graph).run(start_id)
