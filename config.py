# --- 1. THE LOCATION ---
# We are focusing on "Norrmalm", the central business district of Stockholm.
# This area has high traffic density and is perfect for our simulation.
CITY_NAME = "Norrmalm, Stockholm, Sweden"

# --- 2. COORDINATES (Lat, Lon) ---
# Start: Near Stockholm Central Station
START_LOC = (59.3300, 18.0581) 

# End: Near Kungsträdgården (The King's Garden)
END_LOC   = (59.3307, 18.0716)

# --- 3. SENSOR MAPPING ---
# We simulate that our "Camera 1" is located on a specific road edge.
# We will use this ID later to tell the map "Traffic is High HERE".
CAMERA_ID = "CAM_01"

# --- 4. DATA PATHS ---
# This is the variable that was missing!
VIDEO_PATH = "assets/stockholm_traffic.mp4"