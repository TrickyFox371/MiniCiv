"""Game state."""


class Game_state:
    """A main game class.

    Stores:
    1) A game map
    2) Countries information
    3) Player's turn
    4) All drawn sprites

    """

    def __init__(self):
        """Initialise game_state."""
        self.countries = {}
        self.player_order = []
        self.player_turn = ""
        self.gamemap = None
        self.sprites = []

    def set_gamemap(self, gamemap):
        """Set map to game state.

        Args:
            - gamemap - map, that will be set

        """
        self.gamemap = gamemap

    def get_gamemap(self):
        """Return game map.

        Returns:
            - output - game map

        """
        return self.gamemap

    def add_country(self, country_name, country_stat):
        """Each country has a name, that identifies it.

        Also, it has other characteristics, that are
        condensed in the stat class.
        The "oldest" country has the first turn.

        Args:
            - country_name - name of the added country
            - country_stat - statistics of added country

        """
        self.countries[country_name] = country_stat
        self.player_order.append(country_name)

    def get_countries(self):
        """Return countries list.

        Returns:
            - output - list of countries

        """
        return self.countries

    def clear_factions(self):
        """Delete all countries."""
        self.countries = {}
        self.player_order = []
        self.player_turn = ""

    def set_turn(self, player_turn):
        """Set current turn.

        Args:
             - player_turn - current player

        """
        self.player_turn = player_turn

    def get_turn(self):
        """Return current turn.

        Returns:
            - current player

        """
        return self.player_turn

    def end_turn(self):
        """End current turn."""
        self.countries[self.player_turn].end_turn()
        for player_idx, country in enumerate(self.player_order):
            if country == self.player_turn:
                if player_idx == len(self.player_order) - 1:
                    self.player_turn = self.player_order[0]
                else:
                    self.player_turn = self.player_order[player_idx + 1]
                break
        self.gamemap.end_turn()

    def set_sprites(self, sprites):
        """Set list of sprites used in game.

        Args:
            - sprites - list of sprites

        """
        self.sprites = sprites

    def get_sprites(self):
        """Return list of sprites used in game.

        Returns:
            - output - list of sprites

        """
        return self.sprites
