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

    # Players
    NAMES = sorted(data.all_players())
    PLAYERS = data.all_players()

    # Game
    MAX_ATTEMPTS = settings.SETTINGS.GAME_MAX_ATTEMPTS

    def __init__(self) -> None:
        """Initialises the Game"""
        # Generate Answer
        self.answer = random.choice(list(data.all_players().values()))
        self.turn = 1
        self.hints_left = 7
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
        # Get Player
        possible_player = Game.PLAYERS.get(name)

        # Return
        return possible_player

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
        if self.turn > Game.MAX_ATTEMPTS:
            # Lost!
            self.state = models.State.LOST

        # Guess
        return utils.compare(player, self.answer)

    def hint(self) -> Optional[tuple[str, str]]:
        """Generates a Hint

        Returns:
            Optional[tuple[str, str]]: Possible hint name and value
        """
        # 7 Hints Left
        if self.hints_left == 7:
            # Weight
            hint_data = ("Weight", f"{self.answer.weight_kg}kg")

        # 6 Hints Left
        elif self.hints_left == 6:
            # Height
            hint_data = ("Height", f"{self.answer.height_cm}cm")

        # 5 Hints Left
        elif self.hints_left == 5:
            # Number
            hint_data = ("Number", f"#{self.answer.number}")

        # 4 Hints Left
        elif self.hints_left == 4:
            # Position
            hint_data = ("Position", self.answer.position.pretty_name())

        # 3 Hints Left
        elif self.hints_left == 3:
            # Team
            hint_data = ("Team", self.answer.team.abbreviation)

        # 2 Hints Left
        elif self.hints_left == 2:
            # First Name
            hint_data = ("First Name", self.answer.first_name)

        # 1 Hint Left
        elif self.hints_left == 1:
            # Last Name
            hint_data = ("Last Name", self.answer.last_name)

        else:
            hint_data = None

        # Decrement Hints Left
        self.hints_left -= 1

        # Return
        return hint_data

    def give_up(self) -> None:
        """Gives up the game"""
        # Give Up
        self.state = models.State.LOST
