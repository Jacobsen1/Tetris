#!/usr/bin/env python3
import pygame as pg

from Fig import EMPTY_COLOR
from Figures import Figures
from game import Game
import settings

FALL_INTERVAL_MS = 300
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class TetrisApp:
    """Owns the window, the game state and the main loop.

    The loop is split into ``step()`` so the game can be driven frame by
    frame (e.g. from UI tests running with ``SDL_VIDEODRIVER=dummy``).
    """

    def __init__(self, rng=None) -> None:
        settings.init()
        pg.init()

        self.main_screen = pg.display.set_mode(settings.WINDOW_SIZE)
        pg.display.set_caption("Tetris")
        side = settings.WINDOW_WIDTH - settings.GAME_WIDTH
        self.game_screen = pg.surface.Surface(settings.GAME_SIZE)
        self.next_fig_screen = pg.surface.Surface((side, side))
        self.score_screen = pg.surface.Surface((side, side))

        self.myfont = pg.font.SysFont('Roboto', 30)
        self.score_font = pg.font.SysFont('Roboto', 45)
        # (rendered title, x position centring it in its side panel)
        self.next_fig_title = self._panel_title('Next Figure', side)
        self.score_title = self._panel_title('Score', side)

        self.figures = Figures(rng)
        self.game = Game(settings)
        self.x, self.y, self.fig_mat = self.new_figure()
        self.fall_time = 0
        self.clock = pg.time.Clock()

    @property
    def state(self):
        return settings.GAME_STATE.CURRENT

    @state.setter
    def state(self, value):
        settings.GAME_STATE.CURRENT = value

    def new_figure(self):
        self.game.set_new_color()
        x, y, fig_mat = self.figures.select_figure()
        self.game.set_figure(x, y, fig_mat)
        return x, y, fig_mat

    def check_events(self, event):
        game, x, y, fig_mat = self.game, self.x, self.y, self.fig_mat
        if event.key == pg.K_LEFT and game.check_collision(x, y, fig_mat, "LEFT"):
            pg.key.set_repeat(400, 75)
            x, y = game.update_fig(x, y, fig_mat, "LEFT")
        elif event.key == pg.K_RIGHT and game.check_collision(x, y, fig_mat, "RIGHT"):
            pg.key.set_repeat(400, 75)
            x, y = game.update_fig(x, y, fig_mat, "RIGHT")
        elif event.key == pg.K_DOWN and game.check_collision(x, y, fig_mat):
            pg.key.set_repeat(1, 50)
            x, y = game.update_fig(x, y, fig_mat, "DOWN")
        elif event.key == pg.K_UP and game.check_collision(x, y, self.figures.get_next_fig_mat(), "ROTATE"):
            pg.key.set_repeat(0)
            fig_mat = self.figures.rotate()
            game.rotate(x, y, fig_mat)
        elif event.key == pg.K_ESCAPE:
            self.state = settings.GAME_STATE.QUIT
        elif event.key == pg.K_SPACE:
            game.handle_space_event(x, y, fig_mat)
            x, y, fig_mat = self.new_figure()

        self.x, self.y, self.fig_mat = x, y, fig_mat

    def _panel_title(self, text, panel_width):
        return self.myfont.render(text, True, WHITE), panel_width / 2 - self.myfont.size(text)[0] / 2

    @staticmethod
    def _draw_panel(surface, title):
        """Draw a side panel's frame and its centred title."""
        pg.draw.rect(surface, EMPTY_COLOR, [(0, 0), surface.get_size()], 2, 3)
        text, x = title
        surface.blit(text, (x, 15))

    def draw(self):
        for surface in (self.game_screen, self.next_fig_screen, self.score_screen):
            surface.fill(BLACK)
        self.game.draw(self.game_screen)
        self.game.draw_outlines(self.x, self.y, self.fig_mat)
        self.game.draw_next_fig(self.next_fig_screen, self.figures.get_next_fig())
        self._draw_panel(self.next_fig_screen, self.next_fig_title)

        self._draw_panel(self.score_screen, self.score_title)
        score = str(settings.SCORE)
        score_w, score_h = self.score_font.size(score)
        panel_w, panel_h = self.score_screen.get_size()
        self.score_screen.blit(self.score_font.render(score, True, EMPTY_COLOR),
                               (panel_w / 2 - score_w / 2, panel_h / 2 - score_h / 2))

        self.main_screen.blit(self.game_screen, (0, 0))
        self.main_screen.blit(self.next_fig_screen, (settings.GAME_WIDTH, 0))
        self.main_screen.blit(self.score_screen, (settings.GAME_WIDTH, panel_h))

        pg.display.flip()

    def step(self, dt_ms):
        """Advance the game by one frame that took ``dt_ms`` milliseconds."""
        if self.state == settings.GAME_STATE.PLAYING:
            # FALL SPEED
            self.fall_time += dt_ms
            if self.fall_time >= FALL_INTERVAL_MS:
                self.fall_time = 0
                self.x, self.y = self.game.update_fig(self.x, self.y, self.fig_mat, "DOWN")
            # EVENTS
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.state = settings.GAME_STATE.QUIT
                if event.type == pg.KEYDOWN:
                    self.check_events(event)

            # SELECTING NEW FIGURE WHEN COLLISION IS DETECTED
            if self.state == settings.GAME_STATE.PLAYING and not self.game.check_collision(self.x, self.y, self.fig_mat):
                self.x, self.y, self.fig_mat = self.new_figure()
                self.fall_time = 0

            # DRAWING
            self.draw()

        elif self.state == settings.GAME_STATE.LOST:
            self.draw()
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.state = settings.GAME_STATE.QUIT

    def run(self):
        while self.state != settings.GAME_STATE.QUIT:
            self.clock.tick(60)
            self.step(self.clock.get_rawtime())
        pg.quit()


def main():
    TetrisApp().run()


if __name__ == "__main__":
    main()
