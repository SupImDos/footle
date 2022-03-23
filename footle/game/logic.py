"""Provides Game for Footle"""


# Standard
import random

# Local
from footle import data
from footle import models
from footle import settings
from . import utils

# Typing
from typing import Optional  # pylint: disable=wrong-import-order


class Game:
    """Game Class"""

    # Load Caches
    PLAYERS = data.all_players()

    def __init__(self) -> None:
        """Initialises the Game"""
        # Generate Answer
        self.answer = random.choice(list(data.all_players().values()))
        self.turn = 1
        self.hints = 0
        self.hint_pool = {
            "Weight": f"{self.answer.weight_kg}kg",
            "Height": f"{self.answer.height_cm}cm",
            "Number": f"#{self.answer.number}",
            "Position": self.answer.position.pretty_name(),
            "Team": self.answer.team.abbreviation,
        }
        self.state = models.State.PLAYING

    def playing(self) -> bool:
        """Checks whether the game is still on

        Returns:
            bool: Whether the game is still going
        """
        # Check and Return
        return self.state == models.State.PLAYING

    def player(self, name: str) -> Optional[models.Player]:
        """_summary_

        Args:
            name (str): _description_

        Returns:
            Optional[models.Player]: _description_
        """
        # Return
        return data.all_players().get(name)

    def guess(self, player: models.Player) -> models.Comparison:
        """_summary_

        Args:
            player (models.Player): _description_

        Returns:
            models.Comparison: _description_
        """
        # Increment Turn
        self.turn += 1

        # Check if Won
        if player == self.answer:
            # Won!
            self.state = models.State.WON

        # Check if Lost
        if self.turn > settings.SETTINGS.GAME_MAX_ATTEMPTS:
            # Lost!
            self.state = models.State.LOST

        # Guess
        return utils.compare(player, self.answer)

    def hint(self) -> tuple[int, str, str]:
        """Generates a Hint

        Returns:
            tuple[int, str, str]: Hint number, name and value

        Raises:
            ValueError: Raised if no more hints are available
        """
        # Check for Hints
        if self.hints >= settings.SETTINGS.GAME_MAX_HINTS:
            # Raise Error
            raise ValueError("No more hints left!")

        # Increment Hints
        self.hints += 1

        # Generate Random Hint
        key = random.choice(list(self.hint_pool.keys()))
        value = self.hint_pool.pop(key)

        # Return
        return (self.hints, key, value)

    def give_up(self) -> None:
        """Gives up the game"""
        # Give Up
        self.state = models.State.LOST
