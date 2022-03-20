"""Provides Game for Footle"""


# Standard
import random

# Local
from footle import data
from footle import models
from . import utils

# Typing
from typing import Optional  # pylint: disable=wrong-import-order


class Game:
    """Game Class"""

    # Players
    NAMES = sorted(data.all_players())
    PLAYERS = data.all_players()

    def __init__(self) -> None:
        """Initialises the Game"""
        # Generate Answer
        self.answer = random.choice(list(data.all_players().values()))
        self.turn = 0

    def guess(self, name: str) -> Optional[models.Player]:
        """_summary_

        Args:
            name (str): _description_

        Returns:
            Optional[models.Player]: _description_
        """
        # Get Player
        player = Game.PLAYERS.get(name)

        # Return
        return player

    def check(self, player: models.Player) -> models.Comparison:
        """_summary_

        Args:
            player (models.Player): _description_

        Returns:
            models.Comparison: _description_
        """
        # Increment Turn
        self.turn += 1

        # Guess
        return utils.compare(player, self.answer)
