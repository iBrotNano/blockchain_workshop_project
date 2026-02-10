import base58
import keyring
import config.config as config

from mnemonic import Mnemonic
from typing import Self


class Address:
    mnemonic: str
    private_key: bytes
    public_key: bytes
    address: str
    name: str

    def __init__(self, name: str, mnemonic: str = None):
        """
        Initialize the Address object with a mnemonic. The mnemonic is stored as an instance variable,
        and the class provides methods to retrieve the mnemonic, public key, and address. The
        generate_mnemonic static method creates a new mnemonic using the specified language.

        :param self: Instance of Address
        :param name: Name of the address
        :type name: str
        :param mnemonic: The mnemonic seed phrase used to generate the address
        :type mnemonic: str
        """
        self.mnemonic = mnemonic
        self.name = name

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
        return Mnemonic(config.MNEMONIC_LANGUAGE).generate()

    def try_save(self) -> bool:
        """
        Saves the key pair in a secure way in Windows-Keychain/DPAPI in user scope using the keyring library.
        The key pair is stored as a concatenation of the private and public key bytes.

        :param self: Instance of Address
        :return: True if the key pair was saved successfully, False otherwise
        """
        try:
            try:
                keyring.delete_password(f"{self.name}@{config.APP_NAME}", self.name)
            except keyring.errors.PasswordDeleteError:
                pass  # Ignore if the password does not exist

            encoded_keypair = base58.b58encode(self.get_keypair()).decode("ascii")
            keyring.set_password(
                f"{self.name}@{config.APP_NAME}", self.name, encoded_keypair
            )
        except:
            return False

        return True

    @classmethod
    def load(cls, name: str) -> Self:
        """
        Loads the key pair from Windows-Keychain/DPAPI using the keyring library.
        The key pair is retrieved as a concatenation of the private and public key bytes,
        which are then split and stored in the properties of the instance.

        :param cls: The class of the address to load
        :type cls: type[Self]
        :param name: The name of the address to load
        :type name: str
        :return: An instance of the address with the loaded key pair
        :rtype: Self
        """
        keypair_encoded = keyring.get_password(f"{name}@{config.APP_NAME}", name)

        if keypair_encoded is None:
            raise ValueError(f"No keypair found for name: {name}")

        keypair = base58.b58decode(keypair_encoded.encode("ascii"))
        address = cls(name)
        address._from_keypair(keypair)
        return address

    def _from_keypair(self, keypair: bytes):
        """
        This method should be implemented by subclasses of Address
        to load the key pair from the keyring and set the private key,
        public key, and address properties accordingly.
        :param self: Instance of Address
        :param keypair: The concatenated private and public key bytes
        :type keypair: bytes
        """
        raise NotImplementedError(
            "This method should be implemented by subclasses of Address."
        )
