import heapq
from typing import Dict, Optional, Tuple, List
from core.graph import Graph
from core.node import Node


def heuristic(node: Node, goal: Node) -> float:
    """
    A* için heuristic:
    Özellik farklarının öklid uzaklığı.
    """
    da = node.aktiflik - goal.aktiflik
    de = node.etkilesim - goal.etkilesim
    db = node.baglanti_sayisi - goal.baglanti_sayisi
    return (da * da + de * de + db * db) ** 0.5


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


def astar(graph: Graph, start_id: int, goal_id: int) -> Dict[str, object]:
    """
    A* en kısa yol algoritması.
    Dönüş:
      {
        "g": {node_id: maliyet},
        "prev": {node_id: parent_id},
        "path": [node_id, ...]
      }
    """

    if start_id not in graph.nodes or goal_id not in graph.nodes:
        raise ValueError("Başlangıç veya hedef düğüm graf içinde yok.")

    start_node = graph.nodes[start_id]
    goal_node = graph.nodes[goal_id]

    g_score: Dict[int, float] = {node_id: float("inf") for node_id in graph.nodes}
    g_score[start_id] = 0.0

    f_score: Dict[int, float] = {node_id: float("inf") for node_id in graph.nodes}
    f_score[start_id] = heuristic(start_node, goal_node)

    prev: Dict[int, Optional[int]] = {node_id: None for node_id in graph.nodes}

    # (f_score, node_id)
    heap: List[Tuple[float, int]] = [(f_score[start_id], start_id)]

    in_open = {start_id}

    while heap:
        _, current = heapq.heappop(heap)
        in_open.discard(current)

        if current == goal_id:
            # hedefe ulaştık
            path = reconstruct_path(prev, start_id, goal_id)
            return {
                "g": g_score,
                "prev": prev,
                "path": path
            }

        for neighbor in graph.get_neighbors(current):
            try:
                w = graph.get_edge_weight(current, neighbor)
            except ValueError:
                continue

            tentative_g = g_score[current] + w
            if tentative_g < g_score[neighbor]:
                prev[neighbor] = current
                g_score[neighbor] = tentative_g

                h = heuristic(graph.nodes[neighbor], goal_node)
                f_score[neighbor] = tentative_g + h

                if neighbor not in in_open:
                    heapq.heappush(heap, (f_score[neighbor], neighbor))
                    in_open.add(neighbor)

    # yol bulunamazsa:
    return {
        "g": g_score,
        "prev": prev,
        "path": []  # boş yol
    }
