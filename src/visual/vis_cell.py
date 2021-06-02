from src.visual.vis_object import vis_object
from src.visual.vis_unit import attack_unit

BLACK = (0, 0, 0)


class vis_cell(vis_object):
    def __init__(self, x, y, cell_img, map):
        vis_object.__init__(self, x, y, cell_img)
        self.map = map
        self._layer = 1
        self.count = 0
        self.unit = None

    def check_click(self, mouse, master=None):
        ''' Assumption in this function:
        1) The cells belongs to the map.
        2) Map stores the global state
        '''
        if self.rect.collidepoint(mouse) and\
                self.mask.get_at(self.local_coords(mouse)) == 1:
            x, y = self.map.get_coords(self)
            if self.unit is None:
                for cell in self.map.neighbours(x, y):
                    allowed = True
                    unit = cell.vis_cell.get_unit()
                    if unit is None:
                        allowed = False
                    else:
                        if unit.moving() is False:
                            allowed = False
                        if unit.is_immovable() is True:
                            allowed = False
                        if not unit.get_unit().is_possible_cell(
                                self.map.get_cell(x, y).get_terrain()):
                            allowed = False
                    if allowed:
                        self.set_unit(cell.vis_cell.get_unit())
                        self.get_unit().get_unit().add_traveled_cells()
                        self.get_unit().get_unit().set_cell((x, y))
                        self.unit.set_move(False)
                        cell.vis_cell.set_unit(None)
                        break
            else:
                game_state = self.map.get_gamestate()
                allowed = True
                if self.unit.get_unit().get_country() != game_state.get_turn():
                    allowed = False
                if self.unit.is_immovable() is True:
                    allowed = False
                if allowed:
                    steps_done = self.unit.get_unit().get_traveled_cells()
                    limit = self.unit.get_unit().get_speed()
                    if steps_done < limit:
                        self.unit.set_move(True)
                    else:
                        print(f"{self.unit.get_unit().get_country()} unit "
                              "can't move")
                else:
                    # Maybe other unit is attacking this
                    for cell in self.map.neighbours(x, y):
                        allowed = True
                        unit = cell.vis_cell.get_unit()
                        if unit is None:
                            allowed = False
                        else:
                            if unit.moving() is False:
                                allowed = False
                            country = unit.get_unit().get_country()
                            if country != game_state.get_turn():
                                allowed = False
                        if allowed:
                            defending_unit = self.unit
                            attacking_unit = cell.vis_cell.get_unit()

                            if attacking_unit.get_unit().get_attacks() < 1:
                                attack_unit(game_state,
                                            attacking_unit.get_unit(),
                                            defending_unit.get_unit())
                            else:
                                print("Unit can't attack")
                            attacking_unit.set_move(False)
                            attacking_unit.get_unit().stop()
                            break

            for line in self.map.get_cells():
                for cell in line:
                    unit = cell.vis_cell.get_unit()
                    if (unit is not None and cell.vis_cell != self):
                        cell.vis_cell.get_unit().set_move(False)

    def x_size(self):
        return self.rect.right - self.rect.left

    def y_size(self):
        return self.rect.bottom - self.rect.top

    def move(self, move):
        self.rect.center = (self.rect.center[0] + move[0],
                            self.rect.center[1] + move[1])
        if self.unit is not None:
            self.unit.set_center(self.rect.centerx, self.rect.centery)

    def set_unit(self, unit):
        self.unit = unit
        if self.unit is not None:
            self.unit.set_center(self.rect.centerx, self.rect.centery)

    def get_unit(self):
        return self.unit
