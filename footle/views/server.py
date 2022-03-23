"""Provides Server for Footle"""


# Third-Party
import pywebio

# Local
from footle import controllers
from footle import models
from footle import settings
from . import utils

# Typing
from typing import Union  # pylint: disable=wrong-import-order


# Constants
ServerResponse = Union[None, tuple[str, str]]

# Configuration
pywebio.config(
    title="Footle",
    description="Wordle for AFL Players",
    theme="sketchy",
    css_style=r".footer {display: none;}",  # Hide Footer
)


class Server:
    """Footle"""

    # Input Names
    ACTION = "action"
    DATA = "data"

    # Action Names
    ACTION_GUESS = "submit"
    ACTION_GIVE_UP = "give_up"
    ACTION_HINT = "hint"
    ACTION_HOW_TO_PLAY = "how_to_play"

    # Styles
    STYLE_HEADER = "margin-bottom: 0px;"
    STYLE_CENTER = "text-align:center;"
    STYLE_GRID = "text-align: center; grid-gap: 5px;"
    STYLE_ROW_SIZE = "60fr 20fr 40fr 25fr 25fr 20fr"

    # Game
    GAME_CONTINUE = ("", "")  # Hack to continue the game
    GAME_FINISHED = None  # Hack to finish the game

    @classmethod
    def start(cls) -> None:
        """Starts the Footle Server"""
        # Create Server and Run
        pywebio.start_server(
            applications=cls,
            host=settings.SETTINGS.HOST,
            port=settings.SETTINGS.PORT,
        )

    def __init__(self) -> None:
        """Instantiates the Server"""
        # Create Game
        self.game = controllers.Game()

        # Draw Title
        self.title()

        # Run
        # This method blocks until the game is completed
        self.run()

        # Draw Result
        self.result()

    def title(self) -> None:
        """Draws the Title for the Web Page"""
        # Create Title
        pywebio.output.put_markdown(
            """
            # Footle
            Wordle for AFL Players
            """
        ).style(Server.STYLE_CENTER)

    def run(self) -> None:
        """Runs the Web Page"""
        # Draw Input Group
        pywebio.input.input_group(
            inputs=[
                pywebio.input.input(
                    name=Server.DATA,
                    datalist=self.game.NAMES,
                    type=pywebio.input.TEXT,
                    autocomplete="off",
                    placeholder=f"Guess {self.game.turn} of {self.game.MAX_ATTEMPTS}",
                    required=False,
                ),
                pywebio.input.actions(
                    name=Server.ACTION,
                    buttons=[
                        {"label": "Guess", "value": Server.ACTION_GUESS, "color": "primary"},
                        {"label": "Give Up", "value": Server.ACTION_GIVE_UP, "color": "danger"},
                        {"label": "Hint", "value": Server.ACTION_HINT, "color": "success"},
                        {"label": "How to Play", "value": Server.ACTION_HOW_TO_PLAY, "color": "info"},
                    ],
                ),
            ],
            validate=self.dispatch,
        )

    def dispatch(self, response: dict[str, str]) -> ServerResponse:
        """Handles the response

        Args:
            response (dict[str, str]): Response received from input

        Returns:
            ServerResponse: Either an error message to display, a flag to
                continue the game or a flag to end the game.
        """
        # Wrap the Handle Function
        try:
            # Parse Response
            action = response[Server.ACTION]  # pylint: disable=unsubscriptable-object
            data = response[Server.DATA]  # pylint: disable=unsubscriptable-object

            # Handle Response
            self.handle(action, data)

        except ValueError as exc:
            # Error Message
            return (Server.DATA, str(exc))

        else:
            # Check Game State
            if self.game.playing():
                # Continue Game
                return Server.GAME_CONTINUE

            # Finished
            return Server.GAME_FINISHED

    def handle(self, action: str, data: str) -> None:
        """_summary_

        Args:
            action (str): _description_
            data (str): _description_
        """
        # Guess
        if action == Server.ACTION_GUESS:
            # Perform a Guess
            self.guess(data)

        # Give Up
        if action == Server.ACTION_GIVE_UP:
            # Give Up
            self.give_up()

        # Hint
        if action == Server.ACTION_HINT:
            # Draw Hint
            self.hint()

        # How to Play
        if action == Server.ACTION_HOW_TO_PLAY:
            # Draw How to Play
            self.how_to_play()

    def guess(self, name: str) -> None:
        """Perform a guess on the name

        Args:
            name (str): Player name to guess

        Raises:
            ValueError: Raised if there is an error with the supplied name
        """
        # Sanitise Name
        name = name.strip()

        # Check for Empty Guess
        if not name:
            # Raise Error
            raise ValueError("Guess cannot be empty!")

        # Guess
        player = self.game.player(name)

        # Check for Invalid Player Name
        if not player:
            # Raise Error
            raise ValueError(f"{name} is not an AFL player!")

        # Check
        result = self.game.guess(player)

        # Create Grid
        content = [[
            utils.cell(text=player.name(), match=result.name()),
            utils.cell(text=player.team.abbreviation, match=result.team),
            utils.cell(text=player.position.pretty_name(), match=result.position),
            utils.cell(text=f"{player.height_cm}cm", match=result.height_cm),
            utils.cell(text=f"{player.weight_kg}kg", match=result.weight_kg),
            utils.cell(text=f"#{player.number}", match=result.number),
        ]]

        # Check if Row Header Needed
        if self.game.turn == 2:  # TODO -> Bad
            # Create Row Header
            header = [
                pywebio.output.put_text("Name").style(Server.STYLE_HEADER),
                pywebio.output.put_text("Team").style(Server.STYLE_HEADER),
                pywebio.output.put_text("Position").style(Server.STYLE_HEADER),
                pywebio.output.put_text("Height").style(Server.STYLE_HEADER),
                pywebio.output.put_text("Weight").style(Server.STYLE_HEADER),
                pywebio.output.put_text("Number").style(Server.STYLE_HEADER),
            ]

            # Preprend it to the Grid
            content.insert(0, header)

        # Draw Grid
        pywebio.output.put_grid(
            content=content,
            cell_widths=Server.STYLE_ROW_SIZE,
        ).style(Server.STYLE_GRID)

        # Javascript
        # Reset Form and Update Placeholder
        pywebio.session.run_js("document.forms[0].reset();")
        pywebio.session.run_js(
            "document.getElementsByClassName('form-control')[0].placeholder = placeholder",
            placeholder=f"Guess {self.game.turn} of {self.game.MAX_ATTEMPTS}",
        )

    def give_up(self) -> None:
        """Gives up the Game"""
        # Give Up
        self.game.give_up()

    def hint(self) -> None:
        """Draws a Hint for the Web Page

        Raises:
            ValueError: Raised if no more hints are available.
        """
        # Receive Hint
        # TODO -> Hint Number
        hint_data = self.game.hint()

        # Check for Hint Data
        if not hint_data:
            # Raise Error
            raise ValueError("No more hints!")

        # Create Hint
        pywebio.output.put_markdown(
            f"[Hint] {hint_data[0]}: **{hint_data[1]}**"
        ).style(Server.STYLE_CENTER)

    def how_to_play(self) -> None:
        """Draws the How to Play Popup for the Web Page"""
        # Create How to Play Popup
        pywebio.output.popup(
            title="How to Play",
            content=pywebio.output.put_markdown(
                f"""
                * You get {self.game.MAX_ATTEMPTS} guesses
                * You can guess any currently listed AFL player
                * The column colours indicate:
                  * <span style="color:green">GREEN</span>: You are correct
                  * <span style="color:orange">YELLOW</span>: You are close
                  * <span style="color:red">RED</span>: You are incorrect
                * Refresh the page for a new player
                """
            ),
        )

    def result(self) -> None:
        """Draw the Result of the Game"""
        # Won
        if self.game.state == models.State.WON:
            # Winner!
            pywebio.output.put_markdown(
                "You Win!"
            ).style(Server.STYLE_CENTER)

        # Lost
        if self.game.state == models.State.LOST:
            # Loser!
            pywebio.output.put_markdown(
                f"You Lose! It was **{self.game.answer.name()}**"
            ).style(Server.STYLE_CENTER)
