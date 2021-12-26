import pygame as pg
import random as rnd
from Fig import Fig
import copy


colors = [(255, 0, 0), (220, 255, 0), (0, 255, 50),
          (0, 0, 255), (0, 200, 255), (190, 0, 255)]


class Game:
    def __init__(self, settings) -> None:
        self.grid = []
        self.finished_figures = []
        self.color_ind = -1
        self.current_color = -1
        self.settings = settings

        for i in range(settings.BOARD_HEIGHT):
            grid_row = []
            for j in range(settings.BOARD_WIDTH + 1):
                grid_row.append(Fig((75, 75, 75), 1, 3))
            self.grid.append(grid_row)
        for i in range(settings.BOARD_WIDTH):
            self.finished_figures.append(
                pg.Rect((settings.BOARD_HEIGHT)*settings.CELL_SIZE, i * settings.CELL_SIZE, settings.CELL_SIZE, settings.CELL_SIZE))
        for i in range(settings.BOARD_HEIGHT):
            self.finished_figures.append(
                pg.Rect(i * settings.CELL_SIZE, -settings.CELL_SIZE, settings.CELL_SIZE, settings.CELL_SIZE))
            self.finished_figures.append(
                pg.Rect(i * settings.CELL_SIZE, (settings.BOARD_WIDTH)*settings.CELL_SIZE, settings.CELL_SIZE, settings.CELL_SIZE))

    def set_new_color(self):
        self.color_ind += 1
        self.current_color = colors[(self.color_ind) % len(colors)]

    def set_figure(self, x, y, fig_mat):
        for i, row in enumerate(fig_mat):
            for j, e in enumerate(row):
                if(e == 1):
                    self.grid[x+i][y+j] = Fig(self.current_color, 0, 3, is_fig=True)

    def draw(self, game_screen):

        for i, row in enumerate(self.grid):
            for j, fig in enumerate(row):
                rect = pg.Rect(j * self.settings.CELL_SIZE, i *
                               self.settings.CELL_SIZE, self.settings.CELL_SIZE, self.settings.CELL_SIZE)
                pg.draw.rect(game_screen, fig.color, rect,
                             fig.border, fig.border_rad)

    def update_fig(self, x, y, fig_mat, dir):
        newx, newy = x, y
        
        for i, row in enumerate(fig_mat):
            for j, e in enumerate(row):
                if(e == 1):
                    self.grid[x+i][y+j] = Fig((75, 75, 75), 1, 3)

        for i, row in enumerate(fig_mat):
            for j, e in enumerate(row):
                if(e == 1):
                    if dir == "DOWN":
                        self.grid[x+i+1][y+j] = Fig(self.current_color, 0, 3, is_fig=True)
                        newx = x + 1
                    elif dir == "LEFT":
                        self.grid[x+i][y+j-1] = Fig(self.current_color, 0, 3, is_fig=True)
                        newy = y - 1
                    elif dir == "RIGHT":
                        self.grid[x+i][y+j+1] = Fig(self.current_color, 0, 3, is_fig=True)
                        newy = y + 1

        return newx, newy

    def check_collision(self, x, y, fig_mat, dir="DOWN"):
        #print("Checking collision", dir)
        cur_fig = []
        for i, row in enumerate(fig_mat):
            for j, e in enumerate(row):
                if(e == 1):
                    cur_fig.append(pg.Rect((x+i)*self.settings.CELL_SIZE, (y+j)*self.settings.CELL_SIZE, self.settings.CELL_SIZE, self.settings.CELL_SIZE))

        for rect in cur_fig:
            rect = rect.copy()
            if dir == "DOWN":
                rect.x += self.settings.CELL_SIZE
            elif dir == "LEFT":
                rect.y -= self.settings.CELL_SIZE
            elif dir == "RIGHT":
                rect.y += self.settings.CELL_SIZE
            if rect.collidelist(self.finished_figures) != -1:
                if dir == "DOWN":
                    for rect in cur_fig:
                        if rect.x <= 0:
                            print("YOU LOST")
                            self.settings.GAME_STATE.CURRENT = self.settings.GAME_STATE.LOST
                    self.finished_figures += cur_fig
                    for i, row in enumerate(fig_mat):
                        for j, e in enumerate(row):
                            if(e == 1):
                                self.grid[x+i][y+j].placed = True
                    #print(self.print_grid(16))
                return False

        return True

    def rotate(self, x, y,fig_mat):

        for i, row in enumerate(fig_mat):
            for j, e in enumerate(row):
                if e == 0:
                    self.grid[x+i][y+j] = Fig((75, 75, 75), 1, 3)
                else:
                    self.grid[x+i][y+j] = Fig(self.current_color, 0, 3, is_fig=True)


    def draw_outlines(self, x, y, fig_mat):
        outline_x = self.find_outline_x(x, y, fig_mat)

        for i, row in enumerate(self.grid):
            for j, e in enumerate(row):
                fig = self.grid[i][j]
                if fig.color == self.current_color and not fig.is_fig:
                    fig.color = (75, 75, 75)

        for i, row in enumerate(fig_mat):
            for j, e in enumerate(row):
                if(e == 1):
                    self.grid[outline_x-1+i][y+j].color = self.current_color

        
    def find_outline_x(self, x, y, fig_mat):
        #Creating figure
        cur_fig = []
        for i, row in enumerate(fig_mat):
            for j, e in enumerate(row):
                if e == 1:
                    cur_fig.append(pg.Rect((x+i)*self.settings.CELL_SIZE, (y+j)*self.settings.CELL_SIZE, self.settings.CELL_SIZE, self.settings.CELL_SIZE))
              
        collided = False
        figx = x
        while(not collided):
            for rect in cur_fig:
                if rect.collidelist(self.finished_figures) != -1:
                    collided = True
            
            if collided:
                return figx
                
            else:
                figx += 1
                for rect in cur_fig:
                    rect.x += self.settings.CELL_SIZE

        return -1   

    def draw_next_fig(self, next_fig_screen, next_fig_mat):
        x, y = 1.5 * self.settings.CELL_SIZE, len(next_fig_mat) * self.settings.CELL_SIZE / 2
        for i, row in enumerate(next_fig_mat):
            for j, e in enumerate(row):
                if(e == 1):
                    rect = pg.Rect(j * self.settings.CELL_SIZE + x, i * self.settings.CELL_SIZE + y, self.settings.CELL_SIZE, self.settings.CELL_SIZE)
                    pg.draw.rect(next_fig_screen, colors[(self.color_ind + 1) % len(colors)], rect)



    def print_grid(self, start):
        str = ''
        for i in range(start, len(self.grid)):
            for fig in self.grid[i]:
                if fig.placed:
                    str += 'X'
                else:
                    str += 'O'
            str += '\n'
        return str