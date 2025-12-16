import csv
from core.graph import Graph
from core.node import Node

def export_nodes_to_csv(graph: Graph, filepath:str):
    with open(filepath, "w", newline="",encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id","aktiflik","etkilesim","baglanti_sayisi"])
        for n in graph.nodes.values():
            writer.writerow([n.id,n.aktiflik,n.etkilesim,len(n.neighbors)])
def import_nodes_from_csv(graph:Graph, filepath:str):
    with open(filepath, "r",encoding="utf-8") as f:
        reader=csv.DictReader(f)
        for row in reader:
            node=Node(
                int(row["id"]),
                float(row["aktiflik"]),
                float(row["etkilesim"]),
                int(row["baglanti_sayisi"])
            )
            if node.id not in graph.nodes:
                graph.add_node(node)