from importlib.metadata import files
from pathlib import Path
import questionary
from config.console import console
from project.merkle_root import MerkleRoot


class CommandLine:
    def select_project_path(self) -> Path | None:
        """
        Prompt the user to input the project directory path.

        :return: The path to the project directory
        :rtype: Path | None
        """
        directory_path = questionary.path(
            "What's the path to the project?", only_directories=True
        ).ask()

        if not directory_path:
            return None

        return Path(directory_path)

    def display_merkle_root(self, merkle_root: MerkleRoot) -> None:
        """
        Display the Merkle root to the user.

        :param merkle_root: The computed Merkle root
        :type merkle_root: None
        """
        console.print(f"Merkle root for:")
        console.rule()

        for file in merkle_root.get_files():
            console.print(f"- {file}")

        console.rule()
        console.print(f"Merkle Root: {merkle_root.get_merkle_root()}")
