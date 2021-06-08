"""Unit."""
from src.visual.vis_unit import vis_unit


class Unit:
    """Represents unit - creature or building.

    Attack rules:
    1) No friendly fire
    2) A unit can attack once per turn
    3) A unit dies, if its hp is below zero
    4) A building doesn't attack, but can defend.

    Movement rules:
    1) A unit can traverse less or equal to their speed
    number of cells
    2) If a unit reached its limit, it can neither move,
    nor attack.

    """

    def __init__(self):
        """Initialize unit.

        1) cell - location of unit
        2) hp - maximum hit points of unit
        3) cur_hp - current hit points of unit
        4) damage - damage that unit causes to enemy
        5) income - value, that changes unit's country resources every turn
        6) speed - how much times unit can move per turn
        7) country - country, which unit belongs to
        8) vis_unit - object, that represents unit on map
        9) possible_cells - types of cells, which unit can traverse
        10) produced_units - types of units, which can be
            produces by unit (in work)
        11) attacks - number of attacks, that unit caused that turn
        12) traveled_cells - number of cells, travelled by unit that turn

        """
        self.cell = -1
        self.hp = -1
        self.cur_hp = -1
        self.damage = -1
        self.income = -1
        self.speed = 1
        self.country = ""
        self.vis_unit = None
        self.possible_cells = set()
        self.produced_units = set()
        self.attacks = 0
        self.traveled_cells = 0

    def set_cell(self, cell):
        """Set cell, on which unit is located.

        Args:
            - cell - cell, that will be set

        """
        self.cell = cell

    def get_cell(self):
        """Return cell, on which unit is located.

        Returns:
            - output - cell, on which unit is located

        """
        return self.cell

    def set_hp(self, hp):
        """Set maximum and current hit points of unit.

        Args:
            - hp - hp, that will be set

        """
        self.hp = hp
        self.cur_hp = hp

    def get_hp(self):
        """Return maximum hit points of unit.

        Returns:
            - output - unit's hp

        """
        return self.hp

    def set_cur_hp(self, cur_hp):
        """Set current hit points of unit.

        Args:
            - cur_hp - cur_hp, that will be set

        """
        self.cur_hp = cur_hp

    def get_cur_hp(self):
        """Return current hit points of unit.

        Returns:
            - output - unit's current hp

        """
        return self.cur_hp

    def set_hp_after_attack(self, game_state, attacking_unit):
        """Interface to attack unit.

        Args:
            - game_state - current game state
            - attacking_unit - unit, that causes attack

        """
        self.cur_hp -= attacking_unit.get_damage()
        if self.cur_hp <= 0:
            # Dead unit disappears from the map
            gamemap = game_state.get_gamemap()
            self.vis_unit.kill()
            unit_country = game_state.get_countries()[self.country]
            if self in unit_country.get_units():
                unit_country.get_units().remove(self)
            elif self in unit_country.get_buildings():
                unit_country.get_buildings().remove(self)
            game_state.get_sprites().remove(self.vis_unit)
            gamemap.get_cells()[self.cell[0]][self.cell[1]].\
                vis_cell.set_unit(None)
            self.vis_unit = None

    def set_damage(self, damage):
        """Set damage of unit.

        Args:
            - damage - damage, that will be caused

        """
        self.damage = damage

    def get_damage(self):
        """Return damage of unit.

        Returns:
            - output - unit's damage

        """
        return self.damage

    def set_income(self, income):
        """Set income of unit.

        Args:
            - income - income, that will be set

        """
        self.income = income

    def get_income(self):
        """Return income of unit.

        Returns:
            - output - unit's income

        """
        return self.income

    def set_speed(self, speed):
        """Set speed of unit.

        Args:
            - speed - unit's speed

        """
        self.speed = speed

    def get_speed(self):
        """Return speed of unit.

        Returns:
            - output - unit's speed

        """
        return self.speed

    def set_country(self, country):
        """Set country of unit.

        Args:
            - country - country, that will be set

        """
        self.country = country

    def get_country(self):
        """Return country of unit.

        Returns:
            - output - unit's country

        """
        return self.country

    def add_possible_cell(self, cell):
        """Add cell to possible cells.

        Args:
            - cell - possible cell, that will be added

        """
        self.possible_cells.add(cell)

    def get_possible_cells(self):
        """Return possible cells of unit.

        Returns:
            - output - unit's possible cells

        """
        return self.possible_cells

    def is_possible_cell(self, cell):
        """Check if cell is possible.

        Args:
            - cell - cell, that will be checked

        Returns:
            - output - True, if cell is possible; False otherwise

        """
        return cell in self.possible_cells

    def clear_possible_cells(self):
        """Clear possible cells of unit."""
        self.possible_cells = set()

    def add_produced_unit(self, unit):
        """Add produced unit.

        Args:
            - unit - unit, that will be added to produced units

        """
        self.produced_units.add(unit)

    def get_produced_units(self):
        """Return produced units of unit.

        Returns:
            - output - unit's produced units

        """
        return self.produced_units

    def clear_produced_units(self):
        """Clear produced units of unit."""
        self.produced_units = set()

    def add_vis_unit(self, unit_img):
        """Add sprite that represents unit.

        Args:
            - unit_img - image, that will be unit's sprite

        """
        self.vis_unit = vis_unit(unit_img)
        # WARNING: Circular reference
        # It is necessary, because Visual_unit borrows
        # information from the Unit, such as country allegiance
        self.vis_unit.add_unit(self)

    def add_attack(self):
        """Increase number of caused attacks."""
        self.attacks += 1

    def get_attacks(self):
        """Return number of caused attacks.

        Returns:
            - output - number of caused attacks

        """
        return self.attacks

    def add_traveled_cells(self):
        """Increase number of travelled cells."""
        self.traveled_cells += 1

    def get_traveled_cells(self):
        """Return travelled cells.

        Returns:
            - output - unit's travelled cells

        """
        return self.traveled_cells

    def stop(self):
        """Stop unit till the end of turn."""
        self.traveled_cells = self.speed

    def end_turn(self):
        """Start new turn."""
        self.attacks = 0
        self.traveled_cells = 0

    def get_vis_unit(self):
        """Get object that represents unit on map.

        Returns:
            - output - unit's vis_unit

        """
        return self.vis_unit
