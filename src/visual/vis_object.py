import pygame as pg

BLACK = (0, 0, 0)


class vis_object(pg.sprite.Sprite):
    def __init__(self, x, y, img,):
        pg.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey(BLACK)
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def local_coords(self, point):
        return point[0] - self.rect.left, point[1] - self.rect.top

    def check_click(self, mouse, master = None):
        pass

    def check_right_click(self, mouse, master = None):
        pass

    def check_right_release(self, mouse, master = None):
        pass

    def check_motion(self, rel, master = None):
        pass
