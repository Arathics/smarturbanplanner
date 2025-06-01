# Smart Urban Planner

Smart Urban Planner is a web-based application designed to optimize urban road networks using real-world OpenStreetMap (OSM) data. By leveraging clustering algorithms and multi-objective genetic optimization, it reconstructs road layouts that aim to reduce traffic congestion and energy consumption while preserving realistic connectivity.

## Project Description

The application processes uploaded OSM files to analyze and reconstruct urban infrastructure. It clusters roads into functional zones, generates inter-zone connections, and applies optimization techniques to improve layout efficiency. The system supports visualization of the optimized layout and provides downloadable output files for further use.

## Key Features

- Upload and parse `.osm` files
- Zone-based clustering using KMeans
- Reconstruction of road networks with interconnectivity
- Traffic signal optimization and congestion reduction
- Energy optimization using traffic flow data
- Exportable outputs in GeoJSON and PDF formats
- Interactive map visualization using Streamlit and Folium

## System Architecture

- **Frontend:** Streamlit-based UI for interaction and visualization
- **Backend Modules:**
  - `traffic.py`: Simulates and analyzes traffic
  - `energy.py`: Estimates and minimizes energy usage
  - `output.py`: Builds synthetic road layouts and generates outputs
  - `optimizer.py`: Applies genetic algorithms to optimize road networks

## Folder Structure

```
Smart_Planner/
├── app.py                  # Main Streamlit application
├── utils/
│   ├── traffic.py          # Traffic simulation
│   ├── energy.py           # Energy modeling
│   ├── output.py           # Road layout generation
│   └── optimizer.py        # Optimization engine
├── data/                   # Uploaded and generated files
│   ├── uploaded.osm
│   ├── optimized_layout.geojson
│   └── energy_report.pdf
├── main3.pdf               # Research paper reference
├── requirements.txt        # Python dependencies
└── README.md               # Documentation
```

## Setup Instructions

1. Clone the file:

```bash

cd Smart_Planner
```

2. Install Dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Application:

```bash
streamlit run app.py
```

## Usage Guide

1. Launch the app and upload an `.osm` file.
2. Choose whether to include energy optimization.
3. Click "Start Optimization" to begin processing.
4. View the results on the map.
5. Download the GeoJSON or energy report.

## Output Files

- `optimized_layout.geojson`: Optimized road layout
- `energy_report.pdf`: Energy efficiency report
- `output.geojson`: Visualizable intermediate output
- `uploaded.osm`: User-provided source file

## Optimization Methodology

The system applies logic from `main3.pdf`, including:
- Zone clustering via KMeans
- Synthetic interconnection of clusters
- Multi-objective optimization minimizing travel time and energy cost

## Dependencies

- osmnx==2.0.2
- streamlit
- geopandas
- shapely
- scikit-learn
- folium
- numpy
- networkx
- matplotlib
