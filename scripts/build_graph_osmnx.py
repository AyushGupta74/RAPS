import os
import osmnx as ox

OUTPUT_GRAPH = "data/san_francisco.graphml"

print("Downloading San Francisco road network (drive)...")

G = ox.graph_from_place(
    "San Francisco, California, USA",
    network_type="drive",
    simplify=True
)

print("Adding edge speeds and travel times...")
G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)

os.makedirs("data", exist_ok=True)
ox.save_graphml(G, OUTPUT_GRAPH)

print("✅ San Francisco graph built and saved successfully!")
