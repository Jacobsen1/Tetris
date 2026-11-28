import asyncio
"""UI tests that drive the real pygame window headlessly with key events."""

import os
import subprocess
import sys

import pygame as pg
import pytest

import settings
from conftest import LANDED_COLOR, ROOT, post_key

BOTTOM = settings.BOARD_HEIGHT - 1


def rows(cells):
    return {r for r, _ in cells}


def cols(cells):
    return {c for _, c in cells}


# --- start-up -----------------------------------------------------------------

def test_app_process_starts_and_keeps_running():
    env = dict(os.environ, SDL_VIDEODRIVER="dummy", SDL_AUDIODRIVER="dummy")
    proc = subprocess.Popen([sys.executable, "main.py"], cwd=ROOT, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        with pytest.raises(subprocess.TimeoutExpired):  # still running = started fine
            proc.wait(timeout=2)
    finally:
        proc.kill()
        proc.wait()


def test_window_opens_with_board_and_side_panels(game):
    surface = pg.display.get_surface()
    assert surface.get_size() == (540, 720)
    assert pg.display.get_caption()[0] == "Tetris"
    assert game.state == settings.GAME_STATE.PLAYING


def test_first_piece_spawns_at_top_and_is_rendered(game):
    # T piece, rotation 0: one cell in row 0, three in row 1, columns 5-7
    assert game.active_cells() == {(0, 6), (1, 5), (1, 6), (1, 7)}
    color = game.app.game.current_color
    for r, c in game.active_cells():
        assert game.pixel(r, c) == color


def test_next_piece_preview_is_drawn(game):
    next_color = game.app.game.next_color
    surface = pg.display.get_surface()
    panel = range(settings.GAME_WIDTH, settings.WINDOW_WIDTH)
    found = any(tuple(surface.get_at((x, y)))[:3] == next_color
                for x in panel for y in range(0, 180, 3))
    assert found, "next-piece preview not rendered in side panel"


def test_ghost_outline_shows_landing_position(game):
    ghost = game.ghost_cells()
    assert len(ghost) == 4
    assert max(rows(ghost)) == BOTTOM
    assert cols(ghost) == cols(game.active_cells())


# --- movement -------------------------------------------------------------------

def test_gravity_moves_piece_down_over_time(game):
    before = game.active_cells()
    game.frame(dt_ms=299)
    assert game.active_cells() == before
    game.frame(dt_ms=1)
    assert game.active_cells() == {(r + 1, c) for r, c in before}


def test_arrow_keys_move_piece_left_and_right(game):
    before = game.active_cells()
    game.press(pg.K_LEFT)
    assert game.active_cells() == {(r, c - 1) for r, c in before}
    game.press(pg.K_RIGHT, times=2)
    assert game.active_cells() == {(r, c + 1) for r, c in before}


def test_walls_stop_the_piece(game):
    game.press(pg.K_LEFT, times=15)
    assert min(cols(game.active_cells())) == 0
    game.press(pg.K_RIGHT, times=20)
    assert max(cols(game.active_cells())) == settings.BOARD_WIDTH - 1


def test_down_arrow_soft_drops_one_row(game):
    before = game.active_cells()
    game.press(pg.K_DOWN)
    assert game.active_cells() == {(r + 1, c) for r, c in before}


def test_up_arrow_rotates_piece(game):
    game.press(pg.K_DOWN)  # leave room above the T for rotation
    game.press(pg.K_UP)
    # T rotation 1 (pointing right), origin moved down one row
    assert game.active_cells() == {(1, 6), (2, 6), (2, 7), (3, 6)}
    game.press(pg.K_UP, times=3)  # full turn back to start orientation
    assert game.active_cells() == {(1, 6), (2, 5), (2, 6), (2, 7)}


# --- landing / line clears ---------------------------------------------------------

def test_space_hard_drops_and_spawns_next_piece(game):
    first_color = game.app.game.current_color
    game.press(pg.K_SPACE)
    assert game.placed_cells() == {(BOTTOM - 1, 6), (BOTTOM, 5), (BOTTOM, 6), (BOTTOM, 7)}
    for r, c in game.placed_cells():
        assert game.pixel(r, c) == first_color
    # next piece (I) appears at the top in a new colour
    assert game.active_cells() == {(1, 5), (1, 6), (1, 7), (1, 8)}
    assert game.app.game.current_color != first_color


def test_piece_lands_by_falling_and_next_piece_spawns(game):
    for _ in range(settings.BOARD_HEIGHT + 2):
        game.frame(dt_ms=300)
        if game.placed_cells():
            break
    assert len(game.placed_cells()) == 4
    assert max(rows(game.placed_cells())) == BOTTOM
    assert len(game.active_cells()) == 4
    assert min(rows(game.active_cells())) <= 1


def test_completed_line_is_cleared_and_stack_shifts_down(make_game):
    game = make_game("IO")
    # bottom row full except the four columns the I piece will drop into
    for c in [0, 1, 2, 3, 4, 9, 10, 11]:
        game.fill(BOTTOM, c)
    game.fill(BOTTOM - 1, 0)  # one block resting on top of the row
    game.frame()

    game.press(pg.K_SPACE)

    assert game.placed_cells() == {(BOTTOM, 0)}
    assert game.pixel(BOTTOM, 1) == (0, 0, 0)


def test_line_completed_by_falling_piece_is_cleared_when_it_lands(make_game):
    game = make_game("IO")
    for c in [0, 1, 2, 3, 4, 9, 10, 11]:
        game.fill(BOTTOM, c)
    game.fill(BOTTOM - 1, 0)
    game.frame()

    # let the I piece fall into the gap by gravity (no hard drop)
    for _ in range(settings.BOARD_HEIGHT + 2):
        game.frame(dt_ms=300)
        if (BOTTOM, 5) in game.placed_cells():
            break

    assert game.placed_cells() == {(BOTTOM, 0)}
    assert game.pixel(BOTTOM, 1) == (0, 0, 0)


def test_rotating_next_to_landed_blocks_keeps_them(make_game):
    game = make_game("T")
    game.press(pg.K_UP, times=2)   # T pointing down: top row of its 3x3 box is empty
    game.press(pg.K_DOWN, times=3)
    x, y = game.app.x, game.app.y
    game.fill(x, y)                # landed block in the empty top-left corner of the box
    game.frame()

    game.press(pg.K_UP)            # rotation itself is allowed: target cells are free

    assert (x, y) in game.placed_cells()
    assert game.pixel(x, y) == LANDED_COLOR


# --- game over / quitting ------------------------------------------------------------

def test_stacking_to_the_top_ends_the_game(make_game):
    game = make_game("O")
    for _ in range(30):
        if game.state == settings.GAME_STATE.LOST:
            break
        game.press(pg.K_SPACE)
    assert game.state == settings.GAME_STATE.LOST

    # game-over screen keeps rendering and ignores non-keyboard events
    game.post(pg.MOUSEMOTION, pos=(10, 10), rel=(1, 1), buttons=(0, 0, 0))
    game.press(pg.K_LEFT)
    assert game.state == settings.GAME_STATE.LOST

    game.press(pg.K_ESCAPE)
    assert game.state == settings.GAME_STATE.QUIT


def test_new_piece_spawning_into_blocks_ends_the_game(make_game):
    game = make_game("OT")
    game.fill(1, 7)                # block where the next piece (T) will appear
    game.frame()
    bottom_rows_before = {cell for cell in game.placed_cells() if cell[0] >= BOTTOM - 1}

    game.press(pg.K_SPACE)         # O lands, T spawns overlapping (1, 7)
    assert game.state == settings.GAME_STATE.LOST

    landed = {cell for cell in game.placed_cells() if cell[0] >= BOTTOM - 1}
    game.press(pg.K_SPACE)         # hard drop must not stamp the piece into the bottom rows
    assert {cell for cell in game.placed_cells() if cell[0] >= BOTTOM - 1} == landed
    assert bottom_rows_before == set()


def test_escape_quits_while_playing(game):
    game.press(pg.K_ESCAPE)
    assert game.state == settings.GAME_STATE.QUIT


def test_closing_window_quits(game):
    game.post(pg.QUIT)
    assert game.state == settings.GAME_STATE.QUIT


@pytest.mark.parametrize("key", [pg.K_LEFT, pg.K_RIGHT, pg.K_DOWN, pg.K_UP, pg.K_SPACE])
def test_run_loop_exits_cleanly_after_input(game, key):
    post_key(key)
    post_key(pg.K_ESCAPE)
    asyncio.run(game.app.run())  # returns once ESC is processed
    assert not pg.display.get_init()
