from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import Qt
from math import cos, sin, pi
from PyQt5.QtGui import QBrush, QPen, QPainter

from core.graph import Graph


class GraphView(QGraphicsView):
    def __init__(self, graph: Graph, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Arka plan rengi
        self.setBackgroundBrush(QBrush(Qt.white))
        self.setRenderHint(QPainter.Antialiasing)
        self.highlighted_path = []
        self.node_colors = {}

        self.draw_graph()

    def draw_graph(self):
        self.scene.clear()

        if not self.graph.nodes:
            return

        # Node'ları dairesel yerleştirelim (şimdilik)
        node_ids = list(self.graph.nodes.keys())
        n = len(node_ids)
        radius = 150
        center_x, center_y = 0, 0

        positions = {}

        for idx, node_id in enumerate(node_ids):
            angle = 2 * pi * idx / n
            x = center_x + radius * cos(angle)
            y = center_y + radius * sin(angle)
            positions[node_id] = (x, y)

        # Önce edge'leri çiz
        pen_edge = QPen(Qt.black)
        for edge in self.graph.edges:
            x1, y1 = positions[edge.source_id]
            x2, y2 = positions[edge.target_id]
            self.scene.addLine(x1, y1, x2, y2, pen_edge)

        # Sonra node'ları çiz
        pen_node = QPen(Qt.black)
        brush_node = QBrush(Qt.blue)

        node_radius = 12
        for node_id, (x, y) in positions.items():
            ellipse = self.scene.addEllipse(
                x - node_radius, y - node_radius,
                2 * node_radius, 2 * node_radius,
                pen_node, brush_node
            )
            # Node id yazısı
            self.scene.addText(str(node_id)).setPos(x + 10, y + 10)
    def set_node_colors(self, color_map: dict[int, int]):
        """Welsh–Powell çıktısı buraya verilir."""
        self.node_colors = color_map or {}
        self.draw_graph()

