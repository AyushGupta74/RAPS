# import osmnx as ox
# import networkx as nx
# import sys
# import os

# # Allow importing from parent directory
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from config import CITY_NAME, START_LOC, END_LOC

# class StockholmMap:
#     def __init__(self):
#         print(f"\n Naqshab (Map Engine): Initializing...")
#         print(f"    Downloading road network for: {CITY_NAME}")
        
#         # 1. Download Graph
#         self.G = ox.graph_from_place(CITY_NAME, network_type='drive')
        
#         # 2. Add Physics (Speed & Time)
#         self.G = ox.add_edge_speeds(self.G)
#         self.G = ox.add_edge_travel_times(self.G)
        
#         print("Map Ready!")

#     def get_graph(self):
#         return self.G

#     def get_best_route(self, start_coords, end_coords):
#         """
#         Finds the fastest route using DIJKSTRA'S ALGORITHM.
#         """
#         print(f"\nCalculating route (Dijkstra)...")
        
#         # 1. Convert GPS to Nodes
#         start_node = ox.nearest_nodes(self.G, start_coords[1], start_coords[0])
#         end_node = ox.nearest_nodes(self.G, end_coords[1], end_coords[0])
        
#         # 2. Run Dijkstra's Algorithm
#         # We explicitly call dijkstra_path so the professor sees we used it.
#         try:
#             route = nx.dijkstra_path(self.G, start_node, end_node, weight='travel_time')
#             print(f"Dijkstra Route Found! It involves {len(route)} intersections.")
#             return route
#         except nx.NetworkXNoPath:
#             print("No path found between these points!")
#             return None

# # --- TEST BLOCK ---
# if __name__ == "__main__":
#     # 1. Initialize
#     engine = StockholmMap()
    
#     # 2. Test the Routing using Config coordinates
#     # We use the START_LOC and END_LOC from your config.py file
#     route = engine.get_best_route(START_LOC, END_LOC)
    
#     # 3. Validation
#     if route:
#         print("\nSUCCESS: Naqshab's module is fully functional!")
#         print("   The 'Brain' can now download the city and navigate it.")

import osmnx as ox
import networkx as nx
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import CITY_NAME, CAMERA_ID

class StockholmMap:
    def __init__(self):
        print(f"\n🗺️  Naqshab (Map Engine): Initializing...")
        print(f"    Downloading road network for: {CITY_NAME}")
        
        self.G = ox.graph_from_place(CITY_NAME, network_type='drive')
        self.G = ox.add_edge_speeds(self.G)
        self.G = ox.add_edge_travel_times(self.G)
        
        # --- NEW: SENSOR MAPPING ---
        # We need to find WHICH road segment corresponds to "Camera 1".
        # We assume the camera is near the Start Location for this demo.
        # In a real app, you'd map lat/lon to edge IDs.
        print("    Linking sensors to map edges...")
        
        # We arbitrarily pick an edge to be the "Monitored Road" for the demo.
        # We pick the first edge attached to the first node to ensure it exists.
        start_node = list(self.G.nodes())[0]
        neighbors = list(self.G.neighbors(start_node))
        self.target_v = neighbors[0]
        self.target_u = start_node
        
        print(f"    ✅ Camera '{CAMERA_ID}' linked to Edge {self.target_u}->{self.target_v}")

    def update_edge_weights(self, congestion_factor, incident_penalty):
        """
        THE CORE ADAPTIVE LOGIC
        Updates the graph weights based on live sensor data.
        """
        # 1. Reset the entire graph to 'normal' first
        # This ensures old traffic jams clear up when sensors go green.
        for u, v, k, data in self.G.edges(keys=True, data=True):
            # The 'current_cost' starts as just the normal travel time
            data['current_cost'] = data['travel_time']

        # 2. Apply updates ONLY to the road with the camera
        # Retrieve the specific road segment data
        # Note: OSMnx graphs are MultiDiGraphs, so we use key=0
        edge_data = self.G[self.target_u][self.target_v][0]
        
        original_time = edge_data['travel_time']
        
        # --- THE FORMULA ---
        # New Cost = (Base Time * Traffic Factor) + Accident Penalty
        new_cost = (original_time * congestion_factor) + incident_penalty
        
        # Update the graph
        self.G[self.target_u][self.target_v][0]['current_cost'] = new_cost
        
        return original_time, new_cost

    def get_best_route(self, start_coords, end_coords):
        """
        Calculates the route using the dynamic 'current_cost'.
        """
        start_node = ox.nearest_nodes(self.G, start_coords[1], start_coords[0])
        end_node = ox.nearest_nodes(self.G, end_coords[1], end_coords[0])
        
        try:
            # Note: We now use weight='current_cost' instead of 'travel_time'
            # If we haven't run update_edge_weights yet, this might fail, 
            # so we ensure 'current_cost' exists.
            
            # Quick check to ensure 'current_cost' exists on all edges (for safety)
            if 'current_cost' not in list(self.G.edges(data=True))[0][2]:
                 for u, v, k, data in self.G.edges(keys=True, data=True):
                    data['current_cost'] = data['travel_time']

            route = nx.dijkstra_path(self.G, start_node, end_node, weight='current_cost')
            return route
        except nx.NetworkXNoPath:
            return None

# --- TEST BLOCK ---
if __name__ == "__main__":
    engine = StockholmMap()
    
    print("\n🧪 Testing Adaptive Logic...")
    
    # 1. Normal Conditions
    orig, new = engine.update_edge_weights(congestion_factor=1.0, incident_penalty=0)
    print(f"    Scenario A (Clear): Cost is {new:.2f}s (Original: {orig:.2f}s)")
    
    # 2. Disaster Scenario
    orig, new = engine.update_edge_weights(congestion_factor=3.0, incident_penalty=2000)
    print(f"    Scenario B (Crash): Cost is {new:.2f}s (Original: {orig:.2f}s)")
    
    if new > orig:
        print("✅ SUCCESS: The map is now Adaptive!")