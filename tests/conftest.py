import os
import sys
from pathlib import Path

# Headless SDL: must be set before pygame creates a window.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pygame as pg  # noqa: E402
import pytest  # noqa: E402

import settings  # noqa: E402
from main import TetrisApp  # noqa: E402


class SequenceRng:
    """Stand-in for random.Random that deals pieces in a fixed order."""

    def __init__(self, letters):
        self.letters = list(letters)
        self.i = 0

    def choice(self, _seq):
        letter = self.letters[self.i % len(self.letters)]
        self.i += 1
        return letter


def post_key(key):
    pg.event.post(pg.event.Event(pg.KEYDOWN, key=key, mod=0, unicode="", scancode=0))


class Driver:
    """Small helper API for driving the real game loop like a player."""

    def __init__(self, app):
        self.app = app

    # --- input -----------------------------------------------------------
    def press(self, key, times=1):
        for _ in range(times):
            post_key(key)
            self.frame()

    def post(self, event_type, **attrs):
        pg.event.post(pg.event.Event(event_type, **attrs))
        self.frame()

    def frame(self, dt_ms=0):
        self.app.step(dt_ms)

    # --- inspection ------------------------------------------------------
    @property
    def state(self):
        return settings.GAME_STATE.CURRENT

    def _cells(self, predicate):
        return {
            (r, c)
            for r, row in enumerate(self.app.game.grid)
            for c, fig in enumerate(row)
            if predicate(fig)
        }

    def active_cells(self):
        return self._cells(lambda fig: fig.is_fig and not fig.placed)

    def placed_cells(self):
        return self._cells(lambda fig: fig.is_fig and fig.placed)

    def ghost_cells(self):
        color = self.app.game.current_color
        return self._cells(lambda fig: not fig.is_fig and fig.color == color and fig.border == 2)

    def pixel(self, row, col):
        """Colour at the centre of a board cell as rendered on screen."""
        size = settings.CELL_SIZE
        surface = pg.display.get_surface()
        return tuple(surface.get_at((col * size + size // 2, row * size + size // 2)))[:3]


def make_driver(letters):
    app = TetrisApp(rng=SequenceRng(letters))
    pg.event.clear()
    driver = Driver(app)
    driver.frame()
    return driver


@pytest.fixture
def make_game():
    yield make_driver
    pg.quit()


@pytest.fixture
def game(make_game):
    return make_game("TIOSZLJ")


RESULTS_DIR = ROOT / "test-results"


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """Save a screenshot of the game window for every failing test."""
    report = yield
    if report.when == "call" and report.failed and pg.display.get_init():
        surface = pg.display.get_surface()
        if surface is not None:
            RESULTS_DIR.mkdir(exist_ok=True)
            safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in item.name)
            pg.image.save(surface, str(RESULTS_DIR / f"{safe}.png"))
    return report
