import osmnx as ox
import geopandas as gpd
import numpy as np
from sklearn.cluster import KMeans

def extract_buildings(osm_file, output="buildings.geojson"):
    buildings = ox.features_from_xml(osm_file, tags={"building": True})
    buildings.to_file(output, driver="GeoJSON")
    return output

def cluster_buildings(building_file, output="buildings_clustered.geojson", n_clusters=5):
    buildings = gpd.read_file(building_file).to_crs(epsg=32643)
    buildings["area"] = buildings.geometry.area
    buildings["centroid"] = buildings.geometry.centroid
    X = np.array(list(zip(buildings["centroid"].x, buildings["centroid"].y, buildings["area"])))
    kmeans = KMeans(n_clusters=n_clusters, n_init=10)
    buildings["cluster"] = kmeans.fit_predict(X)
    buildings.to_file(output, driver="GeoJSON")
    return output
