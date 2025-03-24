import osmnx as ox
import geopandas as gpd
import networkx as nx

def get_road_graph(place="Kozhikode, India"):
    G = ox.graph_from_place(place, network_type="drive")
    return ox.project_graph(G)

def compute_accessibility_scores(G, building_file):
    buildings = gpd.read_file(building_file).to_crs(G.graph["crs"])
    buildings["centroid"] = buildings.geometry.centroid
    representatives = buildings.loc[buildings.groupby("cluster")["area"].idxmax()].reset_index(drop=True)

    nearest_nodes = [
        ox.distance.nearest_nodes(G, pt.x, pt.y)
        for pt in representatives["centroid"]
    ]

    shortest_paths = {}
    for i, node1 in enumerate(nearest_nodes):
        for j, node2 in enumerate(nearest_nodes):
            if i < j:
                try:
                    dist = nx.shortest_path_length(G, node1, node2, weight="length")
                    shortest_paths[(i, j)] = dist
                except:
                    shortest_paths[(i, j)] = float('inf')

    scores = {
        i: sum([
            shortest_paths.get((min(i, j), max(i, j)), float("inf"))
            for j in range(len(nearest_nodes)) if i != j
        ])
        for i in range(len(nearest_nodes))
    }

    return scores
