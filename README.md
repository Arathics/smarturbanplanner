  

---

## **🚀 Urban Traffic Simulation & Optimization**
This project uses **SUMO (Simulation of Urban Mobility)** and **OpenStreetMap (OSM)** data to generate and optimize traffic flow in urban areas.

### **📁 Project Structure**
```
├── utils/                  # Utility scripts for preprocessing
├── venv/                   # Virtual environment (optional)
├── .gitignore              # Git ignore file
├── README.md               # Project documentation
├── app.py                  # Main application script
├── input.osm               # OpenStreetMap data for the target area
├── network.net.xml         # SUMO network file
├── requirements.txt        # Python dependencies
├── routes.rou.xml          # Vehicle route definitions
├── tripinfo.xml            # Output file with simulation results
├── trips.trips.xml         # Trip definitions for SUMO simulation
```

---

## **🛠️ Setup Instructions**
### **1️⃣ Install Dependencies**
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/Arathics/smarturbanplanner/
cd smarturbanplanner
pip install -r requirements.txt
```

### **2️⃣ Install SUMO**
Ensure you have **SUMO** installed. You can install it using:
```bash
sudo apt update && sudo apt install sumo sumo-tools sumo-doc
```
Or download it from [SUMO official website](https://sumo.dlr.de/docs/Downloads.html).

### **3️⃣ Prepare the Network**
Convert the **OSM file** (`input.osm`) into a **SUMO network**:
```bash
netconvert --osm-files input.osm -o network.net.xml
```

### **4️⃣ Generate Routes & Trips**
Generate traffic demand:
```bash
python utils/generate_routes.py
```

### **5️⃣ Run the Simulation**
Run the SUMO simulation:
```bash
sumo-gui -n network.net.xml -r routes.rou.xml
```
For command-line mode:
```bash
sumo -n network.net.xml -r routes.rou.xml --tripinfo-output tripinfo.xml
```

---

## **📊 Output Files**
- **tripinfo.xml** → Simulation results with trip times, waiting times, etc.
- **network.net.xml** → SUMO road network generated from **OSM**.
- **routes.rou.xml** → Vehicle route definitions.

---

## **📌 Features**
✔ Convert **OSM data** into a **SUMO network**  
✔ Optimize urban layouts for **better traffic flow**  
✔ Analyze **trip times, delays, and congestion**  

---

## **🔗 References**
- **SUMO Docs:** [https://sumo.dlr.de/docs](https://sumo.dlr.de/docs)
- **OSMnx:** [https://github.com/gboeing/osmnx](https://github.com/gboeing/osmnx)

---

## **👨‍💻 Author**
Developed by **Arathi Pradeep**  
For any questions, open an **issue** or contact me.

---

