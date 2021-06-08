"""Sea cell."""
from src.cell import Cell


class Sea_cell(Cell):
    """Represent sea cell."""

    def __init__(self, x, y):
        """Initialise Sea_cell (in work).

        Args:
            - x - x coordinate
            - y - y coordinate

        """
        super().__init__(x, y)
