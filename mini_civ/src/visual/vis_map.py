"""Visual map."""
import random
import pygame
import os
from src.cell import Cell
from src.country_stat import Country_stat
from src.game_state import Game_state

START_COORD = 60
WATER_PERCENTAGE = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class vis_map:
    """Represent game map."""

    def __init__(self):
        """Initialise game map."""
        self.cells = []
        self.x = 0
        self.y = 0
        self.moving = False

    def set_size(self, x, y):
        """Set map size.

        Args:
            - x - x size
            - y - y size

        """
        assert(0 < x and 0 < y)
        self.x = x
        self.y = y
        coord_x = START_COORD + 5
        coord_y = START_COORD
        for i in range(0, x):
            list = []
            for j in range(0, y):
                if i % 2 == 1 and j == y - 1:
                    continue
                cell = Cell(i, j, "")
                cell.create_vis_cell((coord_x, coord_y), self)
                coord_x = coord_x + cell.vis_cell.x_size() * 3 // 2
                list.append(cell)
            if i % 2 == 0:
                coord_x = START_COORD * 2 // 3 + 9 + list[0].vis_cell.x_size()
            else:
                coord_x = START_COORD + 5
            coord_y = coord_y + list[0].vis_cell.y_size() // 2
            self.cells.append(list)

    def gen_terrain(self):
        """Generate map terrain."""
        for i in range(0, len(self.cells)):
            for j in range(0, len(self.cells[i])):
                if i < 2 or i > self.x - 3:
                    self.cells[i][j].set_terrain("ice")
                elif i < self.x // 2 - 2 or i > self.x - self.x // 2 + 2:
                    self.cells[i][j].set_terrain("plains")
                else:
                    self.cells[i][j].set_terrain("desert")
                self.cells[i][j].update_vis_cell()

    def gen_water(self, banned_cells):
        """Generate water cells.

        Capitals can't be under-water, as well as units.
        Water is generated randomly, 5% of the map is water.

        Args:
            - banned_cells - cells, where water can not be

        """
        possible_water_tiles = set()
        for i in range(0, len(self.cells)):
            for j in range(0, len(self.cells[i])):
                if (i, j) not in banned_cells:
                    possible_water_tiles.add((i, j))
        max_water_tiles = len(possible_water_tiles) * WATER_PERCENTAGE // 100
        for i in range(max_water_tiles):
            water_tile = random.sample(possible_water_tiles, 1)[0]
            possible_water_tiles.remove(water_tile)
            if self.cells[water_tile[0]][water_tile[1]].terrain != "ice":
                self.cells[water_tile[0]][water_tile[1]].set_terrain("water")
            self.cells[water_tile[0]][water_tile[1]].update_vis_cell()

    def get_cells(self):
        """Get map's cells.

        Returns:
            - output - map's cells

        """
        return self.cells

    def get_coords(self, cell):
        """Get cell's coordinates.

        Args:
            - cell - cell, which coordinates will be returned

        Returns:
            - output - cell's coordinates

        """
        i = 0
        for line in self.cells:
            j = 0
            for next_cell in line:
                if cell == next_cell.vis_cell:
                    return i, j
                j = j + 1
            i = i + 1
        return -1, -1

    def get_cell(self, x, y):
        """Get cell by coordinates.

        Args:
            - x - x coordinate
            - y - y coordinate

        Returns:
            - output - cell with x, y coordinates

        """
        return self.cells[x][y]

    def neighbours(self, x, y):
        """Get cell's neighbours.

        Args:
            - x - cell's x coordinate
            - y - cell's y coordinate

        Returns:
            - output - cell's neighbours

        """
        cells = []
        coords = []
        if x % 2 == 0:
            coords.append((x - 2, y))
            coords.append((x + 2, y))
            coords.append((x - 1, y - 1))
            coords.append((x - 1, y))
            coords.append((x + 1, y - 1))
            coords.append((x + 1, y))
        else:
            coords.append((x - 2, y))
            coords.append((x + 2, y))
            coords.append((x - 1, y))
            coords.append((x - 1, y + 1))
            coords.append((x + 1, y))
            coords.append((x + 1, y + 1))
        for x_i, y_i in coords:
            if 0 <= x_i < len(self.cells):
                if 0 <= y_i < len(self.cells[x_i]):
                    cells.append(self.cells[x_i][y_i])
        return cells

    def set_moving(self, moving):
        """Start map motion.

        Args:
            - moving - True to start motion, False to end

        """
        self.moving = moving

    def move(self, move):
        """Make map motion.

        Args:
            - moving - move coordinates

        """
        if self.moving is True:
            for line in self.cells:
                for cell in line:
                    cell.vis_cell.move(move)

    def in_bounds(self, cell_x, cell_y):
        """Check is cell with x, y coordinates exists.

        Args:
            - cell_x - cell's x coordinate
            - cell_y - cell's y coordinate

        Returns:
            - output - True if cell exists, False otherwise

        """
        return (0 <= cell_x < len(self.cells) and 0 <= cell_y < len(
            self.cells[cell_x]))

    def set_gamestate(self, game_state):
        """Set game state.

        Args:
            - game_state - game state

        """
        self.game_state = game_state

    def get_gamestate(self):
        """Get game state.

        Returns:
            - output - game state

        """
        return self.game_state

    def end_turn(self):
        """End turn."""
        pass


