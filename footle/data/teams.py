"""Provides Teams for Footle"""


# Standard
import functools

# Third-Party
import httpx

# Local
from footle import models
from footle import settings
from . import competitions


@functools.lru_cache()
def all_teams() -> dict[str, models.Team]:
    """Retrieves AFL teams from the AFL API

    Returns:
        dict[str, models.Team]: Dictionary of AFL teams
    """
    # Teams List
    teams: dict[str, models.Team] = {}

    # Retrieve Teams
    with httpx.Client() as client:
        response = client.get(
            url=f"{settings.SETTINGS.API_URL}/teams",
            params={
                "compSeasonId": competitions.season_id(),
            },
            timeout=settings.SETTINGS.API_TIMEOUT_S,
        )

    # Loop through raw data
    for raw in response.json()["teams"]:
        # Create Team
        team = models.Team(
            id=raw["id"],
            name=raw["name"],
            abbreviation=raw["abbreviation"],
            nickname=raw["nickname"],
        )

        # Append
        teams[team.abbreviation] = team

    # Return
    return teams
