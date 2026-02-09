import hashlib

from pathlib import Path
from project.merkle_root import MerkleRoot


class DummyProject:
    def __init__(self, files):
        self._files = files

    def list_all_files(self):
        return self._files


def _write_file(path: Path, data: bytes) -> Path:
    path.write_bytes(data)
    return path


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def test_gets_project_files(tmp_path):
    files = [
        _write_file(tmp_path / "a.txt", b"a"),
        _write_file(tmp_path / "b.txt", b"b"),
    ]

    project = DummyProject(files)
    merkle = MerkleRoot(project)
    assert merkle.get_files() == files


def test_gets_hash_matches_sha256(tmp_path):
    file_path = _write_file(tmp_path / "data.bin", b"hello world")
    project = DummyProject([file_path])
    merkle = MerkleRoot(project)
    assert merkle._get_file_hash(file_path) == _sha256_hex(b"hello world")


def test_compute_root_of_single_file(tmp_path):
    file_path = _write_file(tmp_path / "only.txt", b"one")
    project = DummyProject([file_path])
    merkle = MerkleRoot(project)
    root = merkle.compute_root()
    assert root == _sha256_hex(b"one")
    assert merkle.get_merkle_root() == root


def test_compute_root_of_two_files(tmp_path):
    file_a = _write_file(tmp_path / "a.txt", b"a")
    file_b = _write_file(tmp_path / "b.txt", b"b")
    project = DummyProject([file_a, file_b])
    merkle = MerkleRoot(project)
    root = merkle.compute_root()
    h1 = _sha256_hex(b"a")
    h2 = _sha256_hex(b"b")
    expected = hashlib.sha256((h1 + h2).encode()).hexdigest()
    assert root == expected


def test_compute_root_of_three_files_duplicates_last(tmp_path):
    file_a = _write_file(tmp_path / "a.txt", b"a")
    file_b = _write_file(tmp_path / "b.txt", b"b")
    file_c = _write_file(tmp_path / "c.txt", b"c")
    project = DummyProject([file_a, file_b, file_c])
    merkle = MerkleRoot(project)
    root = merkle.compute_root()
    h1 = _sha256_hex(b"a")
    h2 = _sha256_hex(b"b")
    h3 = _sha256_hex(b"c")
    level1_left = hashlib.sha256((h1 + h2).encode()).hexdigest()
    level1_right = hashlib.sha256((h3 + h3).encode()).hexdigest()
    expected = hashlib.sha256((level1_left + level1_right).encode()).hexdigest()
    assert root == expected
