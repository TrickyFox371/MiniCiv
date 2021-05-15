import random
from src.cell import Cell
from src.visual.vis_cell import vis_cell

START_COORD = 60


class vis_map:
    def __init__(self):
        self.cells = []
        self.x = 0
        self.y = 0
        self.moving = False

    def set_size(self, x, y, img):
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
        ''' Capitals can't be under-water, as well as units
        Water is generated randomly, 5% of the map is water
        '''
        WATER_PERCENTAGE = 5
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
        return self.cells

    def neighbours(self, x, y):
        cells = []
        if y > 1:
            cells.append(self.cells[x][y - 2])
        if y < self.y - 2:
            cells.append(self.cells[x][y + 2])
        if x > 0 and y > 0:
            cells.append(self.cells[x - 1][y - 1])
        if x > 0 and y < self.y - 1:
            cells.append(self.cells[x - 1][y + 1])
        if x < self.x - 1 and y > 0:
            cells.append(self.cells[x + 1][y - 1])
        if x < self.x - 1 and y < self.y - 1:
            cells.append(self.cells[x + 1][y + 1])
        return cells

    def set_moving(self, moving):
        self.moving = moving

    def move(self, move):
        if self.moving == True:
            for list in self.cells:
                for cell in list:
                    cell.vis_cell.move(move)

    def in_bounds(self, cell_x, cell_y):
        return (0 <= cell_x < len(self.cells)
                and 0 <= cell_y < len(self.cells[cell_x]))

import pygame
import os
from src.country_stat import Country_stat

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def generate_map(x: int, y: int, game_folder: str) -> vis_map:
    cell_img = pygame.image.load(os.path.join(game_folder, 'res/hex1-res2.png')).convert()

    gamemap = vis_map()
    gamemap.set_size(x, y, cell_img)
    gamemap.gen_terrain()

    red_stat = Country_stat(RED)
    blue_stat = Country_stat(BLUE)

    red_capital_coords = (random.randint(1, x - 2), random.randint(1, y - 2))
    blue_capital_coords = (random.randint(1, x - 2), random.randint(1, y - 2))
    while -2 <= red_capital_coords[0] - blue_capital_coords[0] <= 2 and -2 <= red_capital_coords[1] - blue_capital_coords[1] <= 2:
        blue_capital_coords = (random.randint(0, x - 1), random.randint(1, y - 2))
    
    red_stat.set_capital(red_capital_coords, gamemap)
    blue_stat.set_capital(blue_capital_coords, gamemap)

    red_stat.gen_unit_loc(3, 1, gamemap)
    blue_stat.gen_unit_loc(3, 1, gamemap)

# Water generation phase
    banned_cells = set()
    banned_cells.add(red_stat.get_capital())
    banned_cells.add(blue_stat.get_capital())
    for unit in red_stat.get_units():
        banned_cells.add(unit.get_cell())
    for unit in blue_stat.get_units():
        banned_cells.add(unit.get_cell())
    gamemap.gen_water(banned_cells)

    townhall_img = pygame.image.load(os.path.join
                                     (game_folder, 'res/townhall.png')).convert()
    for building in red_stat.get_buildings():
        building.add_vis_unit(townhall_img)
        building_cell = building.get_cell()
        gamemap.get_cells()[building_cell[0]][building_cell[1]].\
            vis_cell.set_unit(building.vis_unit)
        building.vis_unit.set_immovable(True)
    for building in blue_stat.get_buildings():
        building.add_vis_unit(townhall_img)
        building_cell = building.get_cell()
        gamemap.get_cells()[building_cell[0]][building_cell[1]].\
            vis_cell.set_unit(building.vis_unit)
        building.vis_unit.set_immovable(True)

    spearman_img = pygame.image.load(os.path.join
                                     (game_folder, 'res/spearman.png')).convert()
    for unit in red_stat.get_units():
        unit.add_vis_unit(spearman_img)
        unit_cell = unit.get_cell()
        gamemap.get_cells()[unit_cell[0]][unit_cell[1]].\
            vis_cell.set_unit(unit.vis_unit)
    for unit in blue_stat.get_units():
        unit.add_vis_unit(spearman_img)
        unit_cell = unit.get_cell()
        gamemap.get_cells()[unit_cell[0]][unit_cell[1]].\
            vis_cell.set_unit(unit.vis_unit)
    return gamemap

