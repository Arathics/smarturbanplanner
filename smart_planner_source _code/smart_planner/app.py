# app.py

import streamlit as st
import os
import json
import numpy as np
from utils.traffic import run_traffic_simulation
from utils.energy import run_energy_optimization
from utils.output import generate_outputs
from utils.optimizer import optimize_road_network
from streamlit_folium import st_folium
import folium

# Configuration
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
st.set_page_config(
    page_title="Smart Urban Planner",
    layout="wide",
    page_icon="📍"
)

# ----- Custom CSS for Styling -----
st.markdown("""
    <style>
    html, body, .block-container {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f7f9fb;
        padding: 1.5rem;
    }
    h1 {
        color: #1f4e79;
        font-size: 2.75rem;
        font-weight: 700;
    }
    h3, .stSubheader {
        color: #0b3c5d;
    }
    .stButton > button, .stDownloadButton > button {
        background-color: #1f4e79;
        color: white;
        font-weight: 500;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        margin-top: 0.5rem;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background-color: #174060;
    }
    .stMarkdown > p {
        font-size: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ----- Header -----
st.title("📍 Smart Urban Planner")
st.markdown("""
A professional tool for **urban traffic and energy optimization** based on OpenStreetMap (OSM) data.

This application uses real-world geospatial information to generate optimized road networks that minimize traffic congestion and reduce energy consumption.
""")

# ----- Sidebar Settings -----
with st.sidebar:
    st.header("⚙️ Application Settings")
    optimize_energy = st.checkbox("Include energy optimization", value=True)
    show_debug = st.checkbox("Show debug information", value=False)

    st.markdown("---")
    st.subheader("ℹ️ About the Project")
    st.markdown("""
    The Smart Urban Planner leverages clustering algorithms and genetic optimization to analyze existing road networks and propose new layouts that offer:
    
    - ✅ Improved traffic flow through realistic inter-zone road generation  
    - ✅ Reduced total travel distance and energy consumption  
    - ✅ Compatibility with real-world topologies and constraints  

    **Note:** All optimizations are performed locally using uploaded OSM data.
    """)

# ----- File Upload -----
st.subheader("📤 1. Upload Road Network Data")
st.markdown("Please upload an OpenStreetMap (`.osm`) file for the area you wish to optimize.")
osm_file = st.file_uploader("Upload .osm file", type=["osm"])

if osm_file:
    osm_path = os.path.join(DATA_DIR, "uploaded.osm")
    with open(osm_path, "wb") as f:
        f.write(osm_file.read())
    st.success("✅ OSM file uploaded successfully.")

    st.subheader("⚡ 2. Run Optimization")
    st.markdown("""
This step will perform:
- 🚏 Road clustering and reconstruction  
- 🚦 Traffic signal optimization  
- 🔋 (Optional) Energy footprint minimization
""")

    if st.button("🚀 Start Optimization"):
        with st.spinner("Running full optimization process..."):
            run_traffic_simulation(osm_path)
            if optimize_energy:
                run_energy_optimization()
            generate_outputs(osm_path)
            optimize_road_network()
        st.success("✅ Optimization completed successfully.")
        st.session_state["optimization_done"] = True


# ----- Output and Visualization -----
if st.session_state.get("optimization_done") and os.path.exists("data/optimized_layout.geojson"):
    st.subheader("🗺️ 3. Optimized Layout Map")

    try:
        with open("data/optimized_layout.geojson", "r", encoding="utf-8") as f:
            geojson_data = json.load(f)

        # Auto-center map
        coordinates = []
        for feature in geojson_data["features"]:
            geom = feature["geometry"]
            if geom["type"] == "LineString":
                coordinates.extend(geom["coordinates"])
            elif geom["type"] == "MultiLineString":
                for line in geom["coordinates"]:
                    coordinates.extend(line)

        map_center = [11.2588, 75.7804]
        if coordinates:
            lngs, lats = zip(*coordinates)
            map_center = [np.mean(lats), np.mean(lngs)]

        m = folium.Map(location=map_center, zoom_start=14)
        folium.GeoJson(geojson_data, name="Optimized Network").add_to(m)
        folium.LayerControl().add_to(m)

        st_data = st_folium(m, width=800, height=600)

        st.download_button("📥 Download Optimized GeoJSON", open("data/optimized_layout.geojson", "rb"), "optimized_layout.geojson")

        # Optional energy report
        if optimize_energy and os.path.exists("data/energy_report.pdf"):
            st.download_button("📊 Download Energy Report", open("data/energy_report.pdf", "rb"), "energy_report.pdf")

    except Exception as e:
        st.error(f"Error reading map output: {e}")

# ----- Debug Info -----
if show_debug:
    st.subheader("🐞 Debug Information")
    try:
        with open("data/output.geojson", "r", encoding="utf-8") as f:
            data = json.load(f)
        st.json(data)
    except FileNotFoundError:
        st.warning("No output.geojson file found. Please run the optimization first.")
