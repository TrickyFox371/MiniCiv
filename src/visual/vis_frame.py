from src.visual.vis_object import vis_object
import pygame.freetype

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class vis_frame(vis_object):
    def __init__(self, x, y, frame_img, game_map):
        vis_object.__init__(self, x, y, frame_img)
        self.map = game_map
        self._layer = 3

    def check_right_click(self, mouse, master = None):
        self.map.set_moving(True)

    def check_right_release(self, mouse, master = None):
        self.map.set_moving(False)

    def check_motion(self, rel, master = None):
        if not ((rel[0] > 0 and self.map.get_cells()[0][0].vis_cell.rect.center[0] > self.rect.center[0]) or
                (rel[1] > 0 and self.map.get_cells()[0][0].vis_cell.rect.center[1] > self.rect.center[1]) or

                (rel[0] > 0 and self.map.get_cells()[-1][0].vis_cell.rect.center[0] > self.rect.center[0]) or
                (rel[1] < 0 and self.map.get_cells()[-1][0].vis_cell.rect.center[1] < self.rect.center[1]) or

                (rel[0] < 0 and self.map.get_cells()[0][-1].vis_cell.rect.center[0] < self.rect.center[0]) or
                (rel[1] > 0 and self.map.get_cells()[0][-1].vis_cell.rect.center[1] > self.rect.center[1]) or

                (rel[0] < 0 and self.map.get_cells()[-1][-1].vis_cell.rect.center[0] < self.rect.center[0]) or
                (rel[1] < 0 and self.map.get_cells()[-1][-1].vis_cell.rect.center[1] < self.rect.center[1])):
            self.map.move(rel)

    def set_text(self, text, color):
        '''
        Render the text over the center of frame.
        It is used to write defeat messages.
        '''
        coords = (120, 325)
        font = pygame.freetype.SysFont('Comic Sans MS', 96)
        linestep = font.get_sized_height()
        for i, txt in enumerate(text.split('\n')):
            label, _ = font.render(txt, 0, WHITE)
            self.image.blit(label, (coords[0], coords[1] + i * linestep))
            self.textsurface, _ = font.render(txt, color)
            self.image.blit(self.textsurface, (coords[0], coords[1] + i * linestep))
