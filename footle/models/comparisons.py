"""Provides Comparison Model for Footle"""


# Local
from . import base
from . import matches


class Comparison(base.Base):
    """Comparison Model for Footle"""
    first_name: matches.Match
    last_name: matches.Match
    team: matches.Match
    position: matches.Match
    height_cm: matches.Match
    weight_kg: matches.Match
    number: matches.Match

    def name(self) -> matches.Match:
        """_summary_

        Returns:
            matches.Match: _description_
        """
        # Average Accuracy and Direction
        accuracy = (self.first_name.accuracy + self.last_name.accuracy) // 2
        direction = (self.first_name.direction + self.last_name.direction) // 2

        # Return Match Average
        return matches.Match(
            accuracy=matches.Accuracy(accuracy),
            direction=matches.Direction(direction),
        )
