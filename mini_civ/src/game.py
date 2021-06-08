"""Game."""
import pygame
import os
import gettext
from src.game_state import Game_state
from src.visual.vis_cursor import vis_cursor
from src.visual.vis_map import generate_map
from src.visual.vis_button import vis_button
from src.visual.vis_frame import vis_frame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

gettext.install('game', os.path.join(os.path.dirname
                (os.path.abspath(__file__)), '../res/po'))


class Game:
    """Represents game process."""

    def __init__(self, width, height, fps):
        """Initialize common game context.

        The game context consists of:
        1) game_folder == folder with game resources
        2) clock
        3) fps == fps for clock
        4) screen == main screen to where everything blits
        5) game_state == specific game context
        6) reset_map, end_turn, both scores, turn and exit buttons
        7) turn == the number of turns already taken

        Args:
            - width - screen width
            - height - screen height
            - fps - game fps

        """
        # For now objects' placing assumes 800x650 screen
        # TODO: support custom screen
        self.game_folder = os.path.normpath(os.path.join(os.path.dirname(
                                            os.path.abspath(__file__)), '..'))
        self.fps = fps
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0),
                                (0, 0, 0, 0, 0, 0, 0, 0))
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(_("MiniCiv"))
        self.clock = pygame.time.Clock()

        all_sprites = pygame.sprite.LayeredUpdates()

        cursor_img = pygame.image.load(os.path.join(self.game_folder,
                                       'mini_civ', 'res', 'cursor1_rs2.png')).convert()

        cursor = vis_cursor(cursor_img)

        all_sprites.add(cursor)

        self.game_state = Game_state()
        self.game_state.set_gamemap(generate_map(self.game_state, 20, 7,
                                    self.game_folder))
        self.colors = {'red': BLUE, 'blue': RED}

        button_img = pygame.image.load(os.path.join(self.game_folder,
                                       'mini_civ', 'res', 'frame_button1.png')).convert()
        self.reset_map_button = vis_button(740, 50, _('Reset map'),
                                           button_img)
        self.reset_map_button.action = self.reset_map
        all_sprites.add(self.reset_map_button)

        button_img = pygame.image.load(os.path.join(self.game_folder,
                                       'mini_civ', 'res', 'frame_button1.png')).convert()
        self.end_turn_button = vis_button(740, 180, _('End turn'), button_img)
        self.end_turn_button.action = self.end_turn
        all_sprites.add(self.end_turn_button)

        button_img = pygame.image.load(os.path.join(self.game_folder,
                                       'mini_civ', 'res', 'frame_button1.png')).convert()
        self.red_score_button = vis_button(740, 245, _('Red: ') + '100',
                                           button_img)
        self.red_score_button.action = self.do_nothing
        all_sprites.add(self.red_score_button)

        button_img = pygame.image.load(os.path.join(self.game_folder,
                                       'mini_civ', 'res', 'frame_button1.png')).convert()
        self.blue_score_button = vis_button(740, 310, _('Blue: ') + '100',
                                            button_img)
        self.blue_score_button.action = self.do_nothing
        all_sprites.add(self.blue_score_button)

        button_img = pygame.image.load(os.path.join(self.game_folder,
                                       'mini_civ', 'res', 'frame_button1.png')).convert()
        self.turn_button = vis_button(740, 375, _('Red turn'),
                                      button_img, RED)
        self.turn_button.action = self.do_nothing
        all_sprites.add(self.turn_button)

        frame_img = pygame.image.load(os.path.join(self.game_folder,
                                      'mini_civ', 'res', 'frame_global5.png')).convert()
        self.global_frame = vis_frame(360, 325, frame_img,
                                      self.game_state.get_gamemap())
        all_sprites.add(self.global_frame)

        self.running = True

        button_img = pygame.image.load(os.path.join(self.game_folder,
                                       'mini_civ', 'res', 'frame_button1.png')).convert()
        self.exit_button = vis_button(740, 115, _('Exit'), button_img)
        self.exit_button.action = self.exit
        all_sprites.add(self.exit_button)

        for line in self.game_state.get_gamemap().get_cells():
            for cell in line:
                all_sprites.add(cell.vis_cell)
                if cell.vis_cell.unit is not None:
                    all_sprites.add(cell.vis_cell.unit)

        self.game_state.set_sprites(all_sprites)
        self.turn = 0

    def end_turn(self, master):
        """End current turn and start the next one.

        Args:
            - master - current game

        """
        print(master)
        master.game_state.end_turn()
        red_resources = master.game_state.get_countries()["red"]\
            .get_resources()
        master.red_score_button.set_text(_("Red: ") + f"{red_resources}")
        blue_resources = master.game_state.get_countries()["blue"]\
            .get_resources()
        master.blue_score_button.set_text(_("Blue: ") + f"{blue_resources}")
        if master.turn % 2 == 0:
            master.turn_button.set_text(_("Blue turn"), BLUE)
        else:
            master.turn_button.set_text(_("Red turn"), RED)
        master.turn = master.turn + 1

    def exit(self, master):
        """Stop the game.

        Args:
            - master - current game

        """
        self.running = False

    def reset_map(self, master):
        """Start the game from the beginning.

        Args:
            - master - current game

        """
        master.game_state.set_gamemap(generate_map(master.game_state, 20, 7,
                                      master.game_folder))
        master.global_frame.map = master.game_state.get_gamemap()
        all_sprites = master.game_state.get_sprites()
        all_sprites.remove_sprites_of_layer(1)
        all_sprites.remove_sprites_of_layer(2)
        for line in master.game_state.get_gamemap().get_cells():
            for cell in line:
                all_sprites.add(cell.vis_cell)
                if cell.vis_cell.unit is not None:
                    all_sprites.add(cell.vis_cell.unit)
        master.turn = 0
        master.turn_button.set_text(_("Red turn"), RED)
        master.red_score_button.set_text(_("Red: ") + "100")
        master.blue_score_button.set_text(_("Blue: ") + "100")
        # return frame to its original state after possible win
        all_sprites.remove_sprites_of_layer(3)
        frame_img = pygame.image.load(os.path.join(self.game_folder,
                                      'mini_civ', 'res', 'frame_global5.png')).convert()
        self.global_frame = vis_frame(360, 325, frame_img,
                                      self.game_state.get_gamemap())
        all_sprites.add(self.global_frame)
        master.game_state.set_sprites(all_sprites)

    def do_nothing(self, master):
        """Don't do anything.

        Args:
            - master - current game

        """
        pass

    def mainloop(self):
        """Implement the process of the game.

        Ticks clock, for every tick checks events that take place.
        For every sprite calls its handler of the actual event.
        Redraw screen and continue iterations.

        """
        while self.running:
            self.clock.tick(self.fps)
            all_sprites = self.game_state.get_sprites()
            for sprite in all_sprites:
                sprite.check()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if event.button == 1:
                        for sprite in all_sprites:
                            sprite.check_click(event.pos, self)
                    elif event.button == 3:
                        for sprite in all_sprites:
                            sprite.check_right_click(event.pos, self)
                elif event.type == pygame.MOUSEMOTION:
                    for sprite in all_sprites:
                        sprite.check_motion(event.rel, self)
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = event.pos
                    if event.button == 3:
                        for sprite in all_sprites:
                            sprite.check_right_release(event.pos, self)
            # If one side has been defeated show the message about that
            # above map
            countries = self.game_state.get_countries()
            if len(countries['blue'].get_buildings()) == 0 or\
                    countries['blue'].get_resources() < 0:
                self.global_frame.set_text(_("Blue is\ndefeated!"),
                                           self.colors['blue'])
            if len(countries['red'].get_buildings()) == 0 or\
                    countries['red'].get_resources() < 0:
                self.global_frame.set_text(_("Red is\ndefeated!"),
                                           self.colors['red'])

            self.game_state.get_sprites().update()

            self.screen.fill(BLACK)
            self.game_state.get_sprites().draw(self.screen)
            pygame.display.flip()

    def quit(self):
        """Completely kill the game."""
        pygame.quit()
