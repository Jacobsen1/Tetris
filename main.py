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
score_screen = pg.surface.Surface((settings.WINDOW_WIDTH-settings.GAME_WIDTH, settings.WINDOW_WIDTH-settings.GAME_WIDTH))


figures = Figures()
game = Game(settings)


def check_events(event, x, y, fig_mat):
    if event.scancode == 80 and game.check_collision(x, y, fig_mat, "LEFT"):
        pg.key.set_repeat(400, 75)
        x, y = game.update_fig(x, y, fig_mat, "LEFT")
    elif event.scancode == 79 and game.check_collision(x, y, fig_mat, "RIGHT"):
        pg.key.set_repeat(400, 75)
        x, y = game.update_fig(x, y, fig_mat, "RIGHT")
    elif event.scancode == 81 and game.check_collision(x, y, fig_mat):
        pg.key.set_repeat(1, 50)
        x, y = game.update_fig(x, y, fig_mat, "DOWN")
    elif event.scancode == 82 and game.check_collision(x, y, figures.get_next_fig_mat(), "ROTATE"):
        pg.key.set_repeat(0)
        fig_mat = figures.rotate()
        game.rotate(x, y, fig_mat)
    elif event.scancode == 41:
        settings.GAME_STATE.CURRENT = settings.GAME_STATE.QUIT
    elif event.scancode == 44:
        game.handle_space_event(x, y, fig_mat)
        x, y, fig_mat = new_figure()

    return x, y, fig_mat

def main_draw_events(x, y, fig_mat):
    game_screen.fill((0,   0,   0))
    next_fig_screen.fill((0,   0,   0))
    score_screen.fill((0,   0,   0))
    game.draw(game_screen)
    game.draw_outlines(x, y, fig_mat)
    game.draw_next_fig(next_fig_screen, figures.get_next_fig())

    pg.draw.rect(next_fig_screen, (75, 75, 75), [(0, 0), next_fig_screen.get_size()], 2, 3)
    next_fig_screen.blit(next_fig_text, (next_fig_screen.get_size()[0]/2 - myfont.size('Next Figure')[0]/2, 15))

    pg.draw.rect(score_screen, (75, 75, 75), [(0, 0), next_fig_screen.get_size()], 2, 3)
    score = str(settings.SCORE)
    score_val_text = score_font.render(score, True, (75, 75, 75))
    score_screen.blit(score_text, (score_screen.get_size()[0]/2 - myfont.size('Score')[0]/2, 15))
    score_screen.blit(score_val_text, (score_screen.get_size()[0]/2 - score_font.size(score)[0]/2,score_screen.get_size()[1]/2 - score_font.size(score)[1]/2 ))

    main_screen.blit(game_screen, (0,0))
    main_screen.blit(next_fig_screen, (settings.GAME_WIDTH, 0))
    main_screen.blit(score_screen, (settings.GAME_WIDTH, score_screen.get_size()[1]))

    pg.display.flip()
    return x, y, fig_mat

def new_figure():
    game.set_new_color()
    x, y, fig_mat = figures.select_figure()
    game.set_figure(x, y, fig_mat)
    return x, y, fig_mat

myfont = pg.font.SysFont('Roboto', 30)
score_font = pg.font.SysFont('Roboto', 45)
next_fig_text = myfont.render('Next Figure', True, (255, 255, 255))
score_text = myfont.render("Score", True, (255, 255, 255))
score_val_text = score_font.render("", True, (75, 75, 75))

x, y, fig_mat = new_figure()
fall_time = 0
clock = pg.time.Clock()
while settings.GAME_STATE.CURRENT != settings.GAME_STATE.QUIT:
    clock.tick(60)
    if(settings.GAME_STATE.CURRENT == settings.GAME_STATE.PLAYING):
        # FALL SPEED
        fall_time += clock.get_rawtime()
        if fall_time >= 300:
            fall_time = 0
            x, y = game.update_fig(x, y, fig_mat, "DOWN")
        # EVENTS
        for event in pg.event.get():
            if event.type == pg.QUIT:
                settings.GAME_STATE.CURRENT = settings.GAME_STATE.QUIT
            if event.type == pg.KEYDOWN:
                x, y, fig_mat = check_events(event, x, y, fig_mat)

        # SELECTING NEW FIGURE WHEN COLLISION IS DETECTED
        if not game.check_collision(x, y, fig_mat):
            x, y, fig_mat = new_figure()
            fall_time = 0
        
        # DRAWING
        x, y, fig_mat = main_draw_events(x, y, fig_mat)
    
    elif settings.GAME_STATE.CURRENT == settings.GAME_STATE.LOST:
        main_draw_events(x, y, fig_mat)
        for event in pg.event.get():
            if event.scancode == 41:
                settings.GAME_STATE.CURRENT = settings.GAME_STATE.QUIT

pg.quit()
