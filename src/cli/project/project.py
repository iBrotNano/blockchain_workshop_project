import pathspec
from pathlib import Path


class Project:
    project_path: Path
    files: list[Path]

    def __init__(self, project_path: Path):
        """
        Ininitialize the Project with the given project path.

        :param self: Instance of Project
        :type self: Project
        :param project_path: Path to the project directory
        :type project_path: Path
        """
        self.project_path = project_path
        self.files = []

    def get_project_path(self) -> Path:
        """
        Get the path to the project directory.

        :return: The path to the project directory
        :rtype: Path
        """
        return self.project_path

    def get_files(self) -> list[Path]:
        """
        Get the list of all files in the project directory, excluding those ignored by .gitignore.

        :return: List of file paths as strings
        :rtype: list[Path]
        """
        return self.files

    def list_all_files(self) -> list[Path]:
        """
        List all files in the project directory, excluding those ignored by .gitignore.

        :return: List of file paths as strings
        :rtype: list[Path]
        """
        if not self.project_path:
            raise ValueError(
                "Project path is not set. Please select a project path first."
            )

        return [
            file
            for file in self.project_path.rglob("*")
            if self._is_source_file(file, self.project_path)
        ]

    def _is_source_file(self, file: Path, project_path: Path) -> bool:
        """
        Determine if a file should be ignored based on .gitignore rules.

        :param file: Path to the file to check
        :type file: Path
        :param project_path: Path to the project root directory
        :type project_path: Path
        :return: True if the file should be ignored, False otherwise
        :rtype: bool
        """
        return (
            ".git" not in file.parts
            and file.is_file()
            and not self._matches_gitignore_rule(file, project_path)
        )

    def _matches_gitignore_rule(self, file_path: Path, root: Path) -> bool:
        """
        Determine if a file should be ignored based on .gitignore rules.

        :param file_path: Path to the file to check
        :param root: Root directory of the project
        :return: True if the file should be ignored, False otherwise
        """
        relative_path = file_path.relative_to(root)

        # Collect all .gitignore files relevant for this path
        current = root

        for part in relative_path.parents:
            gitignore = current / ".gitignore"  # / concatenates paths

            if gitignore.exists():
                with open(gitignore) as f:
                    spec = pathspec.GitIgnoreSpec.from_lines(f.read().splitlines())

                    if spec.match_file(str(relative_path)):
                        return True

            current = current / part

        # Also check .gitignore in the directory of the file
        gitignore_in_dir = file_path.parent / ".gitignore"

        if gitignore_in_dir.exists():
            with open(gitignore_in_dir) as f:
                spec = pathspec.GitIgnoreSpec.from_lines(f.read().splitlines())

                if spec.match_file(str(relative_path)):
                    return True

        return False
