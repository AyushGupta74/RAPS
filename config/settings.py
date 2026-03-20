import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "RAPS - Realtime Adaptive Pathfinding System"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development") 
DEBUG = ENVIRONMENT == "development"

CITY_NAME = os.getenv(
    "CITY_NAME",
    "San Francisco, California, USA"
)

GRAPH_CACHE_PATH = "data/san_francisco.graphml"


DEFAULT_SENSOR_LAT = float(
    os.getenv("DEFAULT_SENSOR_LAT", "37.7749")
)
DEFAULT_SENSOR_LON = float(
    os.getenv("DEFAULT_SENSOR_LON", "-122.4194")
)

TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

USE_SIMULATED_TEXT_DATA = os.getenv(
    "USE_SIMULATED_TEXT_DATA", "true"
).lower() == "true"

MODEL_PATH = os.getenv(
    "MODEL_PATH",
    "models/best.pt"
)

LOG_FILE = os.getenv(
    "LOG_FILE",
    "logs/app.log"
)

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)

API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "5000"))

if ENVIRONMENT == "production":
    if not os.path.exists(GRAPH_CACHE_PATH):
        raise RuntimeError(
            f"Graph cache not found at {GRAPH_CACHE_PATH}. "
            "Run the application once to generate it."
        )

DEMO_MODE = False
