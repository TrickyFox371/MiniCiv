"""Visual unit."""
import time
from src.visual.vis_object import vis_object

BLACK = (0, 0, 0)


class vis_unit(vis_object):
    """Represent unit's sprite.

    Attacking is a type of movement.
    Immovable objects can't attack, they can only defend.

    """

    def __init__(self, unit_img):
        """Initialise vis_unit.

        Args:
            - unit_img - image of unit

        """
        vis_object.__init__(self, 0, 0, unit_img)
        self.move = False
        self.immovable = False
        self._layer = 2
        self.unit = None
        self.attacked = None
        self.return_image = False

    def check(self, master=None):
        """React every main loop iteration.

        Args:
            - master - current game

        """
        if self.return_image is True:
            time.sleep(0.1)
            self.update_image(self.tmp_img)
            self.return_image = False

    def set_center(self, x, y):
        """Set coordinates of sprite's center.

        Args:
            - x - x coordinate
            - y - y coordinate

        """
        self.rect.center = (x, y)

    def set_move(self, move):
        """Activate unit.

        Args:
            - move - True to activate unit, False to deactivate

        """
        self.move = move

    def moving(self):
        """Check if unit is active.

        Returns:
            - output - True if unit is active, False otherwise

        """
        return self.move

    def is_immovable(self):
        """Check if unit is immovable.

        Returns:
            - output - True if unit is immovable, False otherwise

        """
        return self.immovable

    def set_immovable(self, immovable):
        """Make unit immovable.

        Args:
            - immovable - True to make unit immovable, False to
              make unit movable

        """
        self.immovable = immovable

    def add_unit(self, unit):
        """Add reference to the Unit class.

        Args:
            - unit - reference to the Unit class

        """
        # Warning: Circular reference
        self.unit = unit

    def set_attacked(self, img):
        """Set attacked unit's sprite.

        Args:
            - img - image, that will be set

        """
        self.attacked = img

    def get_attacked(self):
        """Get attacked unit's sprite.

        Returns:
            - output - attacked unit's sprite

        """
        return self.attacked

    def get_unit(self):
        """Get reference to the Unit class.

        Returns:
            - output - reference to the Unit class

        """
        return self.unit

    def update_attacked(self):
        """Update unit after attack."""
        if self.attacked is None:
            return
        self.tmp_img = self.image
        self.update_image(self.attacked)
        self.return_image = True


def attack_unit(game_state, attacking_unit, defending_unit):
    """Make one unit attack other.

    Args:
        - game_state - current game state
        - attacking_unit - unit, that make attack
        - defending_unit - unit, that defends

    """
    attacking_unit.add_attack()
    defending_unit.get_vis_unit().update_attacked()
    defending_unit.set_hp_after_attack(game_state,
                                       attacking_unit)
    if defending_unit.get_cur_hp() > 0:
        attacking_unit.set_hp_after_attack(game_state,
                                           defending_unit)
