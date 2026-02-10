import json

from address.index import Index
from pathlib import Path
from config.config import LOCAL_APPDATA_PATH


def test_load_index_returns_empty_when_file_missing(monkeypatch):
    monkeypatch.setattr(
        Index, "_index_path", lambda self: Path("non_existent_file.json")
    )

    index = Index()
    assert index.address_names == []


def test_index_path_uses_app_name_lowercase(tmp_path):
    index = Index()
    assert index._index_path() == LOCAL_APPDATA_PATH / ".plockchain_address_index.json"


def test_add_to_index_writes_sorted_unique(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Index, "_index_path", lambda self: tmp_path / ".testapp_address_index.json"
    )

    index = Index()
    index.add_to_index("b")
    index.add_to_index("a")
    index.add_to_index("b")
    data = json.loads(index._index_path().read_text(encoding="utf-8"))
    assert data == ["a", "b"]
    assert index.address_names == ["b", "a"]


def test_load_index_returns_empty_on_invalid_json(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Index, "_index_path", lambda self: tmp_path / ".testapp_address_index.json"
    )

    path = tmp_path / ".testapp_address_index.json"
    path.write_text("{invalid", encoding="utf-8")
    index = Index()
    assert index.address_names == []


def test_get_all_returns_loaded_names(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Index, "_index_path", lambda self: tmp_path / ".testapp_address_index.json"
    )

    path = tmp_path / ".testapp_address_index.json"
    path.write_text(json.dumps(["x", "y"]), encoding="utf-8")
    index = Index()
    assert index.get_all() == ["x", "y"]
