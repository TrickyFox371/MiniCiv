from units.building import Building
from units.creatures.spearman import Spearman

class Town_hall(Building):

    def __init__(self):
        super().__init__()
        self.hp = 20
        self.cur_hp = 20
        self.damage = 0
        self.income = 10
        self.produced_units.add(Spearman())