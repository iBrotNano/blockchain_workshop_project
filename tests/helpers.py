import importlib
from types import ModuleType


def reload_module(module: ModuleType) -> None:
    """
    Reload a module to ensure that environment changes are reflected.

    :param module: The module to reload
    :type module: ModuleType
    """
    importlib.reload(module)
