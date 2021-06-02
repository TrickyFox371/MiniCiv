import pygame
import os
import sys
sys.path.append(os.path.normpath(os.path.join
                (os.path.dirname(os.path.abspath(__file__)), '..')))

from src.game_state import Game_state
from src.visual.vis_cursor import vis_cursor
from src.visual.vis_map import generate_map
from src.visual.vis_button import vis_button
from src.visual.vis_frame import vis_frame

WIDTH = 800
HEIGHT = 650
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

game_folder = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(
    __file__)), '..'))


def end_turn():
    global game_state
    global red_score_button
    global blue_score_button
    global turn_button
    global turn
    game_state.end_turn()
    red_resources = game_state.get_countries()["red"].get_resources()
    red_score_button.set_text(f"Red: {red_resources}")
    blue_resources = game_state.get_countries()["blue"].get_resources()
    blue_score_button.set_text(f"Blue: {blue_resources}")
    if turn % 2 == 0:
        turn_button.set_text("Blue turn")
    else:
        turn_button.set_text("Red turn")
    turn = turn + 1


def exit():
    global running
    running = False


def reset_map():
    global game_state
    global game_folder
    game_state.set_gamemap(generate_map(game_state, 20, 7, game_folder))
    global global_frame
    global_frame.map = game_state.get_gamemap()
    all_sprites.remove_sprites_of_layer(1)
    all_sprites.remove_sprites_of_layer(2)
    for line in game_state.get_gamemap().get_cells():
        for cell in line:
            all_sprites.add(cell.vis_cell)
            if cell.vis_cell.unit is not None:
                all_sprites.add(cell.vis_cell.unit)
    game_state.set_sprites(all_sprites)


def do_nothing():
    pass


pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0),
                        (0, 0, 0, 0, 0, 0, 0, 0))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game with basic interface")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.LayeredUpdates()

cursor_img = pygame.image.load(os.path.join(game_folder,
                               'res/cursor1_rs2.png')).convert()

cursor = vis_cursor(cursor_img)

all_sprites.add(cursor)

game_state = Game_state()
game_state.set_gamemap(generate_map(game_state, 20, 7, game_folder))

button_img = pygame.image.load(os.path.join(game_folder,
                               'res/frame_button1.png')).convert()
reset_map_button = vis_button(740, 50, 'Reset map', button_img)
reset_map_button.action = reset_map
all_sprites.add(reset_map_button)

button_img = pygame.image.load(os.path.join(game_folder,
                               'res/frame_button1.png')).convert()
end_turn_button = vis_button(740, 180, 'End turn', button_img)
end_turn_button.action = end_turn
all_sprites.add(end_turn_button)

button_img = pygame.image.load(os.path.join(game_folder,
                               'res/frame_button1.png')).convert()
red_score_button = vis_button(740, 245, 'Red: 100', button_img)
red_score_button.action = do_nothing
all_sprites.add(red_score_button)

button_img = pygame.image.load(os.path.join(game_folder,
                               'res/frame_button1.png')).convert()
blue_score_button = vis_button(740, 310, 'Blue: 100', button_img)
blue_score_button.action = do_nothing
all_sprites.add(blue_score_button)

button_img = pygame.image.load(os.path.join(game_folder,
                               'res/frame_button1.png')).convert()
turn_button = vis_button(740, 375, 'Red turn', button_img)
turn_button.action = do_nothing
all_sprites.add(turn_button)

frame_img = pygame.image.load(os.path.join(game_folder,
                              'res/frame_global5.png')).convert()
global_frame = vis_frame(360, 325, frame_img, game_state.get_gamemap())
all_sprites.add(global_frame)

running = True
it = 0

button_img = pygame.image.load(os.path.join(game_folder,
                               'res/frame_button1.png')).convert()
exit_button = vis_button(740, 115, 'Exit', button_img)
exit_button.action = exit
all_sprites.add(exit_button)

for line in game_state.get_gamemap().get_cells():
    for cell in line:
        all_sprites.add(cell.vis_cell)
        if cell.vis_cell.unit is not None:
            all_sprites.add(cell.vis_cell.unit)

game_state.set_sprites(all_sprites)
turn = 0

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if event.button == 1:
                for sprite in all_sprites:
                    sprite.check_click(event.pos)
            elif event.button == 3:
                for sprite in all_sprites:
                    sprite.check_right_click(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            for sprite in all_sprites:
                sprite.check_motion(event.rel)
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            if event.button == 3:
                for sprite in all_sprites:
                    sprite.check_right_release(event.pos)

    game_state.get_sprites().update()

    screen.fill(BLACK)
    game_state.get_sprites().draw(screen)
    pygame.display.flip()

pygame.quit()
