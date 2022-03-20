"""Provides Match Enumeration for Footle"""


# Standard
import enum

# Third-Party
import pydantic


class Accuracy(enum.IntEnum):
    """Match Enumeration for Footle"""
    WRONG = 0
    CLOSE = 1
    RIGHT = 2


class Direction(enum.IntEnum):
    """Numeric Match Enumeration for Footle"""
    TOO_LOW = 0
    EXACT = 1
    TOO_HIGH = 2


class Match(pydantic.BaseModel):
    """Match Model for Footle"""
    accuracy: Accuracy
    direction: Direction
