"""Provides Comparison Model for Footle"""


# Local
from . import base


class Comparison(base.Base):
    """Comparison Model for Footle"""
    first_name: bool
    last_name: bool
    team: bool
    position: bool
    height_cm: int
    weight_kg: int
    number: int
