import pygame as pg

from Fig import Fig


class Game:
    def __init__(self, BOARD_WIDTH, BOARD_HEIGHT, CELL_SIZE) -> None:
        self.grid = []
        self.finished_figures = []
        self.CELL_SIZE = CELL_SIZE
        print("Initializing Board")
        for i in range(BOARD_HEIGHT):
            grid_row = []
            for j in range(BOARD_WIDTH + 1):
                grid_row.append(Fig((75, 75, 75), 1, 3, False))
            self.grid.append(grid_row)
        for i in range(BOARD_WIDTH):
            self.finished_figures.append(
                pg.Rect((BOARD_HEIGHT)*CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def set_figure(self, x, y, fig_mat):
        print("Setting Figure")

        for i, row in enumerate(fig_mat):
            for j, e in enumerate(row):
                if(e == 1):
                    self.grid[x+i][y+j] = Fig((255, 0, 0), 0, 0, True)

    def draw(self, screen):

        for i, row in enumerate(self.grid):
            for j, fig in enumerate(row):
                rect = pg.Rect(j * self.CELL_SIZE, i *
                               self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                pg.draw.rect(screen, fig.color, rect,
                             fig.border, fig.border_rad)

        for rect in self.finished_figures:
            pg.draw.rect(screen, (0, 255, 0), rect)

    def update_fig(self, x, y, fig_mat, dir):
        newx, newy = x, y

        for i, row in enumerate(fig_mat):
            for j, e in enumerate(row):
                if(e == 1):
                    if dir == "DOWN":
                        if not self.grid[x+i-1][y+1].is_fig:
                            self.grid[x+i][y +
                                           j] = Fig((75, 75, 75), 1, 3, False)
                    elif dir == "LEFT":
                        if not self.grid[x+i][y+j+1].is_fig:
                            self.grid[x+i][y +
                                           j] = Fig((75, 75, 75), 1, 3, False)

                    elif dir == "RIGHT":
                        if not self.grid[x+i][y+j-1].is_fig:
                            self.grid[x+i][y +
                                           j] = Fig((75, 75, 75), 1, 3, False)

        for i, row in enumerate(fig_mat):
            for j, e in enumerate(row):
                if(e == 1):
                    if dir == "DOWN":
                        self.grid[x+i+1][y+j] = Fig((255, 0, 0), 0, 0, True)
                        newx = x + 1
                    elif dir == "LEFT":
                        self.grid[x+i][y+j-1] = Fig((255, 0, 0), 0, 0, True)
                        newy = y - 1
                    elif dir == "RIGHT":
                        newy = y + 1
                        self.grid[x+i][y+j+1] = Fig((255, 0, 0), 0, 0, True)

        return newx, newy

    def check_collision(self, x, y, fig_mat, dir="DOWN"):
        #print("Checking collision", dir)
        cur_fig = []
        for i, row in enumerate(fig_mat):
            for j, e in enumerate(row):
                if(e == 1):
                    cur_fig.append(pg.Rect((x+i)*self.CELL_SIZE,
                                   (y+j)*self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

        for rect in cur_fig:
            rect = rect.copy()
            if dir == "DOWN":
                rect.x += self.CELL_SIZE
            elif dir == "LEFT":
                print("left")
                rect.y -= self.CELL_SIZE
            elif dir == "RIGHT":
                rect.y += self.CELL_SIZE
            if rect.collidelist(self.finished_figures) != -1:
                self.finished_figures += cur_fig
                # print(self.finished_figures)
                return False

        return True
