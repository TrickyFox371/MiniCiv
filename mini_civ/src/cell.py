"""Cell."""
import os
import pygame
from src.visual.vis_cell import vis_cell


class Cell:
    """Represents cell."""

    # Relative to the main folder
    TERRAIN_IMAGES = {"ice": os.path.join("mini_civ",
                                          "res", "ice-hex.png"),
                      "plains": os.path.join("mini_civ", "res",
                                             "plains-hex.png"),
                      "desert": os.path.join("mini_civ", "res",
                                             "desert-hex.png"),
                      "water": os.path.join("mini_civ", "res",
                                            "water-hex.png")}

    def __init__(self, x, y, terrain):
        """Initialise cell.

        Args:
            - x - x coordinate
            - y - y coordinate
            - terrain - cell's terrain

        """
        self.x = x
        self.y = y
        self.terrain = terrain
        self.vis_cell = None

    def set_terrain(self, terrain):
        """Set cell's terrain.

        Args:
            - terrain - terrain, that will be set

        """
        self.terrain = terrain

    def get_terrain(self):
        """Get cell's terrain.

        Returns:
            - output - cell's terrain

        """
        return self.terrain

    def X(self):
        """Get cell's x coordinate.

        Returns:
            - output - cell's x coordinate

        """
        return self.x

    def Y(self):
        """Get cell's y coordinate.

        Returns:
            - output - cell's y coordinate

        """
        return self.y

    def create_vis_cell(self, vis_cell_coords, vis_map):
        """Create cell's sprite.

        At start a cell always lacks terrain.

        Args:
            - vis_cell_coords - coordinates of sprite
            - vis_map - game map

        """
        # TODO: Properly get info about the game folder
        game_folder = os.path.normpath(os.path.join
                                       (os.path.dirname
                                        (os.path.abspath(__file__)), '..'))
        cell_img = pygame.image.load(os.path.join
                                     (game_folder,
                                      'mini_civ', 'res',
                                      'base-hex.png')).convert()
        self.vis_cell = vis_cell(vis_cell_coords[0], vis_cell_coords[1],
                                 cell_img, vis_map)

    def update_vis_cell(self):
        """Update cell's sprite."""
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
                game_folder, 'mini_civ', 'res', 'base-hex.png')).convert()
        self.vis_cell.update_image(cell_img)
