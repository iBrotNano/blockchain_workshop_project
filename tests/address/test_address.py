import keyring
from address.address import Address
from address.custom_address import CustomAddress
from address.solana_address import SolanaAddress
import config.config as config_module


def test_generates_mnemonic():
    mnemonic = Address.generate_mnemonic()
    assert isinstance(mnemonic, str)
    assert len(mnemonic.split()) == 12


def test_mnemonic_is_passed_correctly_to_constructor():
    mnemonic = Address.generate_mnemonic()
    address = Address(mnemonic)
    assert address.get_mnemonic() == mnemonic


def test_custom_address_and_solana_address_is_equal_with_same_mnemonic():
    mnemonic = Address.generate_mnemonic()
    custom_address = CustomAddress(mnemonic)
    solana_address = SolanaAddress(mnemonic)
    assert custom_address.get_mnemonic() == solana_address.get_mnemonic()
    assert custom_address.get_pubkey() == solana_address.get_pubkey()
    assert custom_address.get_address() == solana_address.get_address()


def test_saves_the_keypair(monkeypatch):
    calls = []

    def fake_set_password(service, username, password):
        calls.append((service, username, password))

    monkeypatch.setattr(keyring, "set_password", fake_set_password)
    keypair = CustomAddress(Address.generate_mnemonic())
    keypair.save()

    assert calls == [
        (config_module.APP_NAME, keypair.get_address(), keypair.get_keypair())
    ]


def test_returns_keypair():
    keypair = CustomAddress(Address.generate_mnemonic())
    assert keypair.get_keypair() == keypair.private_key + keypair.public_key


def test_loads_the_keypair(monkeypatch):
    calls = []

    def fake_get_password(service, username):
        calls.append((service, username))
        # TODO: Fix the syntax
        return r"S\xec1s\x14\x07#}N!f\xf7\x16\xf2\xf6\xe9\xe3\xd9\xa6\x13\xb5\xb5\xbdd\x02\x06M\x05\x9c\xd7A\x97'\xfb\xee\xde\xf8\xe9b\xba$\xfeQG\xbd\xf7\xe0/!\xc8\x8bz\xef\x
19\x05\xf0\n\x9a\x9a\xbb\x89\x19\x8d\x1f"

    monkeypatch.setattr(keyring, "get_password", fake_get_password)
    keypair = CustomAddress(Address.generate_mnemonic())
    keypair.load()
    assert calls == [(config_module.APP_NAME, keypair.get_address())]
    # TODO: The loaded data should be stored in the properties of the instance.
