import base58
import keyring

from address.address import Address
from address.custom_address import CustomAddress
from address.solana_address import SolanaAddress
from config.config import APP_NAME


def test_generates_mnemonic():
    mnemonic = Address.generate_mnemonic()
    assert isinstance(mnemonic, str)
    assert len(mnemonic.split()) == 12


def test_mnemonic_is_passed_correctly_to_constructor():
    mnemonic = Address.generate_mnemonic()
    address = Address("Test", mnemonic)
    assert address.get_mnemonic() == mnemonic


def test_custom_address_and_solana_address_is_equal_with_same_mnemonic():
    mnemonic = Address.generate_mnemonic()
    custom_address = CustomAddress("Test", mnemonic)
    solana_address = SolanaAddress("Test", mnemonic)
    assert custom_address.get_mnemonic() == solana_address.get_mnemonic()
    assert custom_address.get_pubkey() == solana_address.get_pubkey()
    assert custom_address.get_address() == solana_address.get_address()


def test_saves_the_keypair(monkeypatch):
    calls = []

    def fake_set_password(service, username, password):
        calls.append((service, username, password))

    monkeypatch.setattr(keyring, "set_password", fake_set_password)
    address = CustomAddress("Test", Address.generate_mnemonic())
    address.save()

    assert calls == [
        (
            f"{address.name}@{APP_NAME}",
            address.name,
            base58.b58encode(address.get_keypair()).decode("ascii"),
        )
    ]


def test_returns_keypair():
    address = CustomAddress("Test", Address.generate_mnemonic())
    assert address.get_keypair() == address.private_key + address.public_key
