import sys
from PyQt5.QtWidgets import QApplication

from core.node import Node
from core.graph import Graph
from ui.main_window import MainWindow
from graph_algorithms.dijkstra import dijkstra
from graph_algorithms.astar import astar



def build_sample_graph() -> Graph:
    g = Graph()

    # Örnek 4 node
    n1 = Node(1, aktiflik=0.8, etkilesim=12, baglanti_sayisi=0)
    n2 = Node(2, aktiflik=0.4, etkilesim=5, baglanti_sayisi=0)
    n3 = Node(3, aktiflik=0.9, etkilesim=20, baglanti_sayisi=0)
    n4 = Node(4, aktiflik=0.2, etkilesim=2, baglanti_sayisi=0)

    for n in [n1, n2, n3, n4]:
        g.add_node(n)

    # Bazı bağlantılar
    g.add_undirected_edge(1, 2)
    g.add_undirected_edge(1, 3)
    g.add_undirected_edge(2, 4)
    g.add_undirected_edge(3, 4)

    print(g)
    for e in g.edges:
        print(e)
    # Dijkstra & A* test
    dij = dijkstra(g, start_id=1, goal_id=4)
    print("Dijkstra path 1 -> 4:", dij.get("path"), "dist:", dij["dist"][4])

    ares = astar(g, start_id=1, goal_id=4)
    print("A*       path 1 -> 4:", ares.get("path"), "cost:", ares["g"][4])

    return g

    


def main():
    app = QApplication(sys.argv)

    graph = build_sample_graph()
    window = MainWindow(graph)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
