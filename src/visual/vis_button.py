import pygame as pg
import pygame.freetype

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class vis_button(pg.sprite.Sprite):
    def __init__(self, x, y, text, button_img, font=None):
        pg.sprite.Sprite.__init__(self)
        self.text = text
        self.image = button_img
        self.image.set_colorkey(BLACK)
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self._layer = 3
        if font is None:
            font = pg.freetype.SysFont('Comic Sans MS', 16)
        self.font = font
        self.textsurface, _ = font.render(text, (1, 1, 1))
        self.image.blit(self.textsurface, (10, 25))

    def local_coords(self, point):
        return (point[0] - self.rect.left, point[1] - self.rect.top)

    def check_click(self, mouse):
        if self.rect.collidepoint(mouse) and self.mask.get_at(self.local_coords(mouse)) == 1:
            self.action()

    def check_right_click(self, mouse):
        pass

    def check_right_release(self, mouse):
        pass

    def check_motion(self, rel):
        pass

    def action(self):
        print ('NOT IMPLEMENTED YET')

    def draw_text(self):
        self.textsurface, _ = self.font.render(self.text, (0, 0, 0))
        self.image.blit(self.textsurface, (10, 25))
