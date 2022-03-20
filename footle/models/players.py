"""Provides Player Model for Footle"""


# Local
from . import base, positions, teams


class Player(base.Base):
    """Model for an AFL Player"""
    id: int  # pylint: disable=invalid-name
    first_name: str
    last_name: str
    team: teams.Team
    position: positions.Position
    height_cm: int
    weight_kg: int
    number: int

    def name(self) -> str:
        """Generates the Full Name of the AFL Player

        Returns:
            str: The Full Name of the AFL Player
        """
        # Generate and Return
        return f"{self.first_name} {self.last_name}"
