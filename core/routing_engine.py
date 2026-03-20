import os
import logging
import networkx as nx
import osmnx as ox

from config.settings import GRAPH_CACHE_PATH

logger = logging.getLogger(__name__)


class RoutingEngine:
    """
    Routing engine using a prebuilt OpenStreetMap graph
    with dynamic edge cost adaptation.
    """

    def __init__(self):
        self.graph = self._load_graph()
        self.sensor_edge = None

    # ============================================================
    # GRAPH LOADING
    # ============================================================

    def _load_graph(self):
        if not os.path.exists(GRAPH_CACHE_PATH):
            raise RuntimeError(
                "OSM graph not found. Run build_graph_osmnx.py first."
            )

        logger.info("Loading cached San Francisco OSM graph")
        G = ox.load_graphml(GRAPH_CACHE_PATH)

        # Ensure all edges have a weight attribute
        for _, _, _, data in G.edges(keys=True, data=True):
            if "weight" not in data:
                if "travel_time" in data:
                    data["weight"] = data["travel_time"]
                elif "length" in data:
                    data["weight"] = data["length"]
                else:
                    data["weight"] = 1.0

        return G

    # ============================================================
    # SENSOR BINDING
    # ============================================================

    def bind_sensor_to_location(self, latitude: float, longitude: float):
        u, v, _ = ox.nearest_edges(self.graph, longitude, latitude)
        self.sensor_edge = (u, v)
        logger.info(f"Sensor bound to edge {u} -> {v}")

    # ============================================================
    # DYNAMIC COST UPDATE
    # ============================================================

    def update_edge_cost(self, factor: float):
        """
        Legacy sensor-based congestion update.

        NOTE:
        This method is intentionally deprecated.
        It does NOT guarantee rerouting because the sensor edge
        may not lie on the candidate path.

        The adaptive system MUST use `update_route_edge_cost(...)`
        instead.

        This method is kept only for backward compatibility.
        """
        logger.warning(
            "update_edge_cost() called, but this method is deprecated. "
            "Use update_route_edge_cost(route, factor) for adaptive routing."
        )
        return
    def update_route_edge_cost(self, route, factor: float):
        """
        Apply congestion penalty to edges along the candidate route.
        Guarantees adaptive rerouting if alternatives exist.
        """
        penalty = max(1.0, factor)

        for u, v in zip(route[:-1], route[1:]):
            if self.graph.has_edge(u, v):
                for key in self.graph[u][v]:
                    data = self.graph[u][v][key]
                    if "base_weight" not in data:
                        data["base_weight"] = data["weight"]
                    data["weight"] = data["base_weight"] * penalty

    def reset_edge_costs(self):
        for _, _, _, data in self.graph.edges(keys=True, data=True):
            if "base_weight" in data:
                data["weight"] = data["base_weight"]

    # ============================================================
    # ROUTE COMPUTATION
    # ============================================================

    def compute_route(
        self,
        start_lat: float,
        start_lon: float,
        end_lat: float,
        end_lon: float
    ):
        """
        Compute shortest path using UPDATED edge weights.
        """

        start_node = ox.nearest_nodes(self.graph, start_lon, start_lat)
        end_node = ox.nearest_nodes(self.graph, end_lon, end_lat)

        try:
            logger.info("Computing shortest path using weight")
            return nx.shortest_path(
                self.graph,
                start_node,
                end_node,
                weight="weight"   # 🔥 FINAL FIX
            )

        except nx.NetworkXNoPath:
            logger.error("No path found between start and end")
            return None
