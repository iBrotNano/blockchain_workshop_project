from solders.keypair import Keypair
from address.address import Address
from mnemonic import Mnemonic
from config.config import MNEMONIC_LANGUAGE


class SolanaAddress(Address):

    def __init__(self, mnemonic: str):
        """
        Genereate a Solana address from a mnemonic phrase.

        See: https://kevinheavey.github.io/solders/tutorials/keypairs.html#restoring-a-keypair-from-a-mnemonic-seed-phrase

        :param self: Instance of SolanaAddress
        :param mnemonic: Mnemonic phrase to generate the address
        :type mnemonic: str
        """
        super().__init__(mnemonic)
        seed = Mnemonic(MNEMONIC_LANGUAGE).to_seed(self.mnemonic)
        keypair = Keypair.from_seed(seed[:32])
        self.private_key = bytes(keypair)[:32]
        self.public_key = bytes(keypair)[32:]
        self.address = str(keypair.pubkey())
