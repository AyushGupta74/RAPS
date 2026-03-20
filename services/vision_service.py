print("VISION SERVICE FILE LOADED FROM:", __file__)

import os
import cv2
import tempfile
from typing import Optional

from ultralytics import YOLO

from core.logger import logger
from config.settings import MODEL_PATH


_model: Optional[YOLO] = None


def _load_model() -> Optional[YOLO]:
    global _model

    if _model is not None:
        return _model

    if not os.path.exists(MODEL_PATH):
        logger.error(f"Vision model not found at path: {MODEL_PATH}")
        return None

    try:
        logger.info(f"Loading YOLO vision model from {MODEL_PATH}")
        _model = YOLO(MODEL_PATH)   # ✅ ONLY correct loader
        logger.info("Vision model loaded successfully")
        return _model

    except Exception:
        logger.exception("Failed to load vision model")
        return None


def get_obstacle_factor_from_video(
    video_file,
    frame_skip: int = 20,
    max_frames: int = 40
) -> float:

    model = _load_model()

    if model is None:
        logger.warning("Vision model unavailable; returning neutral factor")
        return 0.0

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(video_file.read())
        video_path = tmp.name

    cap = cv2.VideoCapture(video_path)

    frame_idx = 0
    processed_frames = 0
    total_vehicles = 0

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_idx += 1
            if frame_idx % frame_skip != 0:
                continue

            results = model(frame, verbose=False)

            for r in results:
                if r.boxes is not None:
                    total_vehicles += len(r.boxes)

            processed_frames += 1
            if processed_frames >= max_frames:
                break

    finally:
        cap.release()
        os.remove(video_path)

    if processed_frames == 0:
        return 0.0

    avg_vehicles = total_vehicles / processed_frames
    obstacle_factor = min(avg_vehicles / 15.0, 1.0)

    logger.info(
        f"Vision inference completed | "
        f"Frames={processed_frames}, "
        f"AvgVehicles={avg_vehicles:.2f}, "
        f"ObstacleFactor={obstacle_factor:.2f}"
    )

    return obstacle_factor
