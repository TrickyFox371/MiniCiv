class Unit:

    def __init__(self):
        self.cell = -1
        self.hp = -1
        self.cur_hp = -1
        self.damage = -1
        self.income = -1
        self.possible_cells = set()
        self.produced_units = set()

    def set_cell(self, cell):
        self.cell = cell

    def get_cell(self):
        return self.cell

    def set_hp(self, hp):
        self.hp = hp

    def get_hp(self):
        return self.hp

    def set_cur_hp(self, cur_hp):
        self.cur_hp = cur_hp

    def get_cur_hp(self):
        return self.cur_hp

    def set_damage(self, damage):
        self.damage = damage

    def get_damage(self):
        return self.damage

    def set_income(self, income):
        self.income = income

    def get_income(self):
        return self.income

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