import pygame as pg
import pygame.freetype
from src.visual.vis_object import vis_object

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class vis_button(vis_object):
    def __init__(self, x, y, text, button_img, font=None):
        vis_object.__init__(self, x, y, button_img)
        self.text = text
        self._layer = 4
        if font is None:
            font = pg.freetype.SysFont('Comic Sans MS', 16)
        self.font = font
        self.textsurface, _ = font.render(text, (1, 1, 1))
        self.image.blit(self.textsurface, (10, 25))

    def check_click(self, mouse, master = None):
        if self.rect.collidepoint(mouse) and self.mask.get_at(self.local_coords(mouse)) == 1:
            if master is not None:
                self.action(master)
            else:
                self.action()

    def action(self, master = None):
        print('NOT IMPLEMENTED YET')

    def draw_text(self):
        self.textsurface, _ = self.font.render(self.text, (0, 0, 0))
        self.image.blit(self.textsurface, (10, 25))

    def set_text(self, text):
        label, _ = self.font.render(self.text, 0, WHITE)
        self.image.blit(label, (10, 25))
        self.text = text
        self.textsurface, _ = self.font.render(self.text, (1, 1, 1))
        self.image.blit(self.textsurface, (10, 25))
