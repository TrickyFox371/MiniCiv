from unit import Unit

class Creature(Unit):

    def __init__(self):
        super().__init__()
        self.moves = -1
        self.cur_moves = -1

    def set_moves(self, moves):
        self.moves = moves

    def get_moves(self):
        return self.moves

    def set_cur_moves(self, cur_moves):
        self.cur_moves = cur_moves

    def get_cur_moves(self):
        return self.cur_moves
