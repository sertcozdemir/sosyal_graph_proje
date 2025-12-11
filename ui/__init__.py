from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QBrush, QPen, QPainter
from PyQt5.QtCore import Qt

class GraphView(QGraphicsView):
    def __init__(self, graph: Graph, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.setBackgroundBrush(QBrush(Qt.white))
        self.setRenderHint(QPainter.Antialiasing)

        # En kısa yol vurgusu
        self.highlighted_path = []

        # Welsh–Powell renklendirme için node -> colorIndex map
        self.node_colors = {}  # {node_id: color_index}

        self.draw_graph()
def set_node_colors(self, color_map: dict[int, int]):
    """Welsh–Powell çıktısı buraya verilir."""
    self.node_colors = color_map or {}
    self.draw_graph()
