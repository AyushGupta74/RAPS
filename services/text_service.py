from typing import List
import random
import re

from transformers import pipeline

from core.logger import logger
from config.settings import (
    TWITTER_BEARER_TOKEN,
    USE_SIMULATED_TEXT_DATA
)




try:
    classifier = pipeline(
        "text-classification",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )
    logger.info("Text sentiment model loaded successfully")
except Exception as e:
    classifier = None
    logger.exception("Failed to load NLP model")





SIMULATED_TEXT_STREAM: List[str] = [
    "Traffic moving smoothly in downtown area",
    "Major accident reported near highway exit",
    "Heavy congestion due to construction work",
    "Roads are clear and traffic is light",
    "Multi vehicle collision causing severe delays"
]





def _clean_text(text: str) -> str:
    """
    Basic text cleaning for NLP robustness.
    """
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"#\S+", "", text)
    text = re.sub(r"@\S+", "", text)
    return text.strip()


def _fetch_text_stream() -> List[str]:
    """
    Fetches text data from live or simulated sources.

    NOTE:
    Live Twitter integration is intentionally abstracted.
    In production, this would be replaced with a streaming client.
    """
    if USE_SIMULATED_TEXT_DATA or not TWITTER_BEARER_TOKEN:
        logger.info("Using simulated text data")
        return SIMULATED_TEXT_STREAM

    logger.warning("Live text ingestion not implemented; falling back to simulation")
    return SIMULATED_TEXT_STREAM





def get_incident_factor() -> float:
    """
    Computes traffic incident severity factor based on textual signals.

    Returns:
        float: value between 0.0 and 1.0
               0.0 → no incident
               1.0 → severe incident
    """

    if classifier is None:
        logger.warning("NLP model unavailable; returning neutral factor")
        return 0.0

    texts = _fetch_text_stream()
    sample_text = random.choice(texts)
    cleaned_text = _clean_text(sample_text)

    logger.info(f"Analyzing text signal: '{cleaned_text}'")

    try:
        result = classifier(cleaned_text)[0]
        label = result["label"]
        score = result["score"]

        
        

        if label == "NEGATIVE":
            incident_factor = min(score, 1.0)
        else:
            incident_factor = 0.0

        logger.info(
            f"NLP result | Label={label}, Score={score:.2f}, "
            f"IncidentFactor={incident_factor:.2f}"
        )

        return incident_factor

    except Exception as e:
        logger.exception("Text classification failed; returning neutral factor")
        return 0.0
