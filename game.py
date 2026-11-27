import pygame as pg

from Fig import EMPTY_COLOR, Fig


colors = [(255, 0, 0), (220, 255, 0), (0, 255, 50),
          (0, 0, 255), (0, 200, 255), (190, 0, 255)]

# (row, column) offset per move direction; anything else (e.g. "ROTATE") is (0, 0)
DIRECTIONS = {"DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}


def piece_cells(x, y, fig_mat):
    """Board (row, column) of every filled cell of ``fig_mat`` placed at (x, y)."""
    for i, row in enumerate(fig_mat):
        for j, e in enumerate(row):
            if e == 1:
                yield x + i, y + j


class Game:
    # Note: collision rects use the board row on the x axis and the column on the y axis.

    def __init__(self, settings) -> None:
        self.settings = settings
        self.finished_figures = []
        self.color_ind = -1
        self.current_color = -1

        rows, cols, size = settings.BOARD_HEIGHT, settings.BOARD_WIDTH, settings.CELL_SIZE
        self.grid = [[Fig.empty() for _ in range(cols)] for _ in range(rows)]
        # on-screen rect of every grid cell (column on x, row on y)
        self.screen_rects = [[pg.Rect(c * size, r * size, size, size) for c in range(cols)]
                             for r in range(rows)]

        self.borders = [self.cell_rect(rows, c) for c in range(cols)]
        for r in range(rows):
            self.borders.append(self.cell_rect(r, -1))
            self.borders.append(self.cell_rect(r, cols))

    def cell_rect(self, row, col):
        size = self.settings.CELL_SIZE
        return pg.Rect(row * size, col * size, size, size)

    def is_blocked(self, rect):
        return rect.collidelist(self.finished_figures) != -1 or rect.collidelist(self.borders) != -1

    def set_new_color(self):
        self.color_ind += 1
        self.current_color = colors[self.color_ind % len(colors)]

    @property
    def next_color(self):
        return colors[(self.color_ind + 1) % len(colors)]

    def set_figure(self, x, y, fig_mat):
        for r, c in piece_cells(x, y, fig_mat):
            self.grid[r][c] = Fig.block(self.current_color)

    def clear_figure(self, x, y, fig_mat):
        for r, c in piece_cells(x, y, fig_mat):
            self.grid[r][c] = Fig.empty()

    def draw(self, game_screen):
        for row, rect_row in zip(self.grid, self.screen_rects):
            for fig, rect in zip(row, rect_row):
                pg.draw.rect(game_screen, fig.color, rect, fig.border, fig.border_rad)

    def update_fig(self, x, y, fig_mat, dir):
        dx, dy = DIRECTIONS[dir]
        self.clear_figure(x, y, fig_mat)
        self.set_figure(x + dx, y + dy, fig_mat)
        return x + dx, y + dy

    def check_collision(self, x, y, fig_mat, dir="DOWN"):
        """Return True if the piece can move in ``dir``.

        A blocked downward move locks the piece in place, clears full lines
        and flags game over when the piece is stuck in the top row.
        """
        cur_fig = self.get_fig_from_fig_mat(x, y, fig_mat)
        dx, dy = DIRECTIONS.get(dir, (0, 0))
        size = self.settings.CELL_SIZE

        for rect in cur_fig:
            if self.is_blocked(rect.move(dx * size, dy * size)):
                if dir == "DOWN":
                    self.check_finished_lines()
                    for fig_rect in cur_fig:
                        if fig_rect.x <= 0:
                            print("YOU LOST")
                            self.settings.GAME_STATE.CURRENT = self.settings.GAME_STATE.LOST
                    self.finished_figures += cur_fig
                    for r, c in piece_cells(x, y, fig_mat):
                        self.grid[r][c].placed = True
                return False

        return True

    def rotate(self, x, y, fig_mat):
        for i, row in enumerate(fig_mat):
            for j, e in enumerate(row):
                self.grid[x+i][y+j] = Fig.block(self.current_color) if e else Fig.empty()

    def draw_outlines(self, x, y, fig_mat):
        outline_x = self.find_outline_x(x, y, fig_mat)

        for row in self.grid:
            for fig in row:
                if fig.color == self.current_color and not fig.is_fig:
                    fig.color = EMPTY_COLOR
                    fig.border = 1

        for r, c in piece_cells(outline_x - 1, y, fig_mat):
            self.grid[r][c].color = self.current_color
            self.grid[r][c].border = 2

    def find_outline_x(self, x, y, fig_mat):
        """First row offset (from ``x``) at which the piece would collide."""
        cur_fig = self.get_fig_from_fig_mat(x, y, fig_mat)
        figx = x
        while not any(self.is_blocked(rect) for rect in cur_fig):
            figx += 1
            for rect in cur_fig:
                rect.x += self.settings.CELL_SIZE
        return figx

    def handle_space_event(self, x, y, fig_mat):
        self.clear_figure(x, y, fig_mat)

        x = self.find_outline_x(x, y, fig_mat) - 1
        self.finished_figures += self.get_fig_from_fig_mat(x, y, fig_mat)
        for r, c in piece_cells(x, y, fig_mat):
            fig = self.grid[r][c]
            fig.placed = True
            fig.is_fig = True
            fig.border = 0
        self.check_finished_lines()

    def check_finished_lines(self):
        size = self.settings.CELL_SIZE
        removed_rows = []
        for i, row in enumerate(self.grid):
            if all(fig.placed and fig.is_fig for fig in row):
                removed_rows.append(i)
                self.grid[i][:] = [Fig.empty() for _ in row]

                self.finished_figures[:] = [rect for rect in self.finished_figures if rect.x != i * size]
                for rect in self.finished_figures:
                    if rect.x < i * size:
                        rect.x += size

        for i in removed_rows:
            for j in range(i, -1, -1):
                for k, fig in enumerate(self.grid[j]):
                    if fig.is_fig and fig.placed:
                        self.grid[j+1][k] = fig
                        self.grid[j][k] = Fig.empty()

    def draw_next_fig(self, next_fig_screen, next_fig_mat):
        size = self.settings.CELL_SIZE
        x = (self.settings.WINDOW_WIDTH - self.settings.GAME_WIDTH) / 2 - (len(next_fig_mat) * size / 2)
        y = 2 * size
        for i, j in piece_cells(0, 0, next_fig_mat):
            rect = pg.Rect(j * size + x, i * size + y, size, size)
            pg.draw.rect(next_fig_screen, self.next_color, rect)

    def get_fig_from_fig_mat(self, x, y, fig_mat):
        return [self.cell_rect(r, c) for r, c in piece_cells(x, y, fig_mat)]
