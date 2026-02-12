from pathlib import Path
from plyvel import DB


class Blockchain:
    def __init__(self):
        """
        Initializes the Blockchain instance and opens the LevelDB database.

        :param self: Instance of Blockchain
        """
        data_dir = Path("data")
        data_dir.mkdir(parents=True, exist_ok=True)
        self._db = DB(str(data_dir / "plockchain.db"), create_if_missing=True)

    def add_block(self, block_bytes: bytes):
        """
        Adds a block to the blockchain by storing it in the LevelDB database with an incrementing height as the key.

        :param self: Instance of Blockchain
        :param block_bytes: The block data in bytes to be added to the blockchain
        :type block_bytes: bytes
        """
        it = self._db.iterator(reverse=True)
        last_key, _ = self._db.next(it)
        last_height = int.from_bytes(last_key, "little")
        last_height += 1
        height_key = last_height.to_bytes(8, "little")  # uint64
        self._db.put(height_key, block_bytes)

    def get_latest_block(self):
        """
        Gets the block with the highest blockheight.
        """
        it = self._db.iterator(reverse=True)
        _, last_value = next(it)
        return last_value

    def close(self):
        """
        Closes the database.
        """
        self._db.close()
