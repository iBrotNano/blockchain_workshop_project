import msgpack
import config.config as config

from address.address import Address
from project.merkle_root import MerkleRoot
from config.console import console
from datetime import datetime
from typing import Any
from hashlib import sha256


# TODO: Test for the class.
class DeploymentRecord:
    address: Address
    merkle_root: MerkleRoot
    metadata: dict[str, Any]

    def __init__(
        self, address: Address, merkle_root: MerkleRoot, metadata: dict[str, Any]
    ):
        """
        Initialize the DeploymentRecord with the given address, Merkle root, and metadata. The metadata is expected to be a dictionary containing relevant information about the deployment.

        :param self: Instance of DeploymentRecord
        :param address: Instance of Address representing the address involved in the deployment
        :type address: Address
        :param merkle_root: Instance of MerkleRoot representing the Merkle root of the deployed project
        :type merkle_root: MerkleRoot
        :param metadata: Dictionary containing metadata about the deployment
        :type metadata: dict
        """
        self.address = address
        self.merkle_root = merkle_root
        self.metadata = metadata

    def serialize(self) -> tuple[bytes, bytes]:
        """
        Serialize the deployment record into a binary format and sign it with the private key of the address. The serialized record includes the version, address, Merkle root, and metadata. The signature is generated using the private key of the address.

        :param self: Instance of DeploymentRecord
        :return: A tuple containing the serialized deployment record and its signature
        :rtype: tuple[bytes, bytes]
        """
        # Works on a shallow copy of the metadata to avoid mutating the original metadata of the deployment record.
        metadata = self.metadata.copy()
        timestamp = metadata.get("timestamp")

        # Convert the timestamp from ISO 8601 format to a UNIX timestamp.
        metadata["timestamp"] = datetime.fromtimestamp(
            datetime.fromisoformat(timestamp).timestamp()
        ).timestamp()

        record = {
            "version": config.DEPLOYMENT_RECORD_VERSION,
            "address": self.address.get_address(),
            "merkle_root": self.merkle_root.get_merkle_root(),
            "metadata": metadata,
        }

        serialized_record = msgpack.packb(record, use_bin_type=True)
        # Is more efficient to sign the hash with a fixed length than the serialized record.
        record_hash = sha256(serialized_record).digest()
        signature = self.address.sign(record_hash)
        return (serialized_record, signature)
