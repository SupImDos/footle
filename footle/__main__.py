"""Provides Entry Point to Footle"""


# Local
from . import game


def main() -> None:
    """Main Function"""
    # Start Server
    game.Server.start()


if __name__ == "__main__":
    main()
