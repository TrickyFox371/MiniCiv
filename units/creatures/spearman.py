from units.creature import Creature

class Spearman(Creature):

    def __init__(self):
        super().__init__()
        self.hp = 10
        self.cur_hp = 10
        self.moves = 2
        self.cur_moves = 2
        self.damage = 3
        self.income = -2