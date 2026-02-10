from pathlib import Path
from project.command_line import CommandLine


def _setup_dummy_questionary_path(monkeypatch, return_value):
    class DummyQuestion:
        def ask(self):
            return return_value

    def fake_path(*_args, **_kwargs):
        return DummyQuestion()

    monkeypatch.setattr("project.command_line.questionary.path", fake_path)


def test_select_project_path_returns_none_when_cancelled(monkeypatch):
    _setup_dummy_questionary_path(monkeypatch, None)
    cli = CommandLine()
    assert cli._select_project_path() is None


def test_select_project_path_returns_path(monkeypatch):
    _setup_dummy_questionary_path(monkeypatch, "/tmp/project")
    cli = CommandLine()
    result = cli._select_project_path()
    assert isinstance(result, Path)
    assert result == Path("/tmp/project")


def test_select_key_with_no_addresses_returns_none_and_prints_info(monkeypatch):
    cli = CommandLine()
    monkeypatch.setattr(cli.address_index, "get_all", lambda: [])

    info_calls = []

    def fake_print_info(message):
        info_calls.append(message)

    def fail_select(*_args, **_kwargs):
        raise AssertionError("select should not be called")

    def fail_load(*_args, **_kwargs):
        raise AssertionError("load should not be called")

    monkeypatch.setattr("project.command_line.print_info", fake_print_info)
    monkeypatch.setattr("project.command_line.questionary.select", fail_select)
    monkeypatch.setattr("project.command_line.CustomAddress.load", fail_load)

    result = cli._select_key()

    assert result is None
    assert info_calls == ["No addresses found. Please generate an address first."]


def test_select_key_cancel_returns_none(monkeypatch):
    cli = CommandLine()
    monkeypatch.setattr(cli.address_index, "get_all", lambda: ["key1"])

    captured = {"prompt": None, "choices": None, "use_shortcuts": None}

    class DummyChoice:
        def __init__(self, title, value):
            self.title = title
            self.value = value

    class DummyQuestion:
        def ask(self):
            return None

    def fake_select(prompt, choices, use_shortcuts):
        captured["prompt"] = prompt
        captured["choices"] = choices
        captured["use_shortcuts"] = use_shortcuts
        return DummyQuestion()

    def fail_load(*_args, **_kwargs):
        raise AssertionError("load should not be called")

    monkeypatch.setattr("project.command_line.questionary.Choice", DummyChoice)
    monkeypatch.setattr("project.command_line.questionary.select", fake_select)
    monkeypatch.setattr("project.command_line.CustomAddress.load", fail_load)

    result = cli._select_key()

    assert result is None
    assert captured["prompt"] == "Select a key:"
    assert captured["use_shortcuts"] is True
    assert [c.value for c in captured["choices"]] == ["key1", "Cancel"]


def test_select_key_returns_loaded_address(monkeypatch):
    cli = CommandLine()
    monkeypatch.setattr(cli.address_index, "get_all", lambda: ["key1", "key2"])

    captured = {"choices": None}
    loaded = {"name": None}
    expected_address = object()

    class DummyChoice:
        def __init__(self, title, value):
            self.title = title
            self.value = value

    class DummyQuestion:
        def ask(self):
            return "key2"

    def fake_select(_prompt, choices, **_kwargs):
        captured["choices"] = choices
        return DummyQuestion()

    def fake_load(name):
        loaded["name"] = name
        return expected_address

    monkeypatch.setattr("project.command_line.questionary.Choice", DummyChoice)
    monkeypatch.setattr("project.command_line.questionary.select", fake_select)
    monkeypatch.setattr("project.command_line.CustomAddress.load", fake_load)

    result = cli._select_key()

    assert result is expected_address
    assert loaded["name"] == "key2"
    assert [c.value for c in captured["choices"]] == ["key1", "key2", "Cancel"]


def test_show_returns_when_address_missing(monkeypatch):
    cli = CommandLine()
    monkeypatch.setattr(cli, "_select_key", lambda: None)
    monkeypatch.setattr(
        cli,
        "_select_project_path",
        lambda: (_ for _ in ()).throw(AssertionError("should not be called")),
    )
    calls = []
    monkeypatch.setattr(
        "project.command_line.print_info", lambda message: calls.append(message)
    )

    cli.show()

    assert calls == []


def test_show_returns_when_path_missing(monkeypatch):
    cli = CommandLine()

    class DummyAddress:
        def get_address(self):
            return "ADDR"

    monkeypatch.setattr(cli, "_select_key", lambda: DummyAddress())
    monkeypatch.setattr(cli, "_select_project_path", lambda: None)
    calls = []
    monkeypatch.setattr(
        "project.command_line.print_info", lambda message: calls.append(message)
    )

    cli.show()

    assert calls == []


def test_show_prints_selected_address_when_both_present(monkeypatch):
    cli = CommandLine()

    class DummyMerkleRoot:
        def __init__(self, _project):
            pass

        def compute_root(self):
            return None

        def get_files(self):
            return ["a.txt"]

        def get_merkle_root(self):
            return "root123"

    class DummyAddress:
        def get_address(self):
            return "ADDR123"

    monkeypatch.setattr(cli, "_select_key", lambda: DummyAddress())
    monkeypatch.setattr(cli, "_select_project_path", lambda: Path("/tmp/project"))
    monkeypatch.setattr("project.command_line.MerkleRoot", DummyMerkleRoot)
    calls = []

    monkeypatch.setattr(
        "project.command_line.print_info", lambda message: calls.append(message)
    )

    cli.show()

    assert calls == [
        "Data of the deployment record:\n\n\tSelected address: ADDR123\n\n\tMerkle root: root123\n\n\tFiles included in the Merkle tree:\n\t\t- a.txt\n"
    ]
