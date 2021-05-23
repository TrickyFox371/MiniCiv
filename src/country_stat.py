import random
from src.unit import Unit
from src.units.buildings.town_hall import Town_hall


class Country_stat:

    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.resources = 100
        self.capital = (-1, -1)
        self.buildings = []
        self.units = []
        self.cells = []

    def set_capital(self, capital_coords, vis_map):
        assert(vis_map.in_bounds(capital_coords[0], capital_coords[1]))
        self.capital = capital_coords
        town_hall = Town_hall()
        town_hall.set_cell(self.capital)
        town_hall.set_country(self.name)
        self.add_building(town_hall)

    def get_capital(self):
        return self.capital

    def gen_unit_loc(self, units_num, spawn_area_size, vis_map):
        ''' Function generates initial unit locations in the hex map
        Major assumptions:
        1) Every unit belongs to the country
        2) All units spawn in the square over the country capital
        3) If the spawn location is unavailable, they spawn in the capital
        4) The townhall building is always located in the capital
        This function requires:
        1) The nation must have the capital
        '''
        possible_spawns = set()
        for x in range(self.capital[0] - spawn_area_size,
                       self.capital[0] + spawn_area_size):
            for y in range(self.capital[1] - spawn_area_size,
                           self.capital[1] + spawn_area_size):
                possible_spawns.add((x, y))
        possible_spawns.discard(self.capital)
        for unit_idx in range(units_num):
            if len(possible_spawns) == 0:
                spawn_loc = self.capital
            else:
                spawn_loc = random.sample(possible_spawns, 1)[0]
                possible_spawns.remove(spawn_loc)
                if not vis_map.in_bounds(spawn_loc[0], spawn_loc[1]):
                    spawn_loc = self.capital

            unit = Unit()
            unit.set_cell((spawn_loc[0], spawn_loc[1]))
            unit.set_country(self.name)
            unit.set_damage(2)
            unit.set_hp(10)
            unit.set_income(-5)
            unit.set_speed(3)
            self.add_unit(unit)

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

    def add_building(self, building):
        self.buildings.append(building)

    def remove_building(self, building):
        self.buildings.remove(building)

    def get_buildings(self):
        return self.buildings

    def clear_buildings(self):
        self.buildings = []

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
        self.resources = self.resources + add

    def get_income(self):
        income = 0
        for unit in self.units:
            income = income + unit.get_income()
        for building in self.buildings:
            income = income + building.get_income()
        return income

    def end_turn(self):
        for unit in self.units:
            unit.end_turn()
        for building in self.buildings:
            building.end_turn()
        self.change_resources(self.get_income())
