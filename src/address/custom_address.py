import base58

from cryptography.hazmat.primitives.asymmetric import ed25519
from mnemonic import Mnemonic
from address.address import Address
from config.config import MNEMONIC_LANGUAGE


class CustomAddress(Address):

    def __init__(self, mnemonic: str):
        """
        Initialize the CustomAddress object with a mnemonic. The mnemonic is passed to the base Address class.
        A new Ed25519 key pair is generated, and the private key, public key, and address are derived from it.
        The address is the Base58-encoded version of the public key.

        :param self: Instance of CustomAddress
        :param mnemonic: The mnemonic seed phrase used to generate the address
        :type mnemonic: str
        """
        super().__init__(mnemonic)
        seed = Mnemonic(MNEMONIC_LANGUAGE).to_seed(self.mnemonic)
        pk = ed25519.Ed25519PrivateKey.from_private_bytes(seed[:32])
        self.private_key = pk.private_bytes_raw()
        self.public_key = pk.public_key().public_bytes_raw()
        self.address = base58.b58encode(self.public_key).decode("ascii")
