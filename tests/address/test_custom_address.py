import base58

from address.custom_address import CustomAddress


def test_address_pubkey_has_correct_length():
    address = CustomAddress(CustomAddress.generate_mnemonic())
    assert len(address.get_pubkey()) == 32


def test_address_matches_pubkey_base58():
    address = CustomAddress(CustomAddress.generate_mnemonic())
    expected = base58.b58encode(address.get_pubkey()).decode("ascii")
    assert address.get_address() == expected


def test_address_changes_per_instance():
    first = CustomAddress(CustomAddress.generate_mnemonic())
    second = CustomAddress(CustomAddress.generate_mnemonic())
    assert first.get_pubkey() != second.get_pubkey()
    assert first.get_address() != second.get_address()


def test_generates_mnemonic():
    mnemonic = CustomAddress.generate_mnemonic()
    assert isinstance(mnemonic, str)
    assert len(mnemonic.split()) == 12


def test_same_mnemonic_generates_same_address():
    mnemonic = CustomAddress.generate_mnemonic()
    first = CustomAddress(mnemonic)
    second = CustomAddress(mnemonic)
    assert first.get_pubkey() == second.get_pubkey()
    assert first.get_address() == second.get_address()


def test_mnemonic_is_passed_correctly_to_constructor():
    mnemonic = CustomAddress.generate_mnemonic()
    address = CustomAddress(mnemonic)
    assert address.get_mnemonic() == mnemonic
