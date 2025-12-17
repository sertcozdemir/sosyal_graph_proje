from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QListWidget,QFileDialog,
    QTableWidget,QTableWidgetItem,QListWidgetItem
)
from .graph_view import GraphView
from core.graph import Graph
from graph_algorithms.bfs import bfs
from graph_algorithms.dfs import dfs
from data_io.csv_manager import export_nodes_to_csv, import_nodes_from_csv
from data_io.adjacency_export import export_adjacency_list, export_adjacency_matrix


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
        self.graph_view = GraphView(self.graph)
        self.graph_view.node_clicked.connect(self.on_node_clicked)
        main_layout.addWidget(self.graph_view)

        # SAĞ kısım = kontrol paneli
        self.panel = self.build_panel()
        main_layout.addWidget(self.panel, stretch=1)

        self.setCentralWidget(central)

    def build_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        btn_csv_export =QPushButton("Node CSV Dışa aktar")
        btn_csv_export.clicked.connect(self.export_nodes_csv)
        layout.addWidget(btn_csv_export)
        btn_csv_import=QPushButton("Node CSV İçeri aktar")
        btn_csv_import.clicked.connect(self.import_nodes_csv)
        layout.addWidget(btn_csv_import)
        btn_adj_list=QPushButton("Komşuluk Listesi (CSV)")
        btn_adj_list.clicked.connect(self.export_adj_list)
        layout.addWidget(btn_adj_list)
        btn_adj_matrix = QPushButton("Komşuluk Matrisi (CSV)")
        btn_adj_matrix.clicked.connect(self.export_adj_matrix)
        layout.addWidget(btn_adj_matrix)
        btn_top5=QPushButton("En Etkili 5 Kullanıcı")
        btn_top5.clicked.connect(self.show_top5_centrality)
        layout.addWidget(btn_top5)
        btn_perf=QPushButton("Performans Testi Çalıştır")
        btn_perf.clicked.connect(self.run_performance_test)
        layout.addWidget(btn_perf)
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
        try:
            self.graph.remove_undirected_edge(src,dst)
        except ValueError as e:
            self.show_result([f"Hata: {e}"])

        self.graph_view.draw_graph()
        self.show_result([f"{src} - {dst} arasındaki çift yönlü bağlantı silindi."])
    def export_nodes_csv(self):
        path, _ = QFileDialog.getSaveFileName(self,"CSV Kaydet", "","CSV(*.csv)")
        if path:
            export_nodes_to_csv(self.graph, path)
            self.show_result([f"Node CSV Kaydedildi: {path}"])
    def import_nodes_csv(self):
        path, _=QFileDialog.getOpenFileName(self, "CSV Yükle", "", "CSV (*.csv)")
        if path:
            import_nodes_from_csv(self.graph, path)
            self.graph_view.draw_graph()
            self.show_result([f"Node CSV Yüklendi: {path}"])
    def export_adj_list(self):
        path, _ =QFileDialog.getSaveFileName(self, "Komşuluk Listesi", "", "CSV (*.csv)")
        if path:
            export_adjacency_list(self.graph, path)
            self.show_result([f"Komşuluk Listesi kaydedildi: {path}"])
    def export_adj_matrix(self):
        path, _ =QFileDialog.getSaveFileName(self, "Komşuluk Matrisi", "", "CSV(*.csv)")
        if path:
            export_adjacency_matrix(self.graph, path)
            self.show_result([f"Komşuluk matrisi kaydedildi:{path}"])
    def show_top5_centrality(self):
        from graph_algorithms.centrality import DegreeCentrality
        dc = DegreeCentrality(self.graph)
        top5=dc.top_k(5)
        table=QTableWidget()
        table.setRowCount(len(top5))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels([
            "Sıra",
            "Node ID",
            "Degree Centrality"
        ])
        for row, (node_id, score) in enumerate(top5):
            table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            table.setItem(row, 1, QTableWidgetItem(str(node_id)))
            table.setItem(row,2, QTableWidgetItem(f"{score:.3f}"))
        table.resizeColumnsToContents()
        self.result_list.clear()
        self.result_list.addItem("En Etkili 5 Kullanıcı (Degree Centrality):")
        self.result_list.addItem("")
        item = QListWidgetItem()
        item.setSizeHint(table.sizeHint())
        self.result_list.addItem(item)
        self.result_list.setItemWidget(item, table)
    def on_node_clicked(self,node_id:int):
        if node_id not in self.graph.nodes:
            self.show_result([f"Node bulunamadı: {node_id}"])
            return
        node = self.graph.nodes[node_id]
        neighbors=sorted(list(node.neighbors))
        lines = [
            f"Seçilen Node:{node_id}",
            f"Aktiflik: {node.aktiflik}",
            f"Etkileşim:{node.etkilesim}",
            f"Bağlantı Sayısı: {len(node.neighbors)}",
            f"Komşular: {', '.join(map(str,neighbors)) if neighbors else '(yok)'}",
        ]
        self.show_result(lines)
        if hasattr(self,"node_id_input"):
            self.node_id_input.setText(str(node.id))
        if hasattr(self, "node_activate_input"):
            self.node_active_input.setText(str(node.aktiflik))
        if hasattr(self, "node_interaction_input"):
            self.node_interaction_input.setText(str(node.etkilesim))
    def run_performance_test(self):
        from graph_algorithms.performance import run_performance_tests
        from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem,QListWidgetItem
        results = run_performance_tests()
        table = QTableWidget()
        table.setRowCount(len(results))
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels([
            "Düğüm Sayısı",
            "Edge Sayısı",
            "BFS (s)",
            "DFS (s)",
            "Dijkstra (s)"
        ])
        for row,r in enumerate(results):
            table.setItem(row,0,QTableWidgetItem(str(r["nodes"])))
            table.setItem(row,1,QTableWidgetItem(str(r["edges"])))
            table.setItem(row,2,QTableWidgetItem(f"{r['BFS']:.6f}"))
            table.setItem(row,2,QTableWidgetItem(f"{r['DFS']:.6f}"))
            table.setItem(row,2,QTableWidgetItem(f"{r['Dijkstra']:.6f}"))
        table.resizeColumnToContents()
        self.result_list.clear()
        self.result_list.addItem("Performans Test Sonuçları")
        self.result_list.addItem("")
        item = QListWidgetItem()
        item.setSizeHint(table.sizeHint())
        self.result_list.addItem(item)
        self.result_list.setItemWidget(item,table)




    



