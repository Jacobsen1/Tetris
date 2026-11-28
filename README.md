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

## Web version (WebAssembly)

The game also runs in the browser via [pygbag](https://pypi.org/project/pygbag/):

```bash
python -m pip install -r requirements-web.txt
python scripts/build_web.py          # -> build/web/ (static files)
python -m http.server 5004 -d build/web
```

Open http://localhost:5004 and click once to start (browsers require a user
gesture before audio/media can start). The browser runtime is CPython 3.12
loaded from the pygbag CDN, so game code must stay compatible with 3.12.
`build/web/` can be hosted on any static host. In the game hub it is served
on port 5004.
