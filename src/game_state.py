class Game_state:
    ''' A main game class. Stores:
    1) A game map.
    2) Countries information.
    3) Player's turn
    4) All drawn sprites
    '''
    def __init__(self):
        self.countries = {}
        self.player_order = []
        self.player_turn = ""

    def set_gamemap(self, gamemap):
        self.gamemap = gamemap

    def get_gamemap(self):
        return self.gamemap

    def add_country(self, country_name, country_stat):
        ''' Each country has a name, that identifies it.
        Also, it has other characteristics, that are
        condensed in the stat class.
        The "oldest" country has the first turn.
        '''
        self.countries[country_name] = country_stat
        self.player_order.append(country_name)

    def get_countries(self):
        return self.countries

    def clear_factions(self):
        self.countries = {}
        self.player_order = []
        self.player_turn = ""

    def set_turn(self, player_turn):
        self.player_turn = player_turn

    def get_turn(self):
        return self.player_turn

    def end_turn(self):
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
        self.sprites = sprites

    def get_sprites(self):
        return self.sprites
