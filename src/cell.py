import os
import pygame
from src.visual.vis_cell import vis_cell


class Cell:
    # Relative to the main folder
    TERRAIN_IMAGES = {"ice": "res/ice-hex.png",
                      "plains": "res/plains-hex.png",
                      "desert": "res/desert-hex.png",
                      "water": "res/water-hex.png"}

    def __init__(self, x, y, terrain):
        self.x = x
        self.y = y
        self.terrain = terrain
        self.vis_cell = None

    def set_terrain(self, terrain):
        self.terrain = terrain

    def get_terrain(self):
        return self.terrain

    def X(self):
        return self.x

    def Y(self):
        return self.y

    def create_vis_cell(self, vis_cell_coords, vis_map):
        ''' At start a cell always lacks terrain
        '''
        # TODO: Properly get info about the game folder
        game_folder = os.path.normpath(os.path.join
                                       (os.path.dirname
                                        (os.path.abspath(__file__)), '..'))
        cell_img = pygame.image.load(os.path.join
                                     (game_folder,
                                      'res/base-hex.png')).convert()
        self.vis_cell = vis_cell(vis_cell_coords[0], vis_cell_coords[1],
                                 cell_img, vis_map)

    def update_vis_cell(self):
        assert(self.vis_cell is not None)
        # TODO: Properly get info about the game folder
        game_folder = os.path.normpath(os.path.join
                                       (os.path.dirname
                                        (os.path.abspath(__file__)), '..'))
        if self.terrain in self.TERRAIN_IMAGES.keys():
            cell_img = pygame.image.load(os.path.join(
                game_folder,
                self.TERRAIN_IMAGES[self.terrain])).convert()
        else:
            cell_img = pygame.image.load(os.path.join(
                game_folder, 'res/base-hex.png')).convert()
        self.vis_cell.update_image(cell_img)
