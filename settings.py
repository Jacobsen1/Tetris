class game_states:
    CURRENT = 0
    PLAYING = 0
    LOST = 1
    QUIT = 2


BOARD_WIDTH = 12
BOARD_HEIGHT = 24
CELL_SIZE = 30
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 540, BOARD_HEIGHT * CELL_SIZE  # 540, 720
GAME_SIZE = GAME_WIDTH, GAME_HEIGHT = BOARD_WIDTH * CELL_SIZE, WINDOW_HEIGHT  # 360, 720

GAME_STATE = game_states()
SCORE = 0


def init():
    """Reset the mutable game state for a new game."""
    global GAME_STATE, SCORE
    GAME_STATE = game_states()
    SCORE = 0
