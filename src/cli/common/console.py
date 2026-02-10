from config.console import console
from rich.panel import Panel


def print_rule_separated(message: str):
    """Print a standard message followed by a separator rule.

    Args:
        message: The message to display.
    """
    console.print(message)
    console.rule()


def print_info(message: str, title: str = "INFO"):
    """Print an informational message framed by themed rules.

    Args:
        message: The informational message to display.
        title: The title for the information panel with the default 'INFO'.
    """
    console.print(
        Panel(
            f"[info]:information_source: {title}[/info]\n  {message}",
            border_style="info_border",
        )
    )
