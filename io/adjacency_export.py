import csv
from core.graph import Graph

def export_adjacency_list(graph: Graph, filepath:str):
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer=csv.writer(f)
        writer.writerow(["node", "neighbors"])
        for node_id, node in graph.nodes.items():
            writer.writerow([node_id, ",".join(map(str, sorted(node.neighbors)))])
def export_adjacency_matrix(graph:Graph, filepath:str):
    nodes=sorted(graph.nodes.keys())
    idx={n:i for i,n in enumerate(nodes)}
    matrix=[[0]*len(nodes) for _ in nodes]
    for a in nodes:
        for b in graph.nodes[a].neighbors:
            matrix[idx[a]][idx[b]] = 1
    with open(filepath, "w",newline="",encoding="utf-8") as f:
        writer=csv.writer(f)
        writer.writerow([""]+ nodes)
        for i,a in enumerate(nodes):
            writer.writerow([a] + matrix[i])