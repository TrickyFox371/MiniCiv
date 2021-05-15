import pygame
import os
import sys
sys.path.append(os.path.normpath(os.path.join
                (os.path.dirname(os.path.abspath(__file__)), '..')))

from src.country_stat import Country_stat
from src.unit import Unit
from src.visual.vis_cursor import vis_cursor
from src.visual.vis_cell import vis_cell
from src.visual.vis_map import vis_map
from src.visual.vis_button import vis_button
from src.visual.vis_frame import vis_frame
from src.visual.vis_unit import vis_unit

WIDTH = 800
HEIGHT = 650
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

game_folder = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))

def exit():
    global running
    running = False

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game with basic interface")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.LayeredUpdates()

cell_img = pygame.image.load(os.path.join(game_folder, 'res/hex1-res2.png')).convert()
cursor_img = pygame.image.load(os.path.join(game_folder, 'res/cursor1_rs2.png')).convert()

gamemap = vis_map()
gamemap.set_size(30, 10, cell_img)
gamemap.gen_terrain()

cursor = vis_cursor(cursor_img)

all_sprites.add(cursor)
for line in gamemap.get_cells():
    for cell in line:
        all_sprites.add(cell.vis_cell)

red_stat = Country_stat(RED)
blue_stat = Country_stat(BLUE)
red_stat.set_capital((1, 1), gamemap)
blue_stat.set_capital((5, 5), gamemap)

red_stat.gen_unit_loc(3, 1, gamemap)
blue_stat.gen_unit_loc(3, 1, gamemap)

# Water generation phase
banned_cells = set()
banned_cells.add(red_stat.get_capital())
banned_cells.add(blue_stat.get_capital())
for unit in red_stat.get_units():
    banned_cells.add(unit.get_cell())
for unit in blue_stat.get_units():
    banned_cells.add(unit.get_cell())
gamemap.gen_water(banned_cells)

townhall_img = pygame.image.load(os.path.join
                                 (game_folder, 'res/townhall.png')).convert()
for building in red_stat.get_buildings():
    building.add_vis_unit(townhall_img)
    building_cell = building.get_cell()
    gamemap.get_cells()[building_cell[0]][building_cell[1]].\
        vis_cell.set_unit(building.vis_unit)
    building.vis_unit.set_immovable(True)
    all_sprites.add(building.vis_unit)
for building in blue_stat.get_buildings():
    building.add_vis_unit(townhall_img)
    building_cell = building.get_cell()
    gamemap.get_cells()[building_cell[0]][building_cell[1]].\
        vis_cell.set_unit(building.vis_unit)
    building.vis_unit.set_immovable(True)
    all_sprites.add(building.vis_unit)

spearman_img = pygame.image.load(os.path.join
                                 (game_folder, 'res/spearman.png')).convert()
for unit in red_stat.get_units():
    unit.add_vis_unit(spearman_img)
    unit_cell = unit.get_cell()
    gamemap.get_cells()[unit_cell[0]][unit_cell[1]].\
        vis_cell.set_unit(unit.vis_unit)
    all_sprites.add(unit.vis_unit)
for unit in blue_stat.get_units():
    unit.add_vis_unit(spearman_img)
    unit_cell = unit.get_cell()
    gamemap.get_cells()[unit_cell[0]][unit_cell[1]].\
        vis_cell.set_unit(unit.vis_unit)
    all_sprites.add(unit.vis_unit)

button_img = pygame.image.load(os.path.join(game_folder, 'res/frame_button1.png')).convert()
reset_map_button = vis_button(740, 50, 'Reset map', button_img)
all_sprites.add(reset_map_button)

button_img = pygame.image.load(os.path.join(game_folder, 'res/frame_button1.png')).convert()
end_turn_button = vis_button(740, 180, 'End turn', button_img)
all_sprites.add(end_turn_button)
button_img = pygame.image.load(os.path.join(game_folder, 'res/frame_button1.png')).convert()
red_score_button = vis_button(740, 245, 'Red Score', button_img)
all_sprites.add(red_score_button)

button_img = pygame.image.load(os.path.join(game_folder, 'res/frame_button1.png')).convert()
blue_score_button = vis_button(740, 310, 'Blue Score', button_img)
all_sprites.add(blue_score_button)

frame_img = pygame.image.load(os.path.join(game_folder, 'res/frame_global4.png')).convert()
global_frame = vis_frame(360, 325, frame_img, gamemap)
all_sprites.add(global_frame)

running = True
it = 0

button_img = pygame.image.load(os.path.join(game_folder, 'res/frame_button1.png')).convert()
exit_button = vis_button(740, 115, 'Exit', button_img)
exit_button.action = exit
all_sprites.add(exit_button)

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

    all_sprites.update()

    screen.fill(BLACK)
    #reset_map_button.draw_text()
    all_sprites.remove_sprites_of_layer(1)
    all_sprites.remove_sprites_of_layer(2)
    for line in gamemap.get_cells():
        for cell in line:
            if global_frame.rect.contains(cell.vis_cell.rect):
                all_sprites.add(cell.vis_cell)
                if cell.vis_cell.unit is not None:
                    all_sprites.add(cell.vis_cell.unit)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
