class Country_stat:

    def __init__(self, color):
        self.color = color
        self.resources = 100
        self.units = []
        self.cells = []

    def add_unit(self, unit):
        self.units.append(unit)

    def remove_unit(self, unit):
        self.units.remove(unit)

    def get_units(self):
        return self.units

    def clear_units(self):
        self.units = []

    def add_cell(self, cell):
        self.cells.append(cell)

    def remove_cell(self, cell):
        self.units.remove(cell)

    def get_cells(self):
        return self.cells

    def clear_cells(self):
        self.cells = []

    def get_color(self):
        return self.color

    def get_resources(self):
        return self.resources

    def set_resources(self, resources):
        self.resources = resources

    def change_resources(self, add):
        resources = self.resources + add

    def get_income(self):
        income = 0
        for unit in self.units:
            income = income + unit.get_income()
        return income