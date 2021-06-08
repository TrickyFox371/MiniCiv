"""Visual button."""
import pygame as pg
import pygame.freetype
from src.visual.vis_object import vis_object

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class vis_button(vis_object):
    """Represent button."""

    def __init__(self, x, y, text, button_img, color=(1, 1, 1), font=None):
        """Initialise vis_button.

        Args:
            - x - x coordinate
            - y - y coordinate
            - text - button text
            - button_img - button image
            - color - button text color
            - font - text font

        """
        vis_object.__init__(self, x, y, button_img)
        self.text = text.split('\n')
        self._layer = 4
        if font is None:
            font = pg.freetype.SysFont('Comic Sans MS', 16)
        self.font = font
        self.linestep = font.get_sized_height()
        lines = text.count('\n')
        delta = 0 if lines == 0 else lines * self.linestep - self.linestep // 2
        self.textcoords = (10, 25 - delta)
        for i, txt in enumerate(self.text):
            self.textsurface, _ = font.render(txt, color)
            self.image.blit(self.textsurface, (self.textcoords[0],
                            self.textcoords[1] + i * self.linestep))

    def check_click(self, mouse, master=None):
        """React on left mouse button click.

        Args:
            - mouse - mouse click info
            - master - current game

        """
        if self.rect.collidepoint(mouse) and \
                self.mask.get_at(self.local_coords(mouse)) == 1:
            if master is not None:
                self.action(master)
            else:
                self.action()

    def action(self, master=None):
        """Set action on button click.

        Args:
            - master - current game

        """
        print('NOT IMPLEMENTED YET')

    def draw_text(self):
        """Draw button text."""
        self.textsurface, _ = self.font.render(self.text, (0, 0, 0))
        self.image.blit(self.textsurface, (10, 25))

    def set_text(self, text, color=(1, 1, 1)):
        """Set text to button.

        Args:
            - text - text, that will be set
            - color - text color

        """
        lines = text.count('\n')
        delta = 0 if lines == 0 else lines * self.linestep - self.linestep // 2
        self.textcoords = (10, 25 - delta)
        for i, txt in enumerate(text.split('\n')):
            label, _ = self.font.render(self.text[i], 0, WHITE)
            self.image.blit(label, (self.textcoords[0],
                            self.textcoords[1] + i * self.linestep))
            self.textsurface, _ = self.font.render(txt, color)
            self.image.blit(self.textsurface, (self.textcoords[0],
                            self.textcoords[1] + i * self.linestep))
        self.text = text.split('\n')
