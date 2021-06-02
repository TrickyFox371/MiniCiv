import time
from src.visual.vis_object import vis_object

BLACK = (0, 0, 0)


class vis_unit(vis_object):
    ''' Attacking is a type of movement.
    Immovable objects can't attack, they can only defend.
    '''
    def __init__(self, unit_img):
        vis_object.__init__(self, 0, 0, unit_img)
        self.move = False
        self.immovable = False
        self._layer = 2
        self.unit = None
        self.attacked = None
        self.return_image = False

    def check(self, master=None):
        if self.return_image is True:
            time.sleep(0.1)
            self.update_image(self.tmp_img)
            self.return_image = False

    def set_center(self, x, y):
        self.rect.center = (x, y)

    def set_move(self, move):
        self.move = move

    def moving(self):
        return self.move

    def is_immovable(self):
        return self.immovable

    def set_immovable(self, immovable):
        self.immovable = immovable

    def add_unit(self, unit):
        ''' Adds the reference to the Unit class
        '''
        # Warning: Circular reference
        self.unit = unit

    def set_attacked(self, img):
        self.attacked = img

    def get_attacked(self):
        return self.attacked

    def get_unit(self):
        return self.unit

    def update_attacked(self):
        if self.attacked is None:
            return
        self.tmp_img = self.image
        self.update_image(self.attacked)
        self.return_image = True


def attack_unit(game_state, attacking_unit, defending_unit):
    attacking_unit.add_attack()
    defending_unit.get_vis_unit().update_attacked()
    defending_unit.set_hp_after_attack(game_state,
                                       attacking_unit)
    if defending_unit.get_cur_hp() > 0:
        attacking_unit.set_hp_after_attack(game_state,
                                           defending_unit)
