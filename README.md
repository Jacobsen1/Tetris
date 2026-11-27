# Tetris

A Tetris clone written in Python with [pygame-ce](https://pyga.me/).

## Requirements

- Python 3.15+
- pygame-ce 2.5.8 (installed from `requirements.txt`)

## Run

```sh
python -m venv .venv
.venv/bin/pip install -r requirements.txt      # Windows: .venv\Scripts\pip
.venv/bin/python main.py
```

Controls: ←/→ move, ↓ soft drop, ↑ rotate, Space hard drop, Esc quit.

## UI tests

The tests in `tests/` start the real game window headlessly
(`SDL_VIDEODRIVER=dummy`), send key events through pygame's event queue,
step the game loop frame by frame, and check the game state and the rendered
pixels. A screenshot of the window is saved to `test-results/` for every
failing test.

```sh
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest
```

CI (`.github/workflows/ci.yml`) runs the same tests on every push and pull
request and uploads `test-results/` as an artifact when they fail.
