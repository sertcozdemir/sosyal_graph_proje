import random
import time
from core.graph import Graph
from core.node import Node
from graph_algorithms.bfs import bfs
from graph_algorithms.dfs import dfs
from graph_algorithms.dijkstra import dijkstra
def generate_random_graph(n_nodes: int, edge_prob:float =0.08)-> Graph:
    g = Graph()
    #node ekle
    for i in range(1,n_nodes + 1):
        aktiflik=random.random()
        etkilesim=random.randint(0,100)
        g.add_node(Node(i,aktiflik,etkilesim,0))
    #edge ekle
    node_ids=list(g.nodes.keys())
    for i in range(len(node_ids)):
        for j in range(i+1, len(node_ids)):
            if random.random() < edge_prob:
                g.add_undirected_edge(node_ids[i], node_ids[j])
    return g
def measure_algorithms(graph:Graph,start:int,goal:int):
    results={}
    t0=time.perf_counter()
    bfs(graph,start)
    results["BFS"]=time.perf_counter()-t0
    t0 = time.perf_counter()
    dfs(graph,start)
    results["DFS"] = time.perf_counter()-t0
    t0=time.perf_counter()
    dijkstra(graph,start,goal)
    results["Dijkstra"] = time.perf_counter()-t0
    return results
def run_performance_tests():
    tests=[]
    for n in [15,75]:
        g=generate_random_graph(n)
        ids=sorted(g.nodes.keys())
        start= ids[0]
        goal = ids[-1]
        times = measure_algorithms(g,start,goal)
        tests.append({
            "nodes":n,
            "edges": len(g.edges),
            "BFS": times["BFS"],
            "DFS": times["DFS"],
            "Dijkstra": times["Dijkstra"]

        })
        return tests

