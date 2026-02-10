from common import console as console_module
from rich.panel import Panel


def test_print_info_uses_default_title_and_border_style(monkeypatch):
    calls = []

    def fake_print(value):
        calls.append(value)

    monkeypatch.setattr(console_module.console, "print", fake_print)

    console_module.print_info("Hello")

    assert len(calls) == 1
    panel = calls[0]
    assert isinstance(panel, Panel)
    assert panel.border_style == "info_border"
    assert panel.renderable == "[info]:information_source: INFO[/info]\n  Hello"


def test_print_info_uses_custom_title(monkeypatch):
    calls = []

    def fake_print(value):
        calls.append(value)

    monkeypatch.setattr(console_module.console, "print", fake_print)

    console_module.print_info("Details", title="Important")

    assert len(calls) == 1
    panel = calls[0]
    assert isinstance(panel, Panel)
    assert panel.border_style == "info_border"
    assert panel.renderable == "[info]:information_source: Important[/info]\n  Details"
