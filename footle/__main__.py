"""Provides Entry Point to Footle"""


# Local
from . import views


def main() -> None:
    """Main Function"""
    # Create and Run Server
    server = views.Server()
    server.start()


if __name__ == "__main__":
    main()
