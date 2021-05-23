import pygame
from src.visual.vis_object import vis_object

BLACK = (0, 0, 0)


class vis_cell(vis_object):
    def __init__(self, x, y, cell_img, map):
        vis_object.__init__(self, x, y, cell_img)
        self.map = map
        self._layer = 1
        self.count = 0
        self.unit = None

    def check_click(self, mouse):
        ''' Assumption in this function:
        1) The cells belongs to the map.
        2) Map stores the global state
        '''
        if self.rect.collidepoint(mouse) and self.mask.get_at(self.local_coords(mouse)) == 1:
            if self.unit is None:
                x, y = self.map.get_coords(self)
                for cell in self.map.neighbours(x, y):
                    if cell.vis_cell.get_unit() is not None and cell.vis_cell.get_unit().moving() is True\
                            and cell.vis_cell.get_unit().is_immovable() is False:
                        self.set_unit(cell.vis_cell.get_unit())
                        self.unit.set_move(False)
                        cell.vis_cell.set_unit(None)
                        break
            else:
                game_state = self.map.get_gamestate()
                if (self.unit.get_unit().get_country() ==
                    game_state.get_turn()):
                    self.unit.set_move(True)
            for line in self.map.get_cells():
                for cell in line:
                    if cell.vis_cell.get_unit() is not None and cell.vis_cell != self:
                        cell.vis_cell.get_unit().set_move(False)

    def x_size(self):
        return self.rect.right - self.rect.left

    def y_size(self):
        return self.rect.bottom - self.rect.top

    def move(self, move):
        self.rect.center = (self.rect.center[0] + move[0], self.rect.center[1] + move[1])
        if self.unit is not None:
            self.unit.set_center(self.rect.centerx, self.rect.centery)

    def set_unit(self, unit):
        self.unit = unit
        if self.unit is not None:
            self.unit.set_center(self.rect.centerx, self.rect.centery)

    def get_unit(self):
        return self.unit

    def update_image(self, cell_img):
        self.image = cell_img
        self.image.set_colorkey(BLACK)
        self.mask = pygame.mask.from_surface(self.image)
