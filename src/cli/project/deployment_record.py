import msgpack

from address.address import Address
from config.config import DEPLOYMENT_RECORD_VERSION
from project.merkle_root import MerkleRoot
from config.console import console
from datetime import datetime


# TODO: Test for the class.
class DeploymentRecord:
    def __init__(self, address: Address, merkle_root: MerkleRoot, metadata: dict):
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
        # Store UTC time as timestamp in seconds since the epoch.
        self.metadata["timestamp"] = datetime.fromtimestamp(
            datetime.fromisoformat(self.metadata["timestamp"]).timestamp()
        ).timestamp()

        record = {
            "version": DEPLOYMENT_RECORD_VERSION,
            "address": self.address.get_address(),
            "merkle_root": self.merkle_root.get_merkle_root(),
            "metadata": self.metadata,
        }

        serialized_record = msgpack.packb(record, use_bin_type=True)
        signature = self.address.sign(serialized_record)
        return (serialized_record, signature)
