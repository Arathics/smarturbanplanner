import streamlit as st
from utils import sumo_pipeline, building_pipeline, accessibility, optimizer
import pandas as pd

st.set_page_config(layout="wide")
st.title("🧠 Smart Urban Planner")

uploaded_file = st.file_uploader("📂 Upload an OSM file", type=["osm"])

if uploaded_file:
    with open("input.osm", "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ OSM file uploaded!")

    net = sumo_pipeline.convert_osm_to_sumo("input.osm")
    trips, routes = sumo_pipeline.generate_trips(net)
    tripinfo = sumo_pipeline.simulate_traffic(net, routes)

    buildings_file = building_pipeline.extract_buildings("input.osm")
    clustered_file = building_pipeline.cluster_buildings(buildings_file)

    G = accessibility.get_road_graph()
    scores = accessibility.compute_accessibility_scores(G, clustered_file)

    result = optimizer.optimize_layout(tripinfo, clustered_file, scores)
    annotated = optimizer.annotate_buildings(clustered_file, result)

    st.subheader("📊 Land Use Recommendations")
    st.dataframe(pd.DataFrame(result))

    with open(annotated, "rb") as f:
        st.download_button("⬇️ Download GeoJSON", f, file_name="optimized_buildings.geojson")
