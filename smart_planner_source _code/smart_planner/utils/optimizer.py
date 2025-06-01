import networkx as nx
import pickle
import geojson
from shapely.geometry import LineString

def optimize_road_network(graph_path="data/road_graph.gpickle", output_geojson="data/optimized_layout.geojson"):
    with open(graph_path, "rb") as f:
        G = pickle.load(f)

    # 1. Identify high-cost edges (possible congestion zones)
    high_cost_edges = [(u, v, d) for u, v, d in G.edges(data=True) if d['weight'] >= 4]

    # 2. Analyze bottlenecks (nodes with few connections)
    bottlenecks = [node for node in G.nodes if G.degree(node) <= 1]

    print(f"🚦 Found {len(high_cost_edges)} high-cost edges")
    print(f"🧩 Found {len(bottlenecks)} potential bottlenecks")

    # 3. Remove bottlenecks (simplification step - optional)
    for node in bottlenecks:
        G.remove_node(node)

    # 4. Rebuild GeoJSON from cleaned graph
    features = []
    for u, v, data in G.edges(data=True):
        line = LineString([u, v])
        feature = geojson.Feature(
            geometry=geojson.LineString(list(line.coords)),
            properties={
                "type": data.get("type", "unknown"),
                "length": data.get("length", 0),
                "weight": data.get("weight", 0)
            }
        )
        features.append(feature)

    optimized = geojson.FeatureCollection(features)

    with open(output_geojson, "w", encoding="utf-8") as f:
        geojson.dump(optimized, f)

    print(f" Optimized layout saved to {output_geojson}")
