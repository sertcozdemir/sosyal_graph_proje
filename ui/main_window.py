from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QListWidget
)
from .graph_view import GraphView
from core.graph import Graph
from graph_algorithms.bfs import bfs
from graph_algorithms.dfs import dfs


class MainWindow(QMainWindow):

    def __init__(self, graph: Graph):
        super().__init__()
        self.graph = graph

        self.setWindowTitle("Sosyal Ağ Analizi Uygulaması - Proje II")
        self.resize(1000, 600)

        # ana widget
        central = QWidget()
        main_layout = QHBoxLayout(central)

        # SOL kısım = graf canvas
        self.graph_view.node_clicked.connect(self.on_node_clicked) = GraphView(self.graph)
        main_layout.addWidget(self.graph_view, stretch=3)

        # SAĞ kısım = kontrol paneli
        self.panel = self.build_panel()
        main_layout.addWidget(self.panel, stretch=1)

        self.setCentralWidget(central)

    def build_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Başlangıç node ID input
        layout.addWidget(QLabel("Başlangıç Node ID:"))
        self.start_input = QLineEdit()
        self.start_input.setPlaceholderText("Örn: 1")
        layout.addWidget(self.start_input)

        # BFS butonu
        btn_bfs = QPushButton("BFS Çalıştır")
        btn_bfs.clicked.connect(self.run_bfs)
        layout.addWidget(btn_bfs)

        # DFS butonu
        btn_dfs = QPushButton("DFS Çalıştır")
        btn_dfs.clicked.connect(self.run_dfs)
        layout.addWidget(btn_dfs)
            # ---------------- Node CRUD ----------------
        layout.addWidget(QLabel("Node İşlemleri"))

        # Node ID
        self.node_id_input = QLineEdit()
        self.node_id_input.setPlaceholderText("Node ID (örn: 5)")
        layout.addWidget(self.node_id_input)

        # Aktiflik
        self.node_active_input = QLineEdit()
        self.node_active_input.setPlaceholderText("Aktiflik (örn: 0.7)")
        layout.addWidget(self.node_active_input)

        # Etkileşim
        self.node_interaction_input = QLineEdit()
        self.node_interaction_input.setPlaceholderText("Etkileşim (örn: 10)")
        layout.addWidget(self.node_interaction_input)

        # Bağlantı sayısı (0 girilecek, otomatik güncellenir)
        self.node_degree_input = QLineEdit()
        self.node_degree_input.setPlaceholderText("Bağlantı Sayısı (örn: 0)")
        layout.addWidget(self.node_degree_input)

        # Node Ekle
        btn_add_node = QPushButton("Node Ekle")
        btn_add_node.clicked.connect(self.add_node)
        layout.addWidget(btn_add_node)

        # Node Sil
        btn_del_node = QPushButton("Node Sil")
        btn_del_node.clicked.connect(self.delete_node)
        layout.addWidget(btn_del_node)

        # Node Güncelle
        btn_update_node = QPushButton("Node Güncelle")
        btn_update_node.clicked.connect(self.update_node)
        layout.addWidget(btn_update_node)
                # ---------------- Edge İşlemleri ----------------
        layout.addWidget(QLabel("Bağlantı (Edge) İşlemleri"))

        self.edge_src_input = QLineEdit()
        self.edge_src_input.setPlaceholderText("Kaynak Node ID (örn: 1)")
        layout.addWidget(self.edge_src_input)

        self.edge_dst_input = QLineEdit()
        self.edge_dst_input.setPlaceholderText("Hedef Node ID (örn: 2)")
        layout.addWidget(self.edge_dst_input)

        btn_add_edge = QPushButton("Bağlantı Ekle (Çift Yönlü)")
        btn_add_edge.clicked.connect(self.add_edge)
        layout.addWidget(btn_add_edge)

        btn_del_edge = QPushButton("Bağlantı Sil (Çift Yönlü)")
        btn_del_edge.clicked.connect(self.delete_edge)
        layout.addWidget(btn_del_edge)

        

        

        # Sonuç listesi
        layout.addWidget(QLabel("Sonuçlar:"))
        self.result_list = QListWidget()
        layout.addWidget(self.result_list)

        layout.addStretch()

        return panel

    # --------- BFS ÇALIŞTIR -----------
    def run_bfs(self):
        start = int(self.start_input.text())
        result = bfs(self.graph, start)
        self.show_result(result["visited_order"])

    # --------- DFS ÇALIŞTIR -----------
    def run_dfs(self):
        start = int(self.start_input.text())
        result = dfs(self.graph, start)
        self.show_result(result["visited_order"])

    # --------- SONUÇ GÖSTERME -----------
    def show_result(self, visited_order):
        self.result_list.clear()
        for v in visited_order:
            self.result_list.addItem(str(v))
    def add_node(self):
        try:
            node_id = int(self.node_id_input.text())
            aktiflik = float(self.node_active_input.text())
            etkilesim = float(self.node_interaction_input.text())
            bag_sayisi = int(self.node_degree_input.text())
        except:
            self.show_result(["Hata: Geçerli değerler girin"])
            return

        from core.node import Node

        # Aynı ID'de node varsa hata
        if node_id in self.graph.nodes:
            self.show_result([f"Node {node_id} zaten var!"])
            return

        new_node = Node(node_id, aktiflik, etkilesim, bag_sayisi)
        self.graph.add_node(new_node)

        # grafi güncelle
        self.graph_view.draw_graph()
        self.show_result([f"Node {node_id} başarıyla eklendi."])
    def delete_node(self):
        try:
            node_id = int(self.node_id_input.text())
        except:
            self.show_result(["Hata: Node ID geçersiz"])
            return

        if node_id not in self.graph.nodes:
            self.show_result([f"Node {node_id} bulunamadı"])
            return

        self.graph.remove_node(node_id)
        self.graph_view.draw_graph()
        self.show_result([f"Node {node_id} silindi"])
    def update_node(self):
        try:
            node_id = int(self.node_id_input.text())
            aktiflik = float(self.node_active_input.text())
            etkilesim = float(self.node_interaction_input.text())
            bag_sayisi = int(self.node_degree_input.text())
        except:
            self.show_result(["Hata: Değerler geçersiz"])
            return

        if node_id not in self.graph.nodes:
            self.show_result([f"Node {node_id} mevcut değil"])
            return

        node = self.graph.nodes[node_id]

        # Güncelleme
        node.aktiflik = aktiflik
        node.etkilesim = etkilesim
        node.baglanti_sayisi = bag_sayisi

        # Grafik güncelle
        self.graph_view.draw_graph()
        self.show_result([f"Node {node_id} güncellendi"])
    def add_edge(self):
        try:
            src = int(self.edge_src_input.text())
            dst = int(self.edge_dst_input.text())
        except:
            self.show_result(["Hata: Geçerli node ID'leri girin"])
            return

        if src == dst:
            self.show_result(["Hata: Self-loop yasak (aynı node'a edge yok)"])
            return

        if src not in self.graph.nodes or dst not in self.graph.nodes:
            self.show_result(["Hata: Node'lardan biri graf içinde yok"])
            return

        try:
            self.graph.add_undirected_edge(src, dst)
        except ValueError as e:
            self.show_result([f"Hata: {e}"])
            return

        self.graph_view.draw_graph()
        self.show_result([f"{src} - {dst} arasında çift yönlü bağlantı eklendi."])

    def delete_edge(self):
        try:
            src = int(self.edge_src_input.text())
            dst = int(self.edge_dst_input.text())
        except:
            self.show_result(["Hata: Geçerli node ID'leri girin"])
            return

        if src not in self.graph.nodes or dst not in self.graph.a:
            self.show_result(["Hata: Node'lardan biri graf içinde yok"])
            return

        self.graph.remove_undirected_edge(src, dst)
        self.graph_view.draw_graph()
        self.show_result([f"{src} - {dst} arasındaki çift yönlü bağlantı silindi."])

    



