import heapq
from typing import Dict, Optional, Tuple, List
from core.graph import Graph


def reconstruct_path(previous: Dict[int, Optional[int]], start: int, goal: int) -> List[int]:
    path = []
    current = goal
    while current is not None:
        path.append(current)
        if current == start:
            break
        current = previous.get(current)
    path.reverse()
    return path


def dijkstra(graph: Graph, start_id: int, goal_id: Optional[int] = None) -> Dict[str, object]:
    """
    Dijkstra en kısa yol algoritması.
    - start_id: başlangıç düğümü
    - goal_id verilirse: o düğüme kadar en kısa yol
    - verilmezse: tüm düğümlere en kısa uzaklıklar

    Dönüş:
      {
        "dist": {node_id: mesafe},
        "prev": {node_id: parent_id},
        "path": [node_id, ...]  # goal_id verilmişse
      }
    """

    if start_id not in graph.nodes:
        raise ValueError(f"Başlangıç düğümü yok: {start_id}")

    dist: Dict[int, float] = {node_id: float("inf") for node_id in graph.nodes}
    prev: Dict[int, Optional[int]] = {node_id: None for node_id in graph.nodes}
    dist[start_id] = 0.0

    # (mesafe, node_id)
    heap: List[Tuple[float, int]] = [(0.0, start_id)]

    while heap:
        current_dist, u = heapq.heappop(heap)

        # Heap'ten çıkan değer güncel değilse atla
        if current_dist > dist[u]:
            continue

        # Hedef düğüme ulaştıysak çıkabiliriz
        if goal_id is not None and u == goal_id:
            break

        for v in graph.get_neighbors(u):
            try:
                w = graph.get_edge_weight(u, v)
            except ValueError:
                continue  # edge yoksa boşver

            alt = dist[u] + w
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heapq.heappush(heap, (alt, v))

    result = {
        "dist": dist,
        "prev": prev,
    }

    if goal_id is not None:
        result["path"] = reconstruct_path(prev, start_id, goal_id)

    return result
