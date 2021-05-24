import pygame
import os
import sys
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


class Game:
    def __init__(self, width, height, fps):
        '''
        Initialize common game context. The game context consists of:
         * game_folder == folder with game resources;
         * clock;
         * fps == fps for clock;
         * screen == main screen to where everything blits;
         * game_state == specific game context;
         * reset_map, end_turn, both scores, turn and exit buttons;
         * turn == the number of turns already taken.
        '''
        # For now objects' placing assumes 800x650 screen
        # TODO: support custom screen
        self.game_folder = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
        self.fps = fps
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("MiniCiv")
        self.clock = pygame.time.Clock()

        all_sprites = pygame.sprite.LayeredUpdates()

        cursor_img = pygame.image.load(os.path.join(self.game_folder, 'res/cursor1_rs2.png')).convert()

        cursor = vis_cursor(cursor_img)

        all_sprites.add(cursor)

        self.game_state = Game_state()
        self.game_state.set_gamemap(generate_map(self.game_state, 20, 7, self.game_folder))
        self.colors = {'red': BLUE, 'blue' : RED}

        button_img = pygame.image.load(os.path.join(self.game_folder, 'res/frame_button1.png')).convert()
        self.reset_map_button = vis_button(740, 50, 'Reset map', button_img)
        self.reset_map_button.action = self.reset_map
        all_sprites.add(self.reset_map_button)

        button_img = pygame.image.load(os.path.join(self.game_folder, 'res/frame_button1.png')).convert()
        self.end_turn_button = vis_button(740, 180, 'End turn', button_img)
        self.end_turn_button.action = self.end_turn
        all_sprites.add(self.end_turn_button)

        button_img = pygame.image.load(os.path.join(self.game_folder, 'res/frame_button1.png')).convert()
        self.red_score_button = vis_button(740, 245, 'Red: 100', button_img)
        self.red_score_button.action = self.do_nothing
        all_sprites.add(self.red_score_button)

        button_img = pygame.image.load(os.path.join(self.game_folder, 'res/frame_button1.png')).convert()
        self.blue_score_button = vis_button(740, 310, 'Blue: 100', button_img)
        self.blue_score_button.action = self.do_nothing
        all_sprites.add(self.blue_score_button)

        button_img = pygame.image.load(os.path.join(self.game_folder, 'res/frame_button1.png')).convert()
        self.turn_button = vis_button(740, 375, 'Red turn', button_img)
        self.turn_button.action = self.do_nothing
        all_sprites.add(self.turn_button)

        frame_img = pygame.image.load(os.path.join(self.game_folder, 'res/frame_global5.png')).convert()
        self.global_frame = vis_frame(360, 325, frame_img, self.game_state.get_gamemap())
        all_sprites.add(self.global_frame)

        self.running = True

        button_img = pygame.image.load(os.path.join(self.game_folder, 'res/frame_button1.png')).convert()
        self.exit_button = vis_button(740, 115, 'Exit', button_img)
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
        '''
        End current turn and start the next one.
        '''
        master.game_state.end_turn()
        red_resources = master.game_state.get_countries()["red"].get_resources()
        master.red_score_button.set_text(f"Red: {red_resources}")
        blue_resources = master.game_state.get_countries()["blue"].get_resources()
        master.blue_score_button.set_text(f"Blue: {blue_resources}")
        if master.turn % 2 == 0:
            master.turn_button.set_text("Blue turn")
        else:
            master.turn_button.set_text("Red turn")
        master.turn = master.turn + 1

    def exit(self, master):
        '''
        Stop the game.
        '''
        self.running = False

    def reset_map(self, master):
        '''
        Start the game from the beginning.
        '''
        master.game_state.set_gamemap(generate_map(master.game_state, 20, 7, master.game_folder))
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
        master.turn_button.set_text("Red turn")
        # return frame to its original state after possible win
        all_sprites.remove_sprites_of_layer(3);
        frame_img = pygame.image.load(os.path.join(self.game_folder, 'res/frame_global5.png')).convert()
        self.global_frame = vis_frame(360, 325, frame_img, self.game_state.get_gamemap())
        all_sprites.add(self.global_frame)
        master.game_state.set_sprites(all_sprites)

    def do_nothing(self, master):
        '''
        Don't do anything.
        '''
        pass

    def mainloop(self):
        '''
        The main function that implements the process of the game.
        Ticks clock, for every tick checks events that take place.
        For every sprite calls its handler of the actual event.
        Redraw screen and continue iterations.
        '''
        while self.running:
            self.clock.tick(self.fps)
            all_sprites = self.game_state.get_sprites()
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
            # If one side has been defeated show the message about that above map
            countries = self.game_state.get_countries()
            for country in countries:
                if len(countries[country].get_buildings()) == 0:
                    self.global_frame.set_text(country + ' defeated!', self.colors[country])

            self.game_state.get_sprites().update()

            self.screen.fill(BLACK)
            self.game_state.get_sprites().draw(self.screen)
            pygame.display.flip()

    def quit(self):
        '''
        Completely kill the game.
        '''
        pygame.quit()
