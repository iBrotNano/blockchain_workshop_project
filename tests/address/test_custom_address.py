import base58
import keyring

from address.custom_address import CustomAddress
from config.config import APP_NAME


def test_address_pubkey_has_correct_length():
    address = CustomAddress("Test", CustomAddress.generate_mnemonic())
    assert len(address.get_pubkey()) == 32


def test_address_matches_pubkey_base58():
    address = CustomAddress("Test", CustomAddress.generate_mnemonic())
    expected = base58.b58encode(address.get_pubkey()).decode("ascii")
    assert address.get_address() == expected


def test_address_changes_per_instance():
    first = CustomAddress("Test1", CustomAddress.generate_mnemonic())
    second = CustomAddress("Test2", CustomAddress.generate_mnemonic())
    assert first.get_pubkey() != second.get_pubkey()
    assert first.get_address() != second.get_address()


def test_generates_mnemonic():
    mnemonic = CustomAddress.generate_mnemonic()
    assert isinstance(mnemonic, str)
    assert len(mnemonic.split()) == 12


def test_same_mnemonic_generates_same_address():
    mnemonic = CustomAddress.generate_mnemonic()
    first = CustomAddress("Test1", mnemonic)
    second = CustomAddress("Test2", mnemonic)
    assert first.get_pubkey() == second.get_pubkey()
    assert first.get_address() == second.get_address()


def test_mnemonic_is_passed_correctly_to_constructor():
    mnemonic = CustomAddress.generate_mnemonic()
    address = CustomAddress("Test", mnemonic)
    assert address.get_mnemonic() == mnemonic


def test_loads_the_keypair(monkeypatch):
    calls = []

    def fake_get_password(service, username):
        calls.append((service, username))
        return base58.b58encode(
            b"6|\xeegI\xa7\xe3yG\x83k<\xd1\xc4\xc1_!\xf5\xcb\xc1\xdf\xc5\xaa\xd3v\xb8|?\xcfa\xecM\xf8JEVS\xceC\xe1\x83\xd4n\n\xa36G\x852x^\xea=\xb2G\xbf\x12\xd4\x17\x00\xda\xc7\xc9+"
        ).decode("ascii")

    monkeypatch.setattr(keyring, "get_password", fake_get_password)
    address = CustomAddress.load("Test")
    assert calls == [(f"{address.name}@{APP_NAME}", "Test")]
    assert type(address) == CustomAddress
    assert address.get_address() == "HiDo5u8nvvCVoxT78m9u6AQwQjy4nUpkmqVE1cDaTHxN"

    assert (
        address.get_keypair()
        == b"6|\xeegI\xa7\xe3yG\x83k<\xd1\xc4\xc1_!\xf5\xcb\xc1\xdf\xc5\xaa\xd3v\xb8|?\xcfa\xecM\xf8JEVS\xceC\xe1\x83\xd4n\n\xa36G\x852x^\xea=\xb2G\xbf\x12\xd4\x17\x00\xda\xc7\xc9+"
    )

    assert (
        address.get_pubkey()
        == b"6|\xeegI\xa7\xe3yG\x83k<\xd1\xc4\xc1_!\xf5\xcb\xc1\xdf\xc5\xaa\xd3v\xb8|?\xcfa\xecM\xf8JEVS\xceC\xe1\x83\xd4n\n\xa36G\x852x^\xea=\xb2G\xbf\x12\xd4\x17\x00\xda\xc7\xc9+"[
            32:
        ]
    )

    assert address.get_mnemonic() == None
