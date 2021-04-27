from src.visual.vis_cell import vis_cell

START_COORD = 60

class vis_map:
    def __init__(self):
        self.cells = []
        self.x = 0
        self.y = 0

    def set_size(self, x, y, img):
        self.x = x
        self.y = y
        coord_x = START_COORD + 5
        coord_y = START_COORD
        for i in range(0, x):
            list = []
            for j in range(0, y):
                if i % 2 == 1 and j == y - 1:
                    continue
                cell = vis_cell(coord_x, coord_y, img)
                coord_x = coord_x + cell.x_size() * 3 // 2
                list.append(cell)
            if i % 2 == 0:
                coord_x = START_COORD * 2 // 3 + 9 + list[0].x_size()
            else:
                coord_x = START_COORD + 5
            coord_y = coord_y + list[0].y_size() // 2
            self.cells.append(list)

    def get_cells(self):
        return self.cells

    def neighbours(self, x, y):
        cells = []
        if y > 1:
            cells.append(self.cells[x][y - 2])
        if y < self.y - 2:
            cells.append(self.cells[x][y + 2])
        if x > 0 and y > 0:
            cells.append(self.cells[x - 1][y - 1])
        if x > 0 and y < self.y - 1:
            cells.append(self.cells[x - 1][y + 1])
        if x < self.x - 1 and y > 0:
            cells.append(self.cells[x + 1][y - 1])
        if x < self.x - 1 and y < self.y - 1:
            cells.append(self.cells[x + 1][y + 1])
        return cells


