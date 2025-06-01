import osmium
import geojson
import os
import networkx as nx
import numpy as np
from shapely.geometry import LineString, Point
from sklearn.cluster import KMeans
import random
import pickle
from utils import traffic, energy

class RoadCollector(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.edges = []

    def way(self, w):
        if 'highway' in w.tags and len(w.nodes) > 1:
            coords = [(node.lon, node.lat) for node in w.nodes]
            for i in range(len(coords) - 1):
                self.edges.append((coords[i], coords[i + 1]))

def cluster_nodes(nodes, n_clusters=10):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(nodes)
    return kmeans.labels_, kmeans.cluster_centers_

def build_graph(edges):
    G = nx.Graph()
    for u, v in edges:
        dist = np.linalg.norm(np.array(u) - np.array(v))
        G.add_edge(u, v, weight=dist, original=True)
    return G

def add_realistic_intercluster_edges(G, labels, centroids):
    features = []
    centroid_nodes = [min(G.nodes, key=lambda n: np.linalg.norm(np.array(n) - c)) for c in centroids]

    for i in range(len(centroid_nodes)):
        for j in range(i + 1, len(centroid_nodes)):
            u = centroid_nodes[i]
            v = centroid_nodes[j]
            if not G.has_edge(u, v):
                try:
                    path = nx.shortest_path(G, source=u, target=v, weight='weight')
                    path_coords = [list(node) for node in path]
                    for k in range(len(path) - 1):
                        dist = np.linalg.norm(np.array(path[k]) - np.array(path[k+1]))
                        G.add_edge(path[k], path[k+1], weight=dist, original=False)
                    features.append(geojson.Feature(
                        geometry=geojson.LineString(path_coords),
                        properties={"type": "optimized"}
                    ))
                except nx.NetworkXNoPath:
                    continue
    return features

def mutate_graph(graph):
    new_graph = graph.copy()
    edges = list(new_graph.edges(data=True))
    for u, v, data in edges:
        if data.get("original", True):
            new_graph[u][v]["weight"] *= random.uniform(0.95, 1.05)
        else:
            if random.random() < 0.3:
                new_graph.remove_edge(u, v)
            else:
                new_graph[u][v]["weight"] *= random.uniform(0.8, 1.2)
    return new_graph

def evaluate_graph(graph):
    if nx.is_connected(graph):
        congestion = traffic.estimate_total_congestion(graph)
        energy_cost = energy.estimate_total_energy(graph)
        return 1 / (1 + congestion + energy_cost)
    return 0

def optimize_layout(graph, generations=50, population_size=10):
    population = [mutate_graph(graph) for _ in range(population_size)]
    best_graph = graph
    best_score = evaluate_graph(graph)
    for _ in range(generations):
        new_population = []
        for g in population:
            mutated = mutate_graph(g)
            score = evaluate_graph(mutated)
            if score > best_score:
                best_graph = mutated
                best_score = score
            new_population.append(mutated)
        population = new_population
    return best_graph

def generate_outputs(osm_file="data/uploaded.osm", output_geojson="data/output.geojson"):
    collector = RoadCollector()
    collector.apply_file(osm_file, locations=True)

    if not collector.edges:
        print(" No roads found in OSM file.")
        return

    G = build_graph(collector.edges)
    all_nodes = list(G.nodes())
    if len(all_nodes) < 10:
        print(" Not enough nodes for clustering.")
        return

    labels, centroids = cluster_nodes(all_nodes, n_clusters=8)
    synthetic_features = add_realistic_intercluster_edges(G, labels, centroids)

    G_with_synthetic = G.copy()
    for feature in synthetic_features:
        coords = feature.geometry.coordinates
        for i in range(len(coords) - 1):
            u, v = tuple(coords[i]), tuple(coords[i+1])
            dist = np.linalg.norm(np.array(u) - np.array(v))
            G_with_synthetic.add_edge(u, v, weight=dist, original=False)

    optimized_graph = optimize_layout(G_with_synthetic)

    features = []
    for u, v, data in optimized_graph.edges(data=True):
        coords = [list(u), list(v)]
        props = {
            "type": "original" if data.get("original", False) else "optimized",
            "weight": data["weight"]
        }
        features.append(geojson.Feature(geometry=geojson.LineString(coords), properties=props))

    feature_collection = geojson.FeatureCollection(features)
    with open(output_geojson, "w", encoding="utf-8") as f:
        geojson.dump(feature_collection, f)

    print(f" Generated {len(features)} roads to {output_geojson}")
    print(f" Graph has {len(optimized_graph.nodes)} nodes and {len(optimized_graph.edges)} edges")

    with open("data/road_graph.gpickle", "wb") as f:
        pickle.dump(optimized_graph, f)
