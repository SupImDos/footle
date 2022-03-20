"""Provides Server for Footle"""


# Third-Party
import pywebio

# Local
from footle import controllers
from footle import settings
from . import utils


class Server:
    """Server Class"""

    @classmethod
    def start(cls) -> None:
        """Starts the Footle Server"""
        # Create Server and Run
        pywebio.start_server(
            applications=cls.run,
            host=settings.SETTINGS.HOST,
            port=settings.SETTINGS.PORT,
        )

    @classmethod
    @pywebio.config(
        title="Footle",
        description="Wordle for AFL Players",
        theme="sketchy",
        css_style=r".footer {display: none;}",  # Hide Footer
    )
    def run(cls) -> None:
        """Runs the Footle Server for a Session"""
        # Game
        game = controllers.Game()

        # Header
        pywebio.output.put_markdown(
            """
            # Footle
            Wordle for AFL Players
            """
        ).style("text-align:center;")

        # Loop
        while game.turn < settings.SETTINGS.GAME_MAX_ATTEMPTS:
            # Draw Input
            name = pywebio.input.input(
                datalist=controllers.Game.NAMES,
                type=pywebio.input.TEXT,
                autocomplete="off",
                placeholder=f"Guess {game.turn + 1} of {settings.SETTINGS.GAME_MAX_ATTEMPTS}",
                required=True,
            )

            # Guess
            player = game.guess(name)

            # Check
            if not player:
                # Draw and Continue
                pywebio.output.toast(
                    content=f"'{name}' is not an AFL player!",
                    color="error",
                )
                continue

            # Check
            result = game.check(player)

            # Create Row
            content = [
                utils.cell(text=player.name(), match=result.name()),
                utils.cell(text=player.team.abbreviation, match=result.team),
                utils.cell(text=player.position.pretty_name(), match=result.position),
                utils.cell(text=f"{player.height_cm}cm", match=result.height_cm),
                utils.cell(text=f"{player.weight_kg}kg", match=result.weight_kg),
                utils.cell(text=f"#{player.number}", match=result.number),
            ]

            # Draw Row
            pywebio.output.put_row(
                content=content,
                size="60fr 20fr 40fr 25fr 25fr 20fr",
            ).style("text-align: center; grid-gap: 5px;")

            # Check Win
            if player == game.answer:
                # Winner!
                pywebio.output.put_markdown(
                    f"You Win! It was **{game.answer.name()}**"
                ).style("text-align:center")
                return

        # Loser!
        pywebio.output.put_markdown(
            f"You Lose! It was **{game.answer.name()}**"
        ).style("text-align:center")
