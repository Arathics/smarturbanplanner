import subprocess

def convert_osm_to_sumo(osm_file, net_file="network.net.xml"):
    cmd = ["netconvert", "--osm-files", osm_file, "--output-file", net_file]
    subprocess.run(cmd, check=True)
    return net_file

def generate_trips(net_file, trip_file="trips.trips.xml", route_file="routes.rou.xml"):
    cmd = ['python', 'C:/Program Files (x86)/Eclipse/Sumo/tools/randomTrips.py', '-n', 'network.net.xml', '-o', 'trips.trips.xml', '-r', 'routes.rou.xml', '--period', '10']

    subprocess.run(cmd, check=True)
    return trip_file, route_file

def simulate_traffic(net_file, route_file, tripinfo_output="tripinfo.xml"):
    cmd = [
        "sumo",
        "-n", net_file,
        "-r", route_file,
        "--tripinfo-output", tripinfo_output
    ]
    subprocess.run(cmd, check=True)
    return tripinfo_output
