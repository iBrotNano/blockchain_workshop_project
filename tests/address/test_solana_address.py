import base58

from address.solana_address import SolanaAddress


def test_address_pubkey_has_correct_length():
    address = SolanaAddress(SolanaAddress.generate_mnemonic())
    assert len(address.get_pubkey()) == 32


def test_address_matches_pubkey_base58():
    address = SolanaAddress(SolanaAddress.generate_mnemonic())
    expected = base58.b58encode(address.get_pubkey()).decode("ascii")
    assert address.get_address() == expected


def test_address_changes_with_different_mnemonics():
    first = SolanaAddress(SolanaAddress.generate_mnemonic())
    second = SolanaAddress(SolanaAddress.generate_mnemonic())
    assert first.get_pubkey() != second.get_pubkey()
    assert first.get_address() != second.get_address()


def test_generates_mnemonic():
    mnemonic = SolanaAddress.generate_mnemonic()
    assert isinstance(mnemonic, str)
    assert len(mnemonic.split()) == 12


def test_same_mnemonic_generates_same_address():
    mnemonic = SolanaAddress.generate_mnemonic()
    first = SolanaAddress(mnemonic)
    second = SolanaAddress(mnemonic)
    assert first.get_pubkey() == second.get_pubkey()
    assert first.get_address() == second.get_address()


def test_mnemonic_is_passed_correctly_to_constructor():
    mnemonic = SolanaAddress.generate_mnemonic()
    address = SolanaAddress(mnemonic)
    assert address.get_mnemonic() == mnemonic
