"""Provides Entry Point to Footle"""


# Local
from . import views


def main() -> None:
    """Main Function"""
    # Start Server
    views.Server.start()


if __name__ == "__main__":
    main()
