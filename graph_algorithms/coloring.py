from typing import Dict, List
from core.graph import Graph


class Coloring:
    """
    Welsh–Powell graf renklendirme algoritmasını çalıştıran sınıf.
    """

    def __init__(self, graph: Graph):
        self.graph = graph

    def welsh_powell(self) -> Dict[int, int]:
        """
        Welsh–Powell algoritması:
          - Node'ları dereceye göre azalan sırada sırala
          - Mümkün olduğunca az renk kullanarak renklendir

        Dönüş:
          { node_id: color_index }
        """
        graph = self.graph

        # (node_id, degree) listesi
        nodes_with_degree: List[tuple[int, int]] = []
        for node_id, node in graph.nodes.items():
            degree = len(node.neighbors)
            nodes_with_degree.append((node_id, degree))

        # dereceye göre azalan sırala
        nodes_with_degree.sort(key=lambda x: x[1], reverse=True)

        colors: Dict[int, int] = {}  # node_id -> color_index
        current_color = 0

        # tüm node'lar renklendirilene kadar devam et
        for node_id, _ in nodes_with_degree:
            if node_id in colors:
                continue  # zaten renklendirilmiş

            # Bu node'a yeni rengi ata
            colors[node_id] = current_color

            # Aynı rengi alabilecek diğerlerini bul
            for other_id, _ in nodes_with_degree:
                if other_id in colors:
                    continue

                # other_id, current_color'a atanmış hiçbir node'un komşusu olmamalı
                conflict = False
                for colored_node, c in colors.items():
                    if c == current_color:
                        if (other_id in graph.nodes[colored_node].neighbors or
                                colored_node in graph.nodes[other_id].neighbors):
                            conflict = True
                            break

                if not conflict:
                    colors[other_id] = current_color

            current_color += 1

        return colors
