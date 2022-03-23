"""Provides Competition Data for Footle"""


# Standard
import functools

# Third-Party
import httpx

# Local
from footle import settings


@functools.lru_cache()
def season_id() -> int:
    """Retrieves the current AFL Season ID

    Returns:
        int: Current AFL Season ID
    """
    # Retrieve Competition Data
    with httpx.Client() as client:
        response = client.get(
            url=f"{settings.SETTINGS.API_URL}/competitions/{settings.SETTINGS.API_COMPETITION_ID}/compseasons",
            timeout=settings.SETTINGS.API_TIMEOUT_S,
        )

    # Deserialize Raw Data
    data = response.json()

    # Return Current Competition Season ID
    return data["compSeasons"][0]["id"]
