from address.command_line import CommandLine
from tests.helpers import fake_method_call


def test_show_returns_none_when_cancelled(monkeypatch):
    monkeypatch.setattr(
        "address.command_line.questionary.select", fake_method_call("ask", None)
    )

    cli = CommandLine()
    assert cli._show_key_management_menu() is None


def test_show_returns_selected_value(monkeypatch):
    monkeypatch.setattr(
        "address.command_line.questionary.select",
        fake_method_call("ask", CommandLine.EXIT_COMMAND),
    )

    cli = CommandLine()
    assert cli._show_key_management_menu() == CommandLine.EXIT_COMMAND


def test_is_key_name_valid():
    cli = CommandLine()
    cli.address_index.address_names = ["existing_key"]

    assert cli._is_key_name_valid("new_key") is True
    assert cli._is_key_name_valid("   ") is False
    assert cli._is_key_name_valid("existing_key") is False


def test_generate_address_adds_to_index_on_save(monkeypatch):
    calls_rule = []
    calls_info = []
    added = []

    class DummyAddress:
        def __init__(self, key_name, mnemonic):
            self._key_name = key_name
            self._mnemonic = mnemonic

        @classmethod
        def generate_mnemonic(cls):
            return "dummy mnemonic"

        def try_save(self):
            return True

        def get_address(self):
            return "ADDR123"

        def get_mnemonic(self):
            return self._mnemonic

    def fake_rule(message):
        calls_rule.append(message)

    def fake_info(message, title):
        calls_info.append((message, title))

    cli = CommandLine()

    monkeypatch.setattr(cli, "_enter_key_name", lambda: "my_key")
    monkeypatch.setattr(cli, "_confirm_save", lambda: True)
    monkeypatch.setattr("address.command_line.CustomAddress", DummyAddress)
    monkeypatch.setattr("address.command_line.print_rule_separated", fake_rule)
    monkeypatch.setattr("address.command_line.print_info", fake_info)

    monkeypatch.setattr(
        cli.address_index, "add_to_index", lambda name: added.append(name)
    )

    cli._generate_address()

    assert added == ["my_key"]
    assert calls_rule == ["Address generated and saved successfully."]
    assert len(calls_info) == 1
    message, title = calls_info[0]
    assert title == "Important information:"
    assert "ADDR123" in message
    assert "dummy mnemonic" in message


def test_generate_address_does_not_add_to_index_on_save_failure(monkeypatch):
    calls_rule = []
    calls_info = []
    added = []

    class DummyAddress:
        def __init__(self, key_name, mnemonic):
            self._key_name = key_name
            self._mnemonic = mnemonic

        @classmethod
        def generate_mnemonic(cls):
            return "dummy mnemonic"

        def try_save(self):
            return False

        def get_address(self):
            return "ADDR123"

        def get_mnemonic(self):
            return self._mnemonic

    def fake_rule(message):
        calls_rule.append(message)

    def fake_info(message, title):
        calls_info.append((message, title))

    cli = CommandLine()

    monkeypatch.setattr(cli, "_enter_key_name", lambda: "my_key")
    monkeypatch.setattr(cli, "_confirm_save", lambda: True)
    monkeypatch.setattr("address.command_line.CustomAddress", DummyAddress)
    monkeypatch.setattr("address.command_line.print_rule_separated", fake_rule)
    monkeypatch.setattr("address.command_line.print_info", fake_info)

    monkeypatch.setattr(
        cli.address_index, "add_to_index", lambda name: added.append(name)
    )

    try:
        cli._generate_address()
    except RuntimeError:
        pass

    assert added == []
    assert calls_rule == []
    assert calls_info == []
