from typing import Tuple, Optional

from core.logger import logger
from core.routing_engine import RoutingEngine
from services.text_service import get_incident_factor
from services.vision_service import get_obstacle_factor_from_video


class AdaptiveOrchestrator:
    """
    Central decision-making unit of RAPS.

    Strategy:
    1. Compute baseline shortest route
    2. Fuse vision + NLP congestion signals
    3. Penalize edges ON the candidate route
    4. Recompute an alternative adaptive route
    """

    def __init__(self):
        logger.info("Initializing AdaptiveOrchestrator")
        self.routing_engine = RoutingEngine()
        logger.info("AdaptiveOrchestrator initialized successfully")

    def compute_adaptive_route(
        self,
        start_coords: Tuple[float, float],
        end_coords: Tuple[float, float],
        video_file=None
    ) -> Optional[list]:

        logger.info(
            f"Computing adaptive route | Start={start_coords}, End={end_coords}"
        )

        # ==================================================
        # 1. Compute BASELINE route (no penalties)
        # ==================================================

        self.routing_engine.reset_edge_costs()

        base_route = self.routing_engine.compute_route(
            start_lat=start_coords[0],
            start_lon=start_coords[1],
            end_lat=end_coords[0],
            end_lon=end_coords[1],
        )

        if not base_route:
            logger.warning("Baseline route computation failed")
            return None

        logger.info(f"Baseline route length: {len(base_route)} nodes")

        # ==================================================
        # 2. Collect congestion signals
        # ==================================================

        try:
            incident_factor = get_incident_factor()
            logger.info(f"NLP incident factor: {incident_factor:.2f}")
        except Exception:
            logger.exception("Text service failed; using neutral factor")
            incident_factor = 0.0

        try:
            obstacle_factor = (
                get_obstacle_factor_from_video(video_file)
                if video_file is not None
                else 0.0
            )
            logger.info(f"Vision obstacle factor: {obstacle_factor:.2f}")
        except Exception:
            logger.exception("Vision service failed; using neutral factor")
            obstacle_factor = 0.0

        congestion_factor = max(obstacle_factor, incident_factor)

        if congestion_factor <= 0.0:
            logger.info("No congestion detected; returning baseline route")
            return base_route

        congestion_multiplier = 1.0 + (congestion_factor * 4.0)

        logger.info(
            f"Applying adaptive congestion | "
            f"Factor={congestion_factor:.2f}, "
            f"Multiplier={congestion_multiplier:.2f}"
        )

        # ==================================================
        # 3. Penalize EDGES ON BASE ROUTE
        # ==================================================

        self.routing_engine.update_route_edge_cost(
            route=base_route,
            factor=congestion_multiplier
        )

        # ==================================================
        # 4. Recompute ADAPTIVE route
        # ==================================================

        adaptive_route = self.routing_engine.compute_route(
            start_lat=start_coords[0],
            start_lon=start_coords[1],
            end_lat=end_coords[0],
            end_lon=end_coords[1],
        )

        if adaptive_route:
            logger.info(
                f"Adaptive route computed | "
                f"BaselineNodes={len(base_route)}, "
                f"AdaptiveNodes={len(adaptive_route)}"
            )
        else:
            logger.warning("Adaptive route computation failed")

        return adaptive_route
