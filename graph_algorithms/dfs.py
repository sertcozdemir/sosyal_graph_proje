from typing import Dict, List, Optional
from core.graph import Graph
from .base import Algorithm


class DFSAlgorithm(Algorithm):
    @property
    def name(self) -> str:
        return "DFS"

    def run(self, start_id: int) -> Dict[str, object]:
        """
        DFS Algoritması (iteratif stack ile)
        - visited_order: düğümlerin gezilme sırası
        - parents: DFS ağacındaki parent ilişkileri
        """

        graph = self.graph

        if start_id not in graph.nodes:
            raise ValueError(f"Başlangıç düğümü bulunamadı: {start_id}")

        visited = set()
        stack = []
        parents: Dict[int, Optional[int]] = {}
        visited_order: List[int] = []

        stack.append(start_id)
        parents[start_id] = None

        while stack:
            current = stack.pop()

            if current in visited:
                continue

            visited.add(current)
            visited_order.append(current)

            neighbors = sorted(graph.get_neighbors(current), reverse=True)
            for neighbor in neighbors:
                if neighbor not in visited:
                    parents[neighbor] = current
                    stack.append(neighbor)

        return {
            "visited_order": visited_order,
            "parents": parents
        }


def dfs(graph: Graph, start_id: int) -> Dict[str, object]:
    return DFSAlgorithm(graph).run(start_id)
