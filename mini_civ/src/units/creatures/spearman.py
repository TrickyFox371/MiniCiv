"""Spearman."""
from src.units.creature import Creature


class Spearman(Creature):
    """Represent spearman."""

    def __init__(self):
        """Initialise spearman."""
        super().__init__()
        self.hp = 10
        self.cur_hp = 10
        self.damage = 2
        self.income = -5
        self.speed = 3
        self.possible_cells = set(["ice", "plains", "desert"])
