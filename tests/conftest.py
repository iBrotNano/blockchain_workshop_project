import sys

from pathlib import Path


# It sets PROJECT_ROOT to the project directory, appends the src/cli path to sys.path, and thereby enables imports like address.address.

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src" / "cli"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


from config.config import configure

configure()
