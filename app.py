import time
import streamlit as st
import folium
from streamlit_folium import st_folium

from core.orchestrator import AdaptiveOrchestrator


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RAPS – Realtime Adaptive Pathfinding",
    layout="wide"
)

st.title("🚦 Realtime Adaptive Pathfinding System (RAPS)")
st.markdown(
    "Adaptive routing using **Vision + NLP + Dynamic Graph Search** "
    "for **San Francisco urban traffic**."
)

# ============================================================
# SIDEBAR – LOCATIONS
# ============================================================

st.sidebar.header("📍 San Francisco Locations")

landmarks = {
    "Downtown SF": (37.7749, -122.4194),
    "Golden Gate Bridge": (37.8199, -122.4783),
    "Union Square": (37.7879, -122.4074),
    "Fisherman's Wharf": (37.8080, -122.4177),
    "SF Airport (SFO)": (37.6213, -122.3790),
    "Mission District": (37.7599, -122.4148),
    "Castro District": (37.7609, -122.4350),
    "Chinatown SF": (37.7941, -122.4078),
    "Financial District": (37.7946, -122.3999),
    "Oracle Park": (37.7786, -122.3893),
    "Presidio": (37.7989, -122.4662),
    "Twin Peaks": (37.7544, -122.4477),
    "Pier 39": (37.8087, -122.4098),
    "City Hall SF": (37.7793, -122.4192),
    "Salesforce Tower": (37.7897, -122.3967),
}

start_place = st.sidebar.selectbox(
    "Start Location", list(landmarks.keys()), index=0
)
end_place = st.sidebar.selectbox(
    "End Location", list(landmarks.keys()), index=2
)

start_lat, start_lon = landmarks[start_place]
end_lat, end_lon = landmarks[end_place]

refresh_rate = st.sidebar.slider(
    "🔄 Optimization Refresh Rate (seconds)",
    min_value=2,
    max_value=15,
    value=5
)

# ============================================================
# VIDEO INPUT (FIX ADDED)
# ============================================================

st.subheader("📹 Traffic Video Input")

video_file = st.file_uploader(
    "Upload real-world traffic video (.mp4)",
    type=["mp4"]
)

# ============================================================
# SESSION STATE
# ============================================================

if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = None

if "running" not in st.session_state:
    st.session_state.running = False

# ============================================================
# SYSTEM CONTROLS
# ============================================================

st.subheader("⚙️ System Control")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🚀 Initialize System"):
        with st.spinner("Initializing routing engine..."):
            st.session_state.orchestrator = AdaptiveOrchestrator()
        st.success("System initialized successfully")

with col2:
    if st.button("▶ Start Optimization"):
        if st.session_state.orchestrator is None:
            st.warning("Please initialize the system first")
        else:
            st.session_state.running = True

with col3:
    if st.button("⏹ Stop"):
        st.session_state.running = False

# ============================================================
# HELPER: NODE → LAT/LON
# ============================================================

def route_nodes_to_latlon(graph, route):
    coords = []
    for node in route:
        data = graph.nodes[node]
        if "y" in data and "x" in data:
            coords.append((data["y"], data["x"]))  # (lat, lon)
    return coords

# ============================================================
# SINGLE MAP RENDER (BASE + ROUTE)
# ============================================================

st.subheader("🗺️ Route Overview")

m = folium.Map(
    location=[start_lat, start_lon],
    zoom_start=13,
    tiles="CartoDB dark_matter"
)

# Start marker
folium.Marker(
    [start_lat, start_lon],
    popup=f"Start: {start_place}",
    icon=folium.Icon(color="green", icon="play")
).add_to(m)

# End marker
folium.Marker(
    [end_lat, end_lon],
    popup=f"End: {end_place}",
    icon=folium.Icon(color="blue", icon="stop")
).add_to(m)

# ============================================================
# ADAPTIVE ROUTE (FIX ADDED: PASS VIDEO)
# ============================================================

if st.session_state.orchestrator and st.session_state.running:

    st.info("Computing adaptive route...")

    route = st.session_state.orchestrator.compute_adaptive_route(
        start_coords=(start_lat, start_lon),
        end_coords=(end_lat, end_lon),
        video_file=video_file  # 🔥 CRITICAL FIX
    )

    if route:
        graph = st.session_state.orchestrator.routing_engine.graph
        path_coords = route_nodes_to_latlon(graph, route)

        folium.PolyLine(
            locations=path_coords,
            color="lime",
            weight=6,
            tooltip="Adaptive Route"
        ).add_to(m)

st_folium(m, width=1100, height=550)

st.caption(
    f"Optimization refresh every {refresh_rate}s (event-driven)"
)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.caption(
    "RAPS | Vision + NLP Driven Adaptive Routing | "
    "San Francisco | Streamlit + Folium Deployment"
)
