#!/usr/bin/python3 
import pygame as pg
from Figures import Figures
from pygame.constants import KEYUP
from game import Game
import settings

settings.init()
pg.init()


main_screen = pg.display.set_mode((settings.WINDOW_SIZE))
game_screen = pg.surface.Surface(settings.GAME_SIZE)
next_fig_screen = pg.surface.Surface((settings.WINDOW_WIDTH-settings.GAME_WIDTH, settings.WINDOW_WIDTH-settings.GAME_WIDTH))

figures = Figures()
game = Game(settings)



def check_events(event, x, y, fig_mat):
    if event.scancode == 80 and game.check_collision(x, y, fig_mat, "LEFT"):
        x, y = game.update_fig(x, y, fig_mat, "LEFT")
    elif event.scancode == 79 and game.check_collision(x, y, fig_mat, "RIGHT"):
        x, y = game.update_fig(x, y, fig_mat, "RIGHT")
    elif event.scancode == 81 and game.check_collision(x, y, fig_mat):
        x, y = game.update_fig(x, y, fig_mat, "DOWN")
    elif event.scancode == 82 and game.check_collision(x, y, figures.get_next_fig_mat(), "ROTATE"):
        pg.key.set_repeat(0)
        fig_mat = figures.rotate()
        game.rotate(x, y, fig_mat)
    elif event.scancode == 41:
        settings.GAME_STATE.CURRENT = settings.GAME_STATE.QUIT
    return x, y, fig_mat

def main_draw_events(x, y, fig_mat):
    game_screen.fill((0,   0,   0))
    next_fig_screen.fill((0,   0,   0))
    game.draw(game_screen)
    game.draw_outlines(x, y, fig_mat)
    game.draw_next_fig(next_fig_screen, figures.get_next_fig())

    next_fig_screen.blit(textsurface, ((settings.WINDOW_WIDTH-settings.GAME_WIDTH)/2 - myfont.size('Some Text')[0]/2,10))

    #Adds the game_screen to the main screen
    main_screen.blit(game_screen, (0,0))
    #Adds the next_fig_screen to the main screen
    main_screen.blit(next_fig_screen, (settings.GAME_WIDTH, 0))

    pg.display.flip()
    return x, y, fig_mat

myfont = pg.font.SysFont('Roboto', 30)
textsurface = myfont.render('Next Figure', True, (255, 255, 255))

game.set_new_color()
x, y, fig_mat = figures.select_figure()
game.set_figure(x, y, fig_mat)
fall_speed = 0.6
fall_time = 0
clock = pg.time.Clock()

while settings.GAME_STATE.CURRENT != settings.GAME_STATE.QUIT:
    if(settings.GAME_STATE.CURRENT == settings.GAME_STATE.PLAYING):
        # FALL SPEED
        fall_time += clock.get_rawtime()
        clock.tick()
        if fall_time/1000 > fall_speed:
            fall_time = 0
            x, y = game.update_fig(x, y, fig_mat, "DOWN")

        # EVENTS
        for event in pg.event.get():
            if event.type == pg.QUIT:
                settings.GAME_STATE.CURRENT = settings.GAME_STATE.QUIT
            if event.type == pg.KEYDOWN:
                    pg.key.set_repeat(500, 50)
                    x, y, fig_mat = check_events(event, x, y, fig_mat)

        # SELECTING NEW FIGURE WHEN COLLISION IS DETECTED
        if not game.check_collision(x, y, fig_mat):
            game.set_new_color()
            x, y, fig_mat = figures.select_figure()
            game.set_figure(x, y, fig_mat)
        
        # DRAWING   
        x, y, fig_mat = main_draw_events(x, y, fig_mat)
    
    elif settings.GAME_STATE.CURRENT == settings.GAME_STATE.LOST:
        clock.tick(1)
        main_draw_events(x, y, fig_mat)
        for event in pg.event.get():
            if event.scancode == 41:
                settings.GAME_STATE.CURRENT = settings.GAME_STATE.QUIT

pg.quit()
