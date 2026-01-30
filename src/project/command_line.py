from pathlib import Path
import questionary


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
