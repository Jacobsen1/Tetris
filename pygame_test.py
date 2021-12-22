import sys
import pygame as pg
from Figures import Figures
from pygame import draw
from pygame.constants import KEYUP
from game import Game

pg.init()

BOARD_WIDTH = 12
BOARD_HEIGHT = 24
CELL_SIZE = 30
CELL = (30, 30)
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
BLUE = (0,   0, 255)


size = width, height = BOARD_WIDTH * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE
game = Game(BOARD_WIDTH, BOARD_HEIGHT, CELL_SIZE)
figures = Figures()
screen = pg.display.set_mode(size)


def check_events(event, x, y, fig_mat):
    if event.scancode == 80 and y > 0 and game.check_collision(x, y, fig_mat, "LEFT"):
        x, y = game.update_fig(x, y, fig_mat, "LEFT")
    elif event.scancode == 79 and y + len(fig_mat) < BOARD_WIDTH and game.check_collision(x, y, fig_mat, "RIGHT"):
        x, y = game.update_fig(x, y, fig_mat, "RIGHT")
    elif event.scancode == 81 and game.check_collision(x, y, fig_mat):
        x, y = game.update_fig(x, y, fig_mat, "DOWN")
    # elif event.scancode == 82:
        # figure.rotate()
    return x, y


x, y = -1, -1

done = False
fall_speed = 0.27
fall_time = 0
clock = pg.time.Clock()
while not done:
    fall_time += clock.get_rawtime()
    clock.tick()
    if fall_time/1000 > fall_speed:
        fall_time = 0
        print("test")
        x, y = game.update_fig(x, y, fig_mat, "DOWN")

    if(x == -1 and y == -1):
        x, y, fig_mat = figures.select_figure()
        game.set_figure(x, y, fig_mat)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        if event.type == pg.KEYDOWN:
            # LEFT = 80, RIGHT = 79
            # print(event.scancode)
            x, y = check_events(event, x, y, fig_mat)

    screen.fill(BLACK)
    # clock.tick(1)
    if not game.check_collision(x, y, fig_mat):
        x, y, fig_mat = figures.select_figure()
    game.draw(screen)

    pg.display.flip()


pg.quit()
