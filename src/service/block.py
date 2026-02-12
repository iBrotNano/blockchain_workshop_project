import struct
from datetime import datetime


class Block:
    HEADER_FORMAT = "<H Q I I 32s"
    # < = Little‑Endian
    # H = uint16 (2 Bytes) → z.B. Version
    # Q = uint64 (8 Bytes) → z.B. Timestamp
    # I = uint32 (4 Bytes) → z.B. Flags
    # I = uint32 (4 Bytes) → z.B. Payload‑Laenge
    # 32s = 32 Bytes → z.B. Hash (SHA‑256)

    payload: bytes
    signature: bytes
    previous_hash: bytes

    def __init__(self, payload: bytes, signature: bytes, previous_hash: bytes = None):
        """
        Define a Block class that represents a block in the blockchain.
        The block consists of a header, a payload and a signature.
        The header contains metadata about the block, such as the version, timestamp, flags, payload length, and the hash of the previous block.

        :param self: Instance of Block
        :param payload: The payload of the block, which contains the data of the deployment record
        :type payload: bytes
        :param signature: The signature of the record, which is used to verify the authenticity of the record
        :type signature: bytes
        :param previous_hash: The hash of the previous block in the blockchain, used to link the blocks together
        :type previous_hash: bytes, optional
        """
        self.payload = payload
        self.signature = signature

        if previous_hash is None:
            self.previous_hash = bytes(32)  # 32 null bytes for the genesis block
        else:
            self.previous_hash = previous_hash

    def build(self) -> bytes:
        """
        Builds the block.
        """
        header = self._build_header(len(self.payload), self.previous_hash)
        return header + self.payload + self.signature

    def _build_header(
        self,
        payload_length: int,
        previous_hash: bytes,
        version: int = 1,
        flags: int = 0,
    ) -> bytes:
        """
        Builds the header of the block.

        :param self: Instance of Block
        :param payload_length: Length of the payload in bytes, used to indicate how much data is contained in the block.
        :type payload_length: int
        :param previous_hash: Hash of the previous block in the blockchain, used to link the blocks together and ensure the integrity of the blockchain.
        :type previous_hash: bytes
        :param version: Version of the block format, used to indicate the structure and interpretation of the block's data. This allows for future updates to the block format while maintaining backward compatibility.
        :type version: int
        :param flags: Flags the blog as a special kind of block. (Not used right now)
        :type flags: int
        :return: The block as bytes, consisting of the header, payload, and signature.
        :rtype: bytes
        """
        timestamp = int(datetime.now().timestamp())

        return struct.pack(
            self.HEADER_FORMAT,
            version,
            timestamp,
            flags,
            payload_length,
            previous_hash,
        )
