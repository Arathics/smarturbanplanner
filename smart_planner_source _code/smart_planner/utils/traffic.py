import pickle
import os

def estimate_total_congestion(graph):
    # Basic congestion = edge weight * average degree of connected nodes
    return sum(
        data["weight"] * (graph.degree(u) + graph.degree(v)) / 2
        for u, v, data in graph.edges(data=True)
    )

def run_traffic_simulation(osm_path=None):
    print(" Running traffic congestion estimation...")
    graph_path = os.path.join("data", "road_graph.gpickle")
    if not os.path.exists(graph_path):
        print(" road_graph.gpickle not found. Make sure to generate outputs first.")
        return

    with open(graph_path, "rb") as f:
        G = pickle.load(f)

    congestion_score = estimate_total_congestion(G)
    print(f" Estimated total congestion: {congestion_score:.2f}")
