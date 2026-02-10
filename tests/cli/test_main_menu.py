from main_menu import CommandLine as main_menu
from tests.helpers import fake_method_call


def test_show_returns_none_when_cancelled(monkeypatch):
    monkeypatch.setattr("main_menu.questionary.select", fake_method_call("ask", None))
    cli = main_menu()
    assert cli.show() is None


def test_show_returns_selected_value(monkeypatch):
    monkeypatch.setattr(
        "main_menu.questionary.select",
        fake_method_call("ask", main_menu.EXIT_COMMAND),
    )

    cli = main_menu()
    assert cli.show() == main_menu.EXIT_COMMAND
