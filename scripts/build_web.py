"""Build the browser (WebAssembly) version of Tetris with pygbag.

Only the game's own sources are copied into a clean staging folder, so the
virtualenv, tests and caches never end up in the web bundle. The result is
static files in build/web/ that any static host can serve.
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ["main.py", "game.py", "Fig.py", "Figures.py", "settings.py"]
STAGE = ROOT / "build" / "stage" / "tetris"
OUT = ROOT / "build" / "web"


def main() -> int:
    shutil.rmtree(ROOT / "build", ignore_errors=True)
    STAGE.mkdir(parents=True)
    for name in SOURCES:
        shutil.copy2(ROOT / name, STAGE / name)

    result = subprocess.run(
        [sys.executable, "-m", "pygbag", "--build", "--title", "Tetris", str(STAGE)],
        cwd=ROOT,
    )
    if result.returncode != 0:
        return result.returncode

    shutil.copytree(STAGE / "build" / "web", OUT)
    shutil.rmtree(ROOT / "build" / "stage")
    if not (OUT / "index.html").is_file():
        print("pygbag did not produce build/web/index.html", file=sys.stderr)
        return 1
    print(f"Web build ready in {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
