"""Provides Utilities for Footle"""


# Third-Party
import pywebio

# Local
from footle import models
from footle import settings


# Constants
ACCURACY_TO_STYLE = {
    models.Accuracy.WRONG: pywebio.output.put_error,
    models.Accuracy.CLOSE: pywebio.output.put_warning,
    models.Accuracy.RIGHT: pywebio.output.put_success,
}
DIRECTION_TO_SYMBOL = {
    models.Direction.TOO_LOW: "↑",
    models.Direction.EXACT: "",
    models.Direction.TOO_HIGH: "↓",
}


def cell(
    text: str,
    match: models.Match,
    ) -> pywebio.output.Output:
    """_summary_

    Args:
        text (str): _description_
        match (models.Match): _description_

    Returns:
        pywebio.output.Output: _description_
    """
    # Get Style
    style = ACCURACY_TO_STYLE[match.accuracy]

    # Get Direction Symbol
    symbol = DIRECTION_TO_SYMBOL[match.direction]

    # Create and Return
    return style(
        pywebio.output.put_text(text, symbol).style("margin-bottom: 0px;")
    ).style("padding: .25rem .25rem; margin-bottom: 5px;")


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
        first_name=match_bool(target.first_name == subject.first_name),
        last_name=match_bool(target.last_name == subject.last_name),
        team=match_bool(target.team == subject.team),
        position=match_bool(target.position == subject.position),
        height_cm=match_number(target.height_cm - subject.height_cm),
        weight_kg=match_number(target.weight_kg - subject.weight_kg),
        number=match_number(target.number - subject.number),
    )

    # Return
    return comparison


def match_bool(value: bool) -> models.Match:
    """_summary_

    Args:
        value (bool): _description_

    Returns:
        models.Match: _description_
    """
    # Check
    if value:
        # Return
        return models.Match(
            accuracy=models.Accuracy.RIGHT,
            direction=models.Direction.EXACT,
        )

    # Return
    return models.Match(
        accuracy=models.Accuracy.WRONG,
        direction=models.Direction.EXACT,
    )


def match_number(value: float) -> models.Match:
    """_summary_

    Args:
        value (float): _description_

    Returns:
        models.Match: _description_
    """
    # Get Accuracy
    if value == 0:
        # Correct
        accuracy = models.Accuracy.RIGHT

    elif abs(value) <= settings.SETTINGS.GAME_GUESS_CLOSE:
        # Close
        accuracy = models.Accuracy.CLOSE

    else:
        # Incorrect
        accuracy = models.Accuracy.WRONG

    # Get Direction
    if value == 0:
        # Exact
        direction = models.Direction.EXACT

    elif value < 0:
        # Too High
        direction = models.Direction.TOO_HIGH

    else:
        # Too Low
        direction = models.Direction.TOO_LOW

    # Return
    return models.Match(
        accuracy=accuracy,
        direction=direction,
    )
