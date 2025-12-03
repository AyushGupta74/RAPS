import streamlit as st
import folium
from streamlit_folium import st_folium
import time
import networkx as nx
import osmnx as ox

# Import our custom modules
from config import START_LOC, END_LOC, CITY_NAME
from modules.map_engine import StockholmMap
from modules.vision_sensor import TrafficEye
from modules.text_sensor import IncidentEar

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="RAPS: Stockholm AI", layout="wide")

st.title("🇸🇪 Real-time Adaptive Pathfinding System (RAPS)")
st.markdown(f"**Live Control Center:** {CITY_NAME}")

# --- 2. INITIALIZE SYSTEM (Cached for performance) ---
@st.cache_resource
def load_core_system():
    map_engine = StockholmMap()
    vision = TrafficEye()
    nlp = IncidentEar()
    return map_engine, vision, nlp

# Load the system
map_engine, vision, nlp = load_core_system()

# --- 3. SIDEBAR CONTROLS ---
st.sidebar.header("System Controls")
ai_mode = st.sidebar.checkbox("✅ Activate AI Rerouting", value=True)
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 1, 5, 2)
st.sidebar.markdown("---")
st.sidebar.info("This dashboard simulates real-time data ingestion from Traffic Cameras and Social Media feeds.")

# --- 4. MAIN DASHBOARD LAYOUT ---
col1, col2 = st.columns([1, 2])

# --- 5. THE LIVE LOOP CONTAINER ---
dashboard_container = st.empty()

# Button to start the simulation loop
if "simulation_running" not in st.session_state:
    st.session_state.simulation_running = False

if st.sidebar.button("Start/Stop Live Simulation"):
    st.session_state.simulation_running = not st.session_state.simulation_running

# --- 6. THE CENTRAL LOOP ---
while st.session_state.simulation_running:
    with dashboard_container.container():
        # A. SENSE (Get Data)
        # 1. Vision Sensor
        car_count = vision.get_vehicle_count()
        congestion_factor, traffic_status = vision.get_congestion_factor(car_count)
        
        # 2. NLP Sensor
        tweet_text, event_type, penalty = nlp.get_latest_incident()
        
        # B. THINK (Update Map)
        if ai_mode:
            # Send data to Naqshab's Map Engine
            orig_cost, new_cost = map_engine.update_edge_weights(congestion_factor, penalty)
        else:
            # If AI is off, reset to normal
            orig_cost, new_cost = map_engine.update_edge_weights(1.0, 0)
            traffic_status = "AI Disabled"
            event_type = "AI Disabled"

        # C. ACT (Calculate Route)
        route = map_engine.get_best_route(START_LOC, END_LOC)
        
        # --- VISUALIZATION SECTION ---
        
        # Left Column: The "Live Feed" Data
        with col1:
            st.subheader("📡 Sensor Feeds")
            
            # Visual Metric Cards
            st.metric(label="📸 Camera 01 (Drottninggatan)", value=f"{car_count} Cars", delta=traffic_status)
            st.metric(label="🐦 Social Feed Analysis", value=event_type, delta_color="inverse")
            st.info(f"Latest Tweet: '{tweet_text}'")
            
            st.markdown("---")
            st.subheader("🧠 Engine Stats")
            st.write(f"**Base Travel Time:** {orig_cost:.2f}s")
            if new_cost > orig_cost:
                st.error(f"**Current Cost:** {new_cost:.2f}s (PENALTY APPLIED)")
            else:
                st.success(f"**Current Cost:** {new_cost:.2f}s (Normal)")

        # Right Column: The Map
        with col2:
            # Create base map centered on Stockholm
            m = folium.Map(location=[START_LOC[0], START_LOC[1]], zoom_start=15)
            
            # 1. Plot the Route (if found)
            if route:
                # --- FIXED CODE START ---
                # We manually extract coordinates instead of using ox.plot_route_folium
                # Node attributes 'y' is Latitude, 'x' is Longitude
                route_coords = [(map_engine.G.nodes[node]['y'], map_engine.G.nodes[node]['x']) for node in route]
                
                # Set color based on AI status
                route_color = "red" if (new_cost > orig_cost and ai_mode) else "blue"
                
                # Draw the line
                folium.PolyLine(
                    route_coords, 
                    color=route_color, 
                    weight=6, 
                    opacity=0.8,
                    tooltip=f"Travel Cost: {new_cost:.1f}"
                ).add_to(m)
                # --- FIXED CODE END ---
            
            # 2. Add Marker for Start/End
            folium.Marker(START_LOC, popup="Start", icon=folium.Icon(color="green", icon="play")).add_to(m)
            folium.Marker(END_LOC, popup="End", icon=folium.Icon(color="red", icon="stop")).add_to(m)
            
            # 3. Add Marker for the "Virtual Camera"
            cam_node_id = map_engine.target_u
            cam_y = map_engine.G.nodes[cam_node_id]['y']
            cam_x = map_engine.G.nodes[cam_node_id]['x']
            
            folium.Marker(
                [cam_y, cam_x], 
                popup=f"<b>Virtual Camera 01</b><br>Traffic: {traffic_status}", 
                icon=folium.Icon(color="orange", icon="camera", prefix="fa")
            ).add_to(m)

            # Render map
            # returned_objects=[] tells the map: "Don't send any data back to Python."
            # This prevents the map from interrupting your sleep timer.
            st_folium(m, height=500, width=800, returned_objects=[])
    # Pause before next update
    time.sleep(refresh_rate)
    # Force streamlit to rerun
    st.rerun()

# If stopped
if not st.session_state.simulation_running:
    st.info("System Standby. Click 'Start Live Simulation' in the sidebar to begin.")