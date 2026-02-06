from solders.keypair import Keypair
from address.address import Address
from mnemonic import Mnemonic
from config.config import MNEMONIC_LANGUAGE


class SolanaAddress(Address):

    def __init__(self, name: str, mnemonic: str = None):
        """
        Genereate a Solana address. Generates from the given mnemonic phrase optionally.

        See: https://kevinheavey.github.io/solders/tutorials/keypairs.html#restoring-a-keypair-from-a-mnemonic-seed-phrase

        :param self: Instance of SolanaAddress
        :param name: Name of the address
        :type name: str
        :param mnemonic: Mnemonic phrase to generate the address
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
        keypair = Keypair.from_seed(seed[:32])
        self.private_key = bytes(keypair)[:32]
        self.public_key = bytes(keypair)[32:]
        self.address = str(keypair.pubkey())

    # TODO: Implement the _from_keypair method to load the keypair from the keyring and set the private key, public key, and address properties accordingly.
