"""Provides Base Model for Footle"""


# Third-Party
import pydantic


class Base(pydantic.BaseModel):
    """Base Model for Footle"""
    class Config:
        """Configuration for Base Model"""
        frozen = True  # Allows hashing and caching
        copy_on_model_validation = False  # Allows shared objects
