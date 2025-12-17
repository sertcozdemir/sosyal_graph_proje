from typing import Dict, List
from .node import Node
from .edge import Edge
import math


class Graph:
    def __init__(self):
        self.nodes: Dict[int, Node] = {}
        self.edges: List[Edge] = []

    # ---- Temel CRUD ----
    def add_node(self, node: Node) -> None:
        if node.id in self.nodes:
            raise ValueError(f"Node {node.id} zaten var.")
        self.nodes[node.id] = node

    def remove_node(self, node_id: int) -> None:
        if node_id not in self.nodes:
            return
        # Komşulardan sil
        for n in self.nodes.values():
            n.neighbors.discard(node_id)
        # Edge'leri filtrele
        self.edges = [
            e for e in self.edges
            if e.source_id != node_id and e.target_id != node_id
        ]
        del self.nodes[node_id]

    def add_undirected_edge(self, a: int, b: int):
        if a == b:
            raise ValueError("Self-loop yasak")

        if a not in self.nodes or b not in self.nodes:
            raise ValueError("Node yok")

    # zaten varsa ekleme
        if b in self.nodes[a].neighbors:
            raise ValueError("Bu edge zaten var")

        w = self.compute_weight(self.nodes[a], self.nodes[b])

        self.edges.append(Edge(a, b, w))

        self.nodes[a].neighbors.add(b)
        self.nodes[b].neighbors.add(a)

        self.nodes[a].baglanti_sayisi = len(self.nodes[a].neighbors)
        self.nodes[b].baglanti_sayisi = len(self.nodes[b].neighbors)

    def remove_undirected_edge(self, node_id_a: int, node_id_b: int) -> None:
        """İki node arasındaki çift yönlü bağlantıyı siler."""
        if node_id_a not in self.nodes or node_id_b not in self.nodes:
            return

        # Edge listesinden filtrele
        self.edges = [
            e for e in self.edges
            if not ((e.source_id == node_id_a and e.target_id == node_id_b) or
                    (e.source_id == node_id_b and e.target_id == node_id_a))
        ]

        # Komşulardan çıkar
        self.nodes[node_id_a].neighbors.discard(node_id_b)
        self.nodes[node_id_b].neighbors.discard(node_id_a)

        # Bağlantı sayısını güncelle
        self.nodes[node_id_a].baglanti_sayisi = len(self.nodes[node_id_a].neighbors)
        self.nodes[node_id_b].baglanti_sayisi = len(self.nodes[node_id_b].neighbors)


    def get_neighbors(self, node_id: int) -> List[int]:
        if node_id not in self.nodes:
            return []
        return list(self.nodes[node_id].neighbors)

    def get_edge_weight(self, source_id: int, target_id: int) -> float:
        """
        İki node arasındaki edge'in ağırlığını döndürür.
        Edge yoksa ValueError fırlatır.
        """
        for e in self.edges:
            if e.a == source_id and e.b == target_id:
                return e.weight
        raise ValueError(f"{source_id} -> {target_id} arasında edge yok.")
  
    # ---- Ağırlık formülü ----
    @staticmethod
    def compute_weight(node_a: Node, node_b: Node) -> float:
        """
        W(i,j) = 1 / (1 + (A_i - A_j)^2 + (E_i - E_j)^2 + (B_i - B_j)^2)
        """
        da = node_a.aktiflik - node_b.aktiflik
        de = node_a.etkilesim - node_b.etkilesim
        db = node_a.baglanti_sayisi - node_b.baglanti_sayisi

        denom = 1.0 + da * da + de * de + db * db
        return 1.0 / denom
    
    # ---- Debug amaçlı ----
    def __repr__(self) -> str:
        return f"Graph(nodes={len(self.nodes)}, edges={len(self.edges)})"
