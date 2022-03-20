"""Provides Utilities for Footle"""


# Third-Party
import pywebio

# Local
from footle import models


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
