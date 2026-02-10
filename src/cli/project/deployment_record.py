from address.address import Address
from project.merkle_root import MerkleRoot


class DeploymentRecord:
    def __init__(self, address: Address, merkle_root: MerkleRoot, metadata: dict):
        self.address = address
        self.merkle_root = merkle_root
        self.metadata = metadata

        # TODO: https://kevinheavey.github.io/solders/tutorials/keypairs.html#signing-and-verifying-messages
