from src.visual.vis_unit import vis_unit


class Unit:
    ''' Attack rules:
    1) No friendly fire
    2) A unit can attack once per turn
    3) A unit dies, if its hp is below zero

    Movement rules:
    1) A unit can traverse less or equal to their speed
    number of cells
    2) If a unit reached its limit, it can neither move,
    nor attack.
    '''

    def __init__(self):
        self.cell = -1
        self.hp = -1
        self.cur_hp = -1
        self.damage = -1
        self.income = -1
        self.speed = -1
        self.country = ""
        self.vis_unit = None
        self.possible_cells = set()
        self.produced_units = set()
        self.attacks = 0
        self.traveled_cells = 0

    def set_cell(self, cell):
        self.cell = cell

    def get_cell(self):
        return self.cell

    def set_hp(self, hp):
        self.hp = hp
        self.cur_hp = hp

    def get_hp(self):
        return self.hp

    def set_cur_hp(self, cur_hp):
        self.cur_hp = cur_hp

    def get_cur_hp(self):
        return self.cur_hp

    def set_hp_after_attack(self, game_state, attacking_unit):
        self.cur_hp -= attacking_unit.get_damage()
        if self.cur_hp <= 0:
            ''' Dead unit disappears from the map
            '''
            gamemap = game_state.get_gamemap()
            self.vis_unit.kill()
            unit_country = game_state.get_countries()[self.country]
            unit_country.get_units().remove(self)
            game_state.get_sprites().remove(self.vis_unit)
            gamemap.get_cells()[self.cell[0]][self.cell[1]].\
                vis_cell.set_unit(None)
            self.vis_unit = None

    def set_damage(self, damage):
        self.damage = damage

    def get_damage(self):
        return self.damage

    def set_income(self, income):
        self.income = income

    def get_income(self):
        return self.income

    def set_speed(self, speed):
        self.speed = speed

    def get_speed(self):
        return self.speed

    def set_country(self, country):
        self.country = country

    def get_country(self):
        return self.country

    def add_possible_cell(self, cell):
        self.possible_cells.add(cell)

    def get_possible_cells(self):
        return self.possible_cells

    def is_possible_cell(self, cell):
        return cell in self.possible_cells

    def clear_possible_cells(self):
        self.possible_cells = set()

    def add_produced_unit(self, unit):
        self.produced_units.add(unit)

    def get_produced_units(self):
        return self.produced_units

    def clear_produced_units(self):
        self.produced_units = set()

    def add_vis_unit(self, unit_img):
        ''' Not every unit should be drawn
        Call this function to get the unit sprite
        '''
        self.vis_unit = vis_unit(unit_img)
        # WARNING: Circular reference
        # It is necessary, because Visual_unit borrows
        # information from the Unit, such as country allegiance
        self.vis_unit.add_unit(self)

    def add_attack(self):
        self.attacks += 1

    def get_attacks(self):
        return self.attacks

    def add_traveled_cells(self):
        self.traveled_cells += 1

    def get_traveled_cells(self):
        return self.traveled_cells

    def end_turn(self):
        self.attacks = 0
        self.traveled_cells = 0
