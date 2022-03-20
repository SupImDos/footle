"""Provides Settings for Footle"""


# Third-Party
import pydantic


class Settings(pydantic.BaseSettings):
    """Settings for Footle"""
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8080

    # API Settings
    API_URL: str = "https://aflapi.afl.com.au/afl/v2"
    API_COMPETITION_ID: int = 1
    API_TIMEOUT_S: float = 10.0

    # Game Settings
    GAME_MAX_ATTEMPTS: int = 10


# Instantiate Settings
SETTINGS = Settings()
