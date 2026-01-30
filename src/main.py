import hashlib
from pathlib import Path
from project.project import Project
from project.command_line import CommandLine
from config.console import console

project_cli = CommandLine()
project = Project(project_cli.select_project_path())
files = project.list_all_files()


def get_file_hash(file_path: Path) -> str:
    """
    Calculate the SHA-256 hash of a file.

    :param file_path: Path to the file
    :type file_path: Path
    :return: SHA-256 hash as a hexadecimal string
    :rtype: str
    """
    sha256_hash = hashlib.sha256()

    # Read file in chunks (memory-efficient for large files)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)

    return sha256_hash.hexdigest()


# TODO: Extract into a separate MerkleTree class
file_hashes = [get_file_hash(file) for file in files]

while len(file_hashes) > 1:
    if len(file_hashes) % 2 != 0:
        file_hashes.append(file_hashes[-1])

    new_level = []

    for i in range(0, len(file_hashes), 2):
        combined = file_hashes[i] + file_hashes[i + 1]
        new_level.append(hashlib.sha256(combined.encode()).hexdigest())

    file_hashes = new_level

merkle_root = file_hashes[0]
console.print(f"Merkle Root: {merkle_root}")
