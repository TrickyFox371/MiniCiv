"""Building."""
from src.unit import Unit


class Building(Unit):
    """Represent buildings."""

    def __init__(self):
        """Initialise building."""
        super().__init__()
        self.speed = 0
