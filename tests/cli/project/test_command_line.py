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
    assert cli.select_project_path() is None


def test_select_project_path_returns_path(monkeypatch):
    _setup_dummy_questionary_path(monkeypatch, "/tmp/project")
    cli = CommandLine()
    result = cli.select_project_path()
    assert isinstance(result, Path)
    assert result == Path("/tmp/project")


def test_displays_merkle_root(monkeypatch):
    calls = []

    def fake_print(message):
        calls.append(("print", message))

    def fake_rule():
        calls.append(("rule",))

    monkeypatch.setattr("project.command_line.console.print", fake_print)
    monkeypatch.setattr("project.command_line.console.rule", fake_rule)

    class DummyMerkleRoot:
        def get_files(self):
            return ["a.txt", "b.txt"]

        def get_merkle_root(self):
            return "root123"

    cli = CommandLine()
    cli.display_merkle_root(DummyMerkleRoot())

    assert calls[0] == ("print", "Merkle root for:")
    assert calls[1] == ("rule",)
    assert ("print", "- a.txt") in calls
    assert ("print", "- b.txt") in calls
    assert calls[-2] == ("rule",)
    assert calls[-1] == ("print", "Merkle Root: root123")
