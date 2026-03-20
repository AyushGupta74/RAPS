#Tried to parse graph using python library pyrosm but failed to do so because of inadequate memory(RAM).

from pyrosm import OSM
import os
import osmnx as ox


PBF_PATH = "data/raw/norcal-260127.osm.pbf"
OUTPUT_GRAPH = "data/san_francisco.graphml"



BBOX = [
    -122.4250,  # west
    37.7680,    # south
    -122.3950,  # east
    37.7920     # north
]

print("Loading OSM PBF file with bounding box...")
osm = OSM(
    PBF_PATH,
    bounding_box=BBOX
)

print("Extracting road network (driving)...")
nodes, edges = osm.get_network("driving")

print("Converting to NetworkX graph...")
G = ox.graph_from_gdfs(nodes, edges)

print("Adding edge speeds and travel times...")
G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)

print("Saving graph to disk...")
os.makedirs("data", exist_ok=True)
ox.save_graphml(G, OUTPUT_GRAPH)

print("✅ Offline OSM graph built successfully!")
