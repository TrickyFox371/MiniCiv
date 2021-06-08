"""Visual object."""
import pygame as pg

BLACK = (0, 0, 0)


class vis_object(pg.sprite.Sprite):
    """Represent object, that has sprite."""

    def __init__(self, x, y, img):
        """Initialise visual object.

        Args:
            - x - object's x coordinate
            - y - object's y coordinate
            - img - object's image

        """
        pg.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey(BLACK)
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def local_coords(self, point):
        """Get local coordinates of point.

        Args:
            - point - tuple of two integers

        Returns:
            - output - local coordinates of point

        """
        return point[0] - self.rect.left, point[1] - self.rect.top

    def check_click(self, mouse, master=None):
        """React on left mouse button click.

        Args:
            - mouse - mouse click info
            - master - current game

        """
        pass

    def check_right_click(self, mouse, master=None):
        """React on right mouse button click.

        Args:
            - mouse - mouse click info
            - master - current game

        """
        pass

    def check_right_release(self, mouse, master=None):
        """React on right mouse button release.

        Args:
            - mouse - mouse click info
            - master - current game

        """
        pass

    def check_motion(self, rel, master=None):
        """React on mouse motion.

        Args:
            - rel - mouse click info
            - master - current game

        """
        pass

    def check(self, master=None):
        """React every main loop iteration.

        Args:
            - master - current game

        """
        pass

    def update_image(self, img):
        """Update object's image.

        Args:
            - img - new image

        """
        self.image = img
        self.image.set_colorkey(BLACK)
        self.mask = pg.mask.from_surface(self.image)

    def get_image(self):
        """Get object's image.

        Returns:
            - object - object's image

        """
        return self.image
