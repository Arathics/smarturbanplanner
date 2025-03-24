import geopandas as gpd
import numpy as np

def normalize(values):
    values = np.array(values)
    return (values - values.min()) / (values.max() - values.min() + 1e-6)

def optimize_layout(tripinfo_file, buildings_file, access_scores):
    cluster_ids = list(access_scores.keys())
    traffic_score = normalize(np.random.rand(len(cluster_ids)))  # Placeholder
    energy_score = normalize(np.random.rand(len(cluster_ids)))   # Placeholder
    access_score = normalize([access_scores[c] for c in cluster_ids])

    recommendations = []
    for i, cluster_id in enumerate(cluster_ids):
        if traffic_score[i] < 0.4 and energy_score[i] > 0.6 and access_score[i] > 0.5:
            use = "High-density Housing 🟢"
        elif traffic_score[i] > 0.7 and access_score[i] < 0.3:
            use = "Avoid Development 🔴"
        else:
            use = "Commercial / Mixed Use 🟡"

        recommendations.append({
            "cluster": int(cluster_id),
            "traffic_score": round(float(traffic_score[i]), 2),
            "energy_score": round(float(energy_score[i]), 2),
            "access_score": round(float(access_score[i]), 2),
            "recommended_use": use
        })

    return recommendations

def annotate_buildings(building_file, recommendations, output="annotated_buildings.geojson"):
    buildings = gpd.read_file(building_file)
    rec_map = {r["cluster"]: r["recommended_use"] for r in recommendations}
    buildings["recommended_use"] = buildings["cluster"].map(rec_map)
    buildings.to_file(output, driver="GeoJSON")
    return output
