from config.console import console, custom_theme
from config import console as console_module


def test_console_is_singleton():
    assert console_module.console is console


def test_custom_theme_is_configured():
    styles = custom_theme.styles
    assert "info" in styles
    assert "info_border" in styles
    assert str(styles["info"]) == "cyan"
    assert str(styles["info_border"]) == "dim cyan"
