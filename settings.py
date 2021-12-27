from sys import set_coroutine_origin_tracking_depth


class game_states:
    CURRENT = 0
    PLAYING = 0
    LOST = 1
    QUIT = 2

def init():
    global BOARD_WIDTH
    global BOARD_HEIGHT
    global CELL_SIZE
    global WINDOW_SIZE
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    global GAME_SIZE
    global GAME_WIDTH
    global GAME_HEIGHT
    global GAME_STATE
    global SCORE 

    GAME_STATE = game_states()
    BOARD_WIDTH = 12
    BOARD_HEIGHT = 24
    CELL_SIZE = 30
    WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 540, BOARD_HEIGHT * CELL_SIZE
    GAME_SIZE = GAME_WIDTH, GAME_HEIGHT = BOARD_WIDTH * CELL_SIZE, WINDOW_HEIGHT #360, 720
    SCORE = 0


