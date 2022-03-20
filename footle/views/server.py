"""Provides Server for Footle"""


# Third-Party
import pywebio

# Local
from footle import controllers
from footle import settings


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
        css_style=r".footer {display: none;}",  # Remove Footer
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
        ).style("text-align:center")

        # Loop
        while game.turn < settings.SETTINGS.GAME_MAX_ATTEMPTS:
            # Draw Input
            name = pywebio.input.input(
                datalist=controllers.Game.NAMES,
                type=pywebio.input.TEXT,
                autocomplete="new-password",  # Hack to stop user autocomplete
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

            # Test
            success = pywebio.output.put_success
            close = pywebio.output.put_warning
            fail = pywebio.output.put_error
            name_func = success if (result.first_name and result.last_name) else fail
            team_func = success if result.team else fail
            pos_func = success if result.position else fail
            height_func = success if result.height_cm == 0 else close if abs(result.height_cm) <= 10 else fail
            height_sign = " ↓" if result.height_cm < 0 else " ↑" if result.height_cm > 0 else ""
            weight_func = success if result.weight_kg == 0 else close if abs(result.weight_kg) <= 10 else fail
            weight_sign = " ↓" if result.weight_kg < 0 else " ↑" if result.weight_kg > 0 else ""
            number_func = success if result.number == 0 else close if abs(result.number) <= 10 else fail
            number_sign = " ↓" if result.number < 0 else " ↑" if result.number > 0 else ""

            # Transform Result
            content = [
                name_func(player.name()),
                team_func(player.team.abbreviation),
                pos_func(player.position.pretty_name()),
                height_func(f"{player.height_cm}cm" + height_sign),
                weight_func(f"{player.weight_kg}kg" + weight_sign),
                number_func(f"{player.number}" + number_sign),
            ]

            # Draw Grid
            pywebio.output.put_row(
                content=content,
                size=r"60fr 20fr 40fr 25fr 25fr 20fr",
            ).style("text-align: center; grid-template-rows: 65px; grid-gap: 5px")

            # Check Win
            if player == game.answer:
                # Winner!
                pywebio.output.put_markdown(
                    f"You Win! It was **{game.answer.name()}**"
                ).style("text-align:center")
                return

        # Winner!
        pywebio.output.put_markdown(
            f"You Lose! It was **{game.answer.name()}**"
        ).style("text-align:center")
