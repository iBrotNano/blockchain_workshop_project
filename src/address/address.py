import keyring

from mnemonic import Mnemonic
from config.config import MNEMONIC_LANGUAGE, APP_NAME


class Address:
    mnemonic: str
    private_key: bytes
    public_key: bytes
    address: str

    def __init__(self, mnemonic: str):
        """
        Initialize the Address object with a mnemonic. The mnemonic is stored as an instance variable,
        and the class provides methods to retrieve the mnemonic, public key, and address. The
        generate_mnemonic static method creates a new mnemonic using the specified language.

        :param self: Instance of Address
        :param mnemonic: The mnemonic seed phrase used to generate the address
        :type mnemonic: str
        """
        self.mnemonic = mnemonic

    def get_mnemonic(self) -> str:
        """
        Get the mnemonic seed phrase used to generate the address.

        :param self: Instance of Address
        :return: The mnemonic seed phrase used to generate the address
        :rtype: str
        """
        return self.mnemonic

    def get_pubkey(self) -> bytes:
        """
        Get the public key associated with the address.

        :param self: Instance of Address
        :return: The public key associated with the address
        :rtype: bytes
        """
        return self.public_key

    def get_address(self) -> str:
        """
        Get the address.

        :param self: Instance of Address
        :return: The address
        :rtype: str
        """
        return self.address

    def get_keypair(self) -> bytes:
        """
        Get the concatenated private and public key.

        :param self: Instance of Address
        :return: The concatenated private and public key
        :rtype: bytes
        """
        return self.private_key + self.public_key

    @staticmethod
    def generate_mnemonic() -> str:
        """
        Generate a new mnemonic seed phrase using the specified language.

        :return: A new mnemonic seed phrase
        :rtype: str
        """
        return Mnemonic(MNEMONIC_LANGUAGE).generate()

    def save(self):
        keyring.set_password(APP_NAME, self.get_address(), self.get_keypair())

    def load(self):
        # TODO: The loaded data should be stored in the properties of the instance.
        return keyring.get_password(APP_NAME, self.get_address())
