import json
from typing import Dict, Any, List, Tuple
from core.graph import Graph
from core.node import Node


def save_graph_to_json(graph: Graph, filepath: str) -> None:
    """
    Grafı JSON formatında dosyaya kaydeder.
    Node özellikleri ve kenar bağlantıları saklanır.
    Ağırlıklar kaydedilmez; yüklerken formüle göre tekrar hesaplanır.
    """
    data: Dict[str, Any] = {}

    # Node'lar
    nodes_list: List[Dict[str, Any]] = []
    for node in graph.nodes.values():
        nodes_list.append({
            "id": node.id,
            "aktiflik": node.aktiflik,
            "etkilesim": node.etkilesim,
            "baglanti_sayisi": node.baglanti_sayisi,
        })

    # Edge'ler (her undirected edge'i bir kez kaydedelim)
    edges_set: set[Tuple[int, int]] = set()
    for e in graph.edges:
        a, b = e.source_id, e.target_id
        if a < b:
            edges_set.add((a, b))

    edges_list = [{"source": a, "target": b} for (a, b) in edges_set]

    data["nodes"] = nodes_list
    data["edges"] = edges_list

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_graph_from_json(filepath: str) -> Graph:
    """
    JSON dosyasından grafı geri yükler.
    Node'lar ve undirected edge'ler oluşturulur.
    Edge ağırlıkları formüle göre tekrar hesaplanır.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    g = Graph()

    # Node'ları ekle
    for n in data.get("nodes", []):
        node = Node(
            node_id=int(n["id"]),
            aktiflik=float(n.get("aktiflik", 0.0)),
            etkilesim=float(n.get("etkilesim", 0.0)),
            baglanti_sayisi=int(n.get("baglanti_sayisi", 0)),
        )
        g.add_node(node)

    # Edge'leri ekle (undirected)
    for e in data.get("edges", []):
        src = int(e["source"])
        dst = int(e["target"])
        # add_undirected_edge ağırlığı otomatik hesaplayacak
        g.add_undirected_edge(src, dst)

    return g
