from pathlib import Path
import hashlib
from project.project import Project


class MerkleRoot:
    project: Project
    files: list[Path]
    merkle_root: str

    def __init__(self, project: Project):
        """
        Initialize the MerkleRoot with a list of files.

        :param self: Instance of MerkleRoot
        :type self: MerkleRoot
        :param project: Project instance containing files to include in the Merkle tree
        :type project: Project
        """
        self.project = project
        self.files = project.list_all_files()

    def get_files(self) -> list[Path]:
        """
        Get the list of files included in the Merkle tree.

        :param self: Instance of MerkleRoot
        :type self: MerkleRoot
        :return: List of file paths
        :rtype: list[Path]
        """
        return self.files

    def get_merkle_root(self) -> str:
        """
        Get the computed Merkle root.

        :param self: Instance of MerkleRoot
        :type self: MerkleRoot
        :return: Merkle root hash
        :rtype: str
        """
        return self.merkle_root

    def compute_root(self):
        """
        Compute the Merkle root from the list of files.

        :param self: Instance of MerkleRoot
        :type self: MerkleRoot
        :return: Merkle root hash
        :rtype: str
        """
        file_hashes = [self._get_file_hash(file) for file in self.files]

        while len(file_hashes) > 1:
            if len(file_hashes) % 2 != 0:
                file_hashes.append(file_hashes[-1])

            new_level = []

            for i in range(0, len(file_hashes), 2):
                combined = file_hashes[i] + file_hashes[i + 1]
                new_level.append(hashlib.sha256(combined.encode()).hexdigest())

            file_hashes = new_level

        self.merkle_root = file_hashes[0]
        return self.merkle_root

    def _get_file_hash(self, file_path: Path) -> str:
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
