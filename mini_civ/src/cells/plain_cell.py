"""Plain cell."""
from src.cell import Cell


class Plain_cell(Cell):
    """Represent plain cell."""

    def __init__(self, x, y):
        """Initialise Plain_cell (in work).

        Args:
            - x - x coordinate
            - y - y coordinate

        """
        super().__init__(x, y)
