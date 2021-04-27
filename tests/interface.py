import pygame
import os

from src.visual.vis_cursor import vis_cursor
from src.visual.vis_cell import vis_cell
from src.visual.vis_map import vis_map
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

game_folder = os.path.dirname("../")

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
gamemap.set_size(20, 7, cell_img)

cursor = vis_cursor(cursor_img)

all_sprites.add(cursor)
for line in gamemap.get_cells():
    for cell in line:
        all_sprites.add(cell)

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
global_frame = vis_frame(360, 325, frame_img)
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

        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos

            for sprite in all_sprites:
                sprite.check_click(event.pos)

    all_sprites.update()

    screen.fill(BLACK)
    all_sprites.draw(screen)
    #reset_map_button.draw_text()
    pygame.display.flip()

pygame.quit()
