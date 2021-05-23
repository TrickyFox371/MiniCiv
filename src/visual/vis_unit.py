from src.visual.vis_object import vis_object

BLACK = (0, 0, 0)


class vis_unit(vis_object):
    def __init__(self, unit_img):
        vis_object.__init__(self, 0, 0, unit_img)
        self.move = False
        self.immovable = False
        self._layer = 2

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

    def get_unit(self):
        return self.unit
