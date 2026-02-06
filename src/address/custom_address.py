import base58

from cryptography.hazmat.primitives.asymmetric import ed25519
from mnemonic import Mnemonic
from address.address import Address
from config.config import MNEMONIC_LANGUAGE


class CustomAddress(Address):

    def __init__(self, name: str, mnemonic: str = None):
        """
        Initialize the CustomAddress. If a mnemonic is passed to the base Address class,
        a new Ed25519 key pair is generated, and the private key, public key, and address are derived from it.
        The address is the Base58-encoded version of the public key.

        :param self: Instance of CustomAddress
        :param name: Name of the address
        :type name: str
        :param mnemonic: The mnemonic seed phrase used to generate the address
        :type mnemonic: str
        """
        super().__init__(name, mnemonic)

        if mnemonic is not None:
            self._from_mnemonic()

    def _from_mnemonic(self):
        """
        Generate the private key, public key, and address from the mnemonic seed phrase. The private key is derived
        using the Ed25519 algorithm, and the address is the Base58-encoded version of the public key.
        """
        seed = Mnemonic(MNEMONIC_LANGUAGE).to_seed(self.mnemonic)
        pk = ed25519.Ed25519PrivateKey.from_private_bytes(seed[:32])
        self.private_key = pk.private_bytes_raw()
        self.public_key = pk.public_key().public_bytes_raw()
        self.address = base58.b58encode(self.public_key).decode("ascii")

    def _from_keypair(self, keypair: bytes):
        """
        Load the key pair from the keyring and set the private key, public key,
        and address properties accordingly. The key pair is expected to be a
        concatenation of the private and public key bytes.
        :param self: Instance of CustomAddress
        :param keypair: The concatenated private and public key bytes
        :type keypair: bytes
        """
        self.private_key = keypair[:32]
        self.public_key = keypair[32:]
        self.address = base58.b58encode(self.public_key).decode("ascii")
