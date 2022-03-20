"""Provides Players for Footle"""


# Standard
import functools
import warnings

# Third-Party
import httpx
import pydantic

# Local
from footle import models
from footle import settings
from . import competitions
from . import teams


@functools.lru_cache()
def all_players() -> dict[str, models.Player]:
    """Retrieves a dictionary of *all* AFL Players

    Returns:
        dict[str, models.Player]: Dictionary of *all* AFL players
    """
    # Players
    players: dict[str, models.Player] = {}

    # Loop
    for team in teams.all_teams().values():
        # API call
        with httpx.Client() as client:
            response = client.get(
                url=f"{settings.SETTINGS.API_URL}/squads",
                params={
                    "teamId": team.id,
                    "compSeasonId": competitions.season_id(),
                },
                timeout=settings.SETTINGS.API_TIMEOUT_S,
            )

        # Deserialize Raw Data
        data = response.json()

        # Loop through
        for raw in data["squad"]["players"]:
            # Catch Errors
            try:
                # Create Player
                player = models.Player(
                    id=raw["player"]["id"],
                    first_name=raw["player"]["firstName"],
                    last_name=raw["player"]["surname"],
                    team=team,
                    position=raw["position"],
                    height_cm=raw["player"]["heightInCm"],
                    weight_kg=raw["player"]["weightInKg"],
                    number=raw["jumperNumber"],
                )

                # Add Player
                players[player.name()] = player

            except (KeyError, pydantic.ValidationError):
                # Warn the User
                warnings.warn(
                    f"Could not parse player: {raw}"
                )

    # Return
    return players
