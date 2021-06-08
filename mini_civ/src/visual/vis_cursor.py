"""Visual cursor."""
import pygame
from src.visual.vis_object import vis_object

BLACK = (0, 0, 0)

WIDTH = 800
HEIGHT = 650


class vis_cursor(vis_object):
    """Represent game cursor."""

    def __init__(self, cursor_img):
        """Init game cursor.

        Args:
            - cursor_img - cursor image

        """
        vis_object.__init__(self, WIDTH / 2, HEIGHT / 2, cursor_img)
        self._layer = 5

    def update(self):
        """Update cursor location."""
        x, y = pygame.mouse.get_pos()
        self.rect.topleft = (x, y)
