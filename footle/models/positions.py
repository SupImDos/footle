"""Provides Positions Enumeration for Footle"""


# Standard
import enum


class Position(str, enum.Enum):
    """Enumeration for an AFL Position"""
    # Mids
    MIDFIELDER = "MIDFIELDER"
    MIDFIELDER_FORWARD = "MIDFIELDER_FORWARD"
    # Fowards
    KEY_FORWARD = "KEY_FORWARD"
    MEDIUM_FORWARD = "MEDIUM_FORWARD"
    # Backs
    KEY_DEFENDER = "KEY_DEFENDER"
    MEDIUM_DEFENDER = "MEDIUM_DEFENDER"
    # Rucks
    RUCK = "RUCK"

    def pretty_name(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return " ".join(x.capitalize() for x in self.split("_"))
