import sys
import importlib

from pathlib import Path
from types import ModuleType


# It sets PROJECT_ROOT to the project directory, appends the src path to sys.path, and thereby enables imports from src (e.g., from address.address import Address).

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


def reload_module(module: ModuleType):
    """
    Reload a module to ensure that changes to environment variables are reflected in the module's configuration.

    :param module: The module to reload
    :type module: ModuleType
    """
    importlib.reload(module)
