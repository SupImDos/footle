"""Provides Team Model for Footle"""


# Local
from . import base


class Team(base.Base):
    """Team Model for Footle"""
    id: int  # pylint: disable=invalid-name
    name: str
    abbreviation: str
    nickname: str