def generate_map(game_state: Game_state,
                 x: int, y: int, game_folder: str) -> vis_map:
    """Generate map.

    Currently assume that every map is generated via this function.
    Any other map generation function must save the game state.

    Args:
        - game_state - current game state
        - x - x map size
        - y - y map size
        - game_folder - game folder

    Returns:
        - output - game map

    """
    gamemap = vis_map()
    gamemap.set_size(x, y)
    gamemap.gen_terrain()
    gamemap.set_gamestate(game_state)

    red_stat = Country_stat(RED, "red")
    blue_stat = Country_stat(BLUE, "blue")

    red_capital_coords = (random.randint(1, x - 2), random.randint(1, y - 2))
    blue_capital_coords = (random.randint(1, x - 2), random.randint(1, y - 2))
    while -4 <= red_capital_coords[0] - blue_capital_coords[0] <= 4 and\
          -4 <= red_capital_coords[1] - blue_capital_coords[1] <= 4:
        blue_capital_coords = (random.randint(1, x - 1),
                               random.randint(1, y - 2))

    red_stat.set_capital(red_capital_coords, gamemap)
    blue_stat.set_capital(blue_capital_coords, gamemap)

    red_stat.gen_unit_loc(3, 1, gamemap)
    blue_stat.gen_unit_loc(3, 1, gamemap)

    game_state.add_country("red", red_stat)
    game_state.add_country("blue", blue_stat)
    game_state.set_turn("red")
# Water generation phase
    banned_cells = set()
    banned_cells.add(red_stat.get_capital())
    banned_cells.add(blue_stat.get_capital())
    for unit in red_stat.get_units():
        banned_cells.add(unit.get_cell())
    for unit in blue_stat.get_units():
        banned_cells.add(unit.get_cell())
    gamemap.gen_water(banned_cells)

    townhall_red_img = pygame.image.load(os.path.join(game_folder,
                                         'mini_civ', 'res', 'townhall_red.png')).convert()
    townhall_blue_img = pygame.image.load(os.path.join(game_folder,
                                          'mini_civ', 'res', 'townhall_blue.png')).convert()
    townhall_attacked = pygame.image.load(
        os.path.join(game_folder,
                     'mini_civ', 'res', 'townhall_attacked.png')).convert()
    for building in red_stat.get_buildings():
        building.add_vis_unit(townhall_red_img)
        building.get_vis_unit().set_attacked(townhall_attacked)
        building_cell = building.get_cell()
        gamemap.get_cells()[building_cell[0]][building_cell[1]].\
            vis_cell.set_unit(building.vis_unit)
        building.vis_unit.set_immovable(True)
    for building in blue_stat.get_buildings():
        building.add_vis_unit(townhall_blue_img)
        building.get_vis_unit().set_attacked(townhall_attacked)
        building_cell = building.get_cell()
        gamemap.get_cells()[building_cell[0]][building_cell[1]].\
            vis_cell.set_unit(building.vis_unit)
        building.vis_unit.set_immovable(True)

    spearman_red_img = pygame.image.load(os.path.join(game_folder,
                                         'mini_civ', 'res', 'spearman_red.png')).convert()
    spearman_blue_img = pygame.image.load(os.path.join(game_folder,
                                          'mini_civ', 'res', 'spearman_blue.png')).convert()
    spearman_attacked = pygame.image.load(
        os.path.join(game_folder,
                     'mini_civ', 'res', 'spearman_attacked.png')).convert()
    for unit in red_stat.get_units():
        unit.add_vis_unit(spearman_red_img)
        unit.get_vis_unit().set_attacked(spearman_attacked)
        unit_cell = unit.get_cell()
        gamemap.get_cells()[unit_cell[0]][unit_cell[1]].\
            vis_cell.set_unit(unit.vis_unit)
    for unit in blue_stat.get_units():
        unit.add_vis_unit(spearman_blue_img)
        unit.get_vis_unit().set_attacked(spearman_attacked)
        unit_cell = unit.get_cell()
        gamemap.get_cells()[unit_cell[0]][unit_cell[1]].\
            vis_cell.set_unit(unit.vis_unit)
    return gamemap
