"""Provides Game State Enumeration for Footle"""


# Standard
import enum


class State(enum.IntEnum):
    """State Game Enumeration for Footle"""
    PLAYING = 0
    LOST = 1
    WON = 2
