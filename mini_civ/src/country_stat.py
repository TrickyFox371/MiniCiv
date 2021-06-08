"""Country statistics."""
import random
from src.units.creatures.spearman import Spearman
from src.units.buildings.town_hall import Town_hall


class Country_stat:
    """Represent statistics of country."""

    def __init__(self, color, name):
        """Initialise country_stat.

        Args:
            - color - county's color
            - name - country's name

        """
        self.color = color
        self.name = name
        self.resources = 100
        self.capital = (-1, -1)
        self.buildings = []
        self.units = []
        self.cells = []

    def set_capital(self, capital_coords, vis_map):
        """Set coordinates of country's capital.

        Args:
            - capital_coords - coordinates of capital
            - vis_map - game map

        """
        assert(vis_map.in_bounds(capital_coords[0], capital_coords[1]))
        self.capital = capital_coords
        town_hall = Town_hall()
        town_hall.set_cell(self.capital)
        town_hall.set_country(self.name)
        self.add_building(town_hall)

    def get_capital(self):
        """Return coordinates of country's capital.

        Returns:
            - output - capital coordinates

        """
        return self.capital

    def gen_unit_loc(self, units_num, spawn_area_size, vis_map):
        """Generate initial unit locations in the hex map.

        Major assumptions:
        1) Every unit belongs to the country
        2) All units spawn in the square over the country capital
        3) If the spawn location is unavailable, they spawn in the capital
        4) The townhall building is always located in the capital
        This function requires:
        1) The nation must have the capital

        Args:
            - units_num - number of generated units
            - spawn_area_size - size of area near capital, where
              units can spawn (in work)
            - vis_map - game map

        """
        neighbours = vis_map.neighbours(self.capital[0], self.capital[1])
        possible_spawns = set()
        for cell in neighbours:
            possible_spawns.add((cell.X(), cell.Y()))
        for unit_idx in range(units_num):
            if len(possible_spawns) == 0:
                spawn_loc = self.capital
            else:
                spawn_loc = random.sample(possible_spawns, 1)[0]
                possible_spawns.remove(spawn_loc)
                if not vis_map.in_bounds(spawn_loc[0], spawn_loc[1]):
                    spawn_loc = self.capital

            unit = Spearman()
            unit.set_cell((spawn_loc[0], spawn_loc[1]))
            unit.set_country(self.name)
            self.add_unit(unit)

    def add_unit(self, unit):
        """Add unit to country.

        Args:
             - unit - unit, that will be added

        """
        self.units.append(unit)

    def remove_unit(self, unit):
        """Remove unit from country.

        Args:
             - unit - unit, that will be removed

        """
        self.units.remove(unit)

    def get_units(self):
        """Return all country's units.

        Return:
            - output - all country's units

        """
        return self.units

    def clear_units(self):
        """Delete all country's units."""
        self.units = []

    def add_cell(self, cell):
        """Add cell to country.

        Args:
            - cell - cell, that will be added

        """
        self.cells.append(cell)

    def add_building(self, building):
        """Add building to country.

        Args:
            - building - building, that will be added

        """
        self.buildings.append(building)

    def remove_building(self, building):
        """Remove building from country.

        Args:
            - building - building, that will be removed

        """
        self.buildings.remove(building)

    def get_buildings(self):
        """Return all country's buildings.

        Returns:
            - output - all country's buildings

        """
        return self.buildings

    def clear_buildings(self):
        """Delete all country's buildings."""
        self.buildings = []

    def remove_cell(self, cell):
        """Remove cell from country.

        Args:
            - cell - cell, that will be removed

        """
        self.units.remove(cell)

    def get_cells(self):
        """Return all country's cells.

        Returns:
            - output - all country's cells

        """
        return self.cells

    def clear_cells(self):
        """Delete all country's cells."""
        self.cells = []

    def get_color(self):
        """Return country's color.

        Returns:
            - output - country's color

        """
        return self.color

    def get_resources(self):
        """Return country's resources.

        Returns:
            - output - country's resources

        """
        return self.resources

    def set_resources(self, resources):
        """Set country's resources.

        Args:
            - resources - country's resources

        """
        self.resources = resources

    def change_resources(self, add):
        """Change country's resources.

        Args:
            - add - value, that will be added to country's resources

        """
        self.resources = self.resources + add

    def get_income(self):
        """Get country's income.

        Returns:
            - output - country's income

        """
        income = 0
        for unit in self.units:
            income = income + unit.get_income()
        for building in self.buildings:
            income = income + building.get_income()
        return income

    def end_turn(self):
        """End current turn."""
        for unit in self.units:
            unit.end_turn()
        for building in self.buildings:
            building.end_turn()
        self.change_resources(self.get_income())
