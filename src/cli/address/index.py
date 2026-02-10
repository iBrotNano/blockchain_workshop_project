import json
import config.config as config

from pathlib import Path


class Index:
    address_names: list[str]

    def __init__(self):
        """Initializes the Index instance and loads the address names from the index file.

        :param self: Instance of Index"""
        self.address_names = self._load_index()

    def add_to_index(self, name: str) -> None:
        """Adds a new address name to the index if it does not already exist, and saves the updated index.

        :param self: Instance of Index
        :param name: The name of the address to add to the index
        :type name: str
        :return: None"""
        if name not in self.address_names:
            self.address_names.append(name)
            self._save_index(self.address_names)

    def get_all(self) -> list[str]:
        """Returns a list of all address names currently stored in the index.

        :param self: Instance of Index
        :return: A list of all address names in the index
        :rtype: list[str]"""
        return self.address_names

    def _index_path(self) -> Path:
        """Returns the file path to the index file where address names are stored.

        :param self: Instance of Index
        :return: The file path to the index file
        :rtype: Path
        """
        return (
            config.LOCAL_APPDATA_PATH / f".{config.APP_NAME.lower()}_address_index.json"
        )

    def _load_index(self) -> list[str]:
        """Loads the address names from the index file. If the file does not exist or contains invalid JSON, it returns an empty list.

        :param self: Instance of Index
         :return: A list of address names loaded from the index file, or an empty list if the file is missing or invalid
         :rtype: list[str]
        """
        path = self._index_path()

        if not path.exists():
            return []

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []

        return [name for name in data]

    def _save_index(self, names: list[str]) -> None:
        """Saves the index file to disk.

        :param self: Instance of Index
        :param name: Names in the index
        :type name: list[str]
        """
        path = self._index_path()
        path.write_text(json.dumps(sorted(set(names))), encoding="utf-8")
