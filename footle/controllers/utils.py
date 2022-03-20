"""Provides Utilities for Footle"""


# Local
from footle import models


def compare(
    subject: models.Player,
    target: models.Player,
    ) -> models.Comparison:
    """Compares player with the target answer player

    Args:
        subject (models.Player): Player to compare
        target (models.Player): Player to compare

    Returns:
        models.Comparison: Comparison with the answer
    """
    # Compare Players
    comparison = models.Comparison(
        first_name=(target.first_name == subject.first_name),
        last_name=(target.last_name == subject.last_name),
        team=(target.team == subject.team),
        position=(target.position == subject.position),
        height_cm=(target.height_cm - subject.height_cm),
        weight_kg=(target.weight_kg - subject.weight_kg),
        number=(target.number - subject.number),
    )

    # Return
    return comparison
