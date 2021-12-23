import pygame as pg
import random as rnd
from Fig import Fig
import copy

colors = [(255, 0, 0), (220, 255, 0), (0, 255, 50),
          (0, 0, 255), (0, 200, 255), (190, 0, 255)]


class Game:
    def __init__(self, BOARD_WIDTH, BOARD_HEIGHT, CELL_SIZE) -> None:
        self.grid = []
        self.finished_figures = []
        self.CELL_SIZE = CELL_SIZE
        self.current_color = -1

        print("Initializing Board")
        for i in range(BOARD_HEIGHT):
            grid_row = []
            for j in range(BOARD_WIDTH + 1):
                grid_row.append(Fig((75, 75, 75), 1, 3, False))
            self.grid.append(grid_row)
        for i in range(BOARD_WIDTH):
            self.finished_figures.append(
                pg.Rect((BOARD_HEIGHT)*CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for i in range(BOARD_HEIGHT):
            self.finished_figures.append(
                pg.Rect(i * CELL_SIZE, -CELL_SIZE, CELL_SIZE, CELL_SIZE))
            self.finished_figures.append(
                pg.Rect(i * CELL_SIZE, (BOARD_WIDTH)*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def set_new_color(self):
        self.current_color = rnd.choice(colors)

    def set_figure(self, x, y, fig_mat):

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

    def update_fig(self, x, y, fig_mat, dir):
        newx, newy = x, y
        outline_x, offset = self.find_outline_x(x, y, fig_mat)
        for i, row in enumerate(fig_mat):
            for j, e in enumerate(row):
                if(e == 1):
                    self.grid[x+i][y+j] = Fig((75, 75, 75), 1, 3, False)
                    self.grid[outline_x+offset-1+i][y+j] = Fig((75, 75, 75), 1, 3, False)
        print(fig_mat)
        for i, row in enumerate(fig_mat):
            for j, e in enumerate(row):
                if(e == 1):
                    if dir == "DOWN":
                        self.grid[x+i+1][y+j] = Fig(self.current_color, 0, 0, True)
                        newx = x + 1
                    elif dir == "LEFT":
                        self.grid[x+i][y+j-1] = Fig(self.current_color, 0, 0, True)
                        newy = y - 1
                    elif dir == "RIGHT":
                        newy = y + 1
                        self.grid[x+i][y+j+1] = Fig(self.current_color, 0, 0, True)

        return newx, newy

    def check_collision(self, x, y, fig_mat, dir="DOWN"):
        #print("Checking collision", dir)
        cur_fig = []
        for i, row in enumerate(fig_mat):
            for j, e in enumerate(row):
                if(e == 1):
                    cur_fig.append(pg.Rect((x+i)*self.CELL_SIZE, (y+j)*self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

        for rect in cur_fig:
            rect = rect.copy()
            if dir == "DOWN":
                rect.x += self.CELL_SIZE
            elif dir == "LEFT":
                rect.y -= self.CELL_SIZE
            elif dir == "RIGHT":
                rect.y += self.CELL_SIZE
            if rect.collidelist(self.finished_figures) != -1:
                if dir == "DOWN":
                    self.finished_figures += cur_fig
                    for i, row in enumerate(fig_mat):
                        for j, e in enumerate(row):
                            if(e == 1):
                                self.grid[x+i][y+j].placed = True
                    print(self.print_grid(16))
                return False

        return True

    def rotate(self, x, y,fig_mat):
        outline_x, offset = self.find_outline_x(x, y, fig_mat)
        print(outline_x)
        outline_fig_mat = copy.deepcopy(fig_mat)
        if offset == 1:
            outline_x -= 1
            for i, row in enumerate(fig_mat):
                outline_fig_mat[(i+1)%len(fig_mat)] = fig_mat[i]
        elif offset == 2:
            outline_x -= 2
            for i, row in enumerate(fig_mat):
                outline_fig_mat[(i+2)%len(fig_mat)] = fig_mat[i]
                
        for i, row in enumerate(outline_fig_mat):
            for j, e in enumerate(row):
                if e == 0:
                    self.grid[outline_x+offset-1+i][y+j] = Fig((75, 75, 75), 1, 3, False)   
        for i, row in enumerate(fig_mat):
            for j, e in enumerate(row):
                if e == 0:
                    self.grid[x+i][y+j] = Fig((75, 75, 75), 1, 3, False)
                else:
                    self.grid[x+i][y+j] = Fig(self.current_color, 0, 0, True)


    def draw_outlines(self, x, y, fig_mat):
        outline_x, offset = self.find_outline_x(x, y, fig_mat)
        
        for i, row in enumerate(fig_mat):
            for j, e in enumerate(row):
                if(e == 1):
                    self.grid[outline_x-1+offset+i][y+j].color = self.current_color
                    self.grid[outline_x-1+offset+i][y+j].is_outline = True
          

        
    def find_outline_x(self, x, y, fig_mat):
        #Creating figure
        offset = 0
        cur_fig = []
        for i, row in enumerate(fig_mat):
            for j, e in enumerate(row):
                cur_fig.append(pg.Rect((x+i)*self.CELL_SIZE, (y+j)*self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))
              
        if all(v == 0 for v in fig_mat[-1]):
            offset = 1
            if all(v == 0 for v in fig_mat[-2]):
                offset = 2
        
        collided = False
        figx = x
        while(not collided):
            for rect in cur_fig:
                if rect.collidelist(self.finished_figures) != -1:
                    collided = True
            
            if collided:
                return figx, offset
                
            else:
                figx += 1
                for rect in cur_fig:
                    rect.x += self.CELL_SIZE

        return -1         

    def print_grid(self, start):
        str = ''
        for i in range(start, len(self.grid)):
            for fig in self.grid[i]:
                if fig.placed:
                    str += 'X'
                elif not fig.is_fig:
                    str += 'O'
            str += '\n'
        return str